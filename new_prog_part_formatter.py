import sys
import xml.etree.ElementTree as ET

#create a line break element
LINE_BREAK = ET.Element("LayoutBreak")
temp = ET.SubElement(LINE_BREAK, "subtype")
temp.text = "line"

def _add_line_break_to_measure(measure):
    "adds line break to a given measure -- right before voice tag"
    index = 0
    for elem in measure:
        if elem.tag == "voice":
            break
        index += 1
    
    #insert line break at insert pos
    measure.insert(index, LINE_BREAK)



def prep_mm_rests(staff):
    """
    Go through each measure in score. 
    if measure n has a "len" attribute: then mark that measure and the next m (m = measure->multiMeasureRest -1) measures with the "_mm" attribute
    """
    measure_to_mark = 0
    for elem in staff:
        if elem.tag == "Measure":
            if measure_to_mark > 0:
                #mark measure
                elem.attrib["_mm"] = str(measure_to_mark) #value is dummy, never used
                measure_to_mark -= 1
            if elem.attrib.get("len"):
                measure_to_mark = int(elem.find("multiMeasureRest").text) -1


def cleanup_mm_rests(staff):
    """
    Go through entire staff, remove any "_mm" attributes
    """
    for elem in staff:
        if elem.attrib.get("_mm") is not None:
            del elem.attrib["_mm"]
    

def add_rehearsal_mark_line_breaks(staff):
    """
    Go through each measure in the score. If there is a rehearsal mark in measure n, add a line break to measure n-1.
    If measure n-1 has a "_mm" attribute, go backwards until the first measure in the chain, and also add a line break.

    add a line break by calling `_add_line_break_to_measure()`
    """
    for i in range(len(staff)):
        elem = staff[i]
        if elem.tag != "Measure":
            continue  # could be vbox or smth

        voice = elem.find("voice")
        if voice is None:
            continue  # Skip if no voice tag

        if voice.find("RehearsalMark") is not None:
            if i > 0:  
                prev_elem = staff[i - 1]
                _add_line_break_to_measure(prev_elem)

            # If part of mm rest, add to start of mm rest as well
            if prev_elem.attrib.get("_mm") is not None:
                print("Added to mm rest")
                for j in range(i - 1, -1, -1):  # Start at i-1 and go backward
                    if staff[j].attrib.get("len") is not None:
                        print(f"Adding line break to measure at index {j}")
                        _add_line_break_to_measure(staff[j])
                        break



def main(mscx_path):
    try:
        parser = ET.XMLParser()
        tree = ET.parse(mscx_path, parser)
        root = tree.getroot()
        score = root.find("Score")
        if score is None:
            raise ValueError("No <Score> tag found in the XML.")

        staves = score.findall("Staff")

        for staff in staves:
            prep_mm_rests(staff)
            add_rehearsal_mark_line_breaks(staff)
            cleanup_mm_rests(staff)

        
        out_path = mscx_path.replace("test-data", "test-data-copy")

        with open(out_path, "wb") as f:
            ET.indent(tree, space="  ", level=0)
            tree.write(f, encoding="utf-8", xml_declaration=True)
        print(f"Output written to {out_path}")

    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        sys.exit(1)
    # except ET.XMLSyntaxError as e:
    #     print(f"Error: Failed to parse XML from '{mscx_path}': {e}")
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"Unhandled error: {e}")
    #     sys.exit(1)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python part_formatter.py <mscx file>")
        sys.exit(1)

    main(sys.argv[1])
