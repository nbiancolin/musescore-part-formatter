import sys
import xml.etree.ElementTree as ET

#create a line break element
LINE_BREAK = ET.Element("LayoutBreak")
temp = ET.SubElement(LINE_BREAK, "subtype")
temp.text = "line"

NUM_MEASURES_PER_LINE = 6

def _make_line_break():
    lb = ET.Element("LayoutBreak")
    subtype = ET.SubElement(lb, "subtype")
    subtype.text = "line"
    return lb

def _make_page_break():
    pb = ET.Element("LayoutBreak")
    subtype = ET.SubElement(pb, "subtype")
    subtype.text = "page"
    return pb

def _make_double_bar():
    db = ET.Element("BarLine")
    subtype = ET.SubElement(db, "subtype")
    subtype.text = "double"
    return db

def _add_line_break_to_measure(measure):
    index = 0
    for elem in measure:
        if elem.tag == "voice":
            break
        index += 1
    measure.insert(index, _make_line_break())

def _add_page_break_to_measure(measure):
    #if line break already there, replace with a page break
    if measure.find("LayoutBreak"):
        measure.find("LayoutBreak").find("subtype").text = "page"
        return
    
    print("added a page break to a bar that did not have a line break!")
    index = 0
    for elem in measue:
        if elem.tag == "voice":
            break
        index += 1

    measure.insert(index, _make_page_break())


def _add_double_bar_to_measure(measure):
    voice = measure.find("voice")
    index = 0
    for _ in voice:
        index += 1
    measure.insert(index, _make_double_bar())


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
    

def add_rehearsal_mark_double_bars(staff):
    """
    Go through each measure in the score. If there is a rehearsal mark in measure n, add a line break to measure n-1.
    If measure n-1 has a "_mm" attribute, go backwards until the first measure in the chain, and also add a line break.
    """
    for i in range(len(staff)):
        elem = staff[i]
        if elem.tag != "Measure":
            continue

        voice = elem.find("voice")
        if voice is None:
            continue #sanity check

        if voice.find("RehearsalMark") is not None:
            if i > 0:
                prev_elem = staff[i -1]
                _add_double_bar_to_measure(prev_elem)

                if prev_elem.attrib.get("_mm") is not None:
                    for j in range(i -1, -1, -1):
                        if staff[j].attrib.get("len") is not None:
                            print(f"adding double bar to rehearsal mark at bar {j}")
                            _add_double_bar_to_measure(staff[j])



#TODO: Should be add line breaks to double bar
def add_double_bar_line_breaks(staff):
    """
    Go through each measure in the score. If there is a double bar on measure n, add a line break to measure n-1.
    If measure n-1 has a "_mm" attribute, go backwards until the first measure in the chain, and also add a line break.

    add a line break by calling `_add_line_break_to_measure()`

    Additionally, set it up s.t. if there are 2 multimeasure rests together, only keep the second line break, remove the first one
        TODO: This should onlt do this if the entire section before the next rehearsal mark is a multimeasure rest
    """
    prev_added_line_break = None
    for i in range(len(staff)):
        elem = staff[i]
        if elem.tag != "Measure":
            continue  # could be vbox or smth

        voice = elem.find("voice")
        if voice is None:
            continue  # Skip if no voice tag
        
        if voice.find("BarLine") is not None:
            if i > 0:  
                prev_elem = staff[i]
                _add_line_break_to_measure(prev_elem)

            # If part of mm rest, add to start of mm rest as well
            if prev_elem.attrib.get("_mm") is not None:
                for j in range(i - 1, -1, -1):  # Start at i-1 and go backward
                    if staff[j].attrib.get("len") is not None:
                        print(f"Adding (double bar) Line Break to measure at index {j}")
                        _add_line_break_to_measure(staff[j])
                        temp_prev_added = (prev_elem, staff[j])

                        #check if we can remove a previous one
                        if prev_added_line_break:
                            temp_prev_added = None
                            for e in prev_added_line_break:
                                e.remove(LINE_BREAK)

                        prev_added_line_break = temp_prev_added
                        break

        else:
            if elem.attrib.get("_mm") is None:
                prev_added_line_break = None


def add_regular_line_breaks(staff):
    """
    We want to add a line break every `NUM_MEASURES_PER_LINE` measures. 
    This does not include multi measure rests, these should be ignored. 
    """
    i = 0
    for elem in staff:
        if elem.tag != "Measure":
            print("Non measure tag encountered")
            continue
    

        if elem.find("voice") is not None and elem.find("voice").find("RehearsalMark") is not None:
            i = 0

        if elem.attrib.get("_mm") is not None:
            if i > 0:
                #TODO: add line break to bar before
                print("Could have added a line break") #Manual testing indicates otherwise ...
            i = 0
        else:
            if i == (NUM_MEASURES_PER_LINE -1) and elem.find("LayoutBreak") is None:
                print("Adding Regular Line Break")
                _add_line_break_to_measure(elem)
                i = 0
            else:
                i += 1


def add_page_breaks(staff):
    """
    Want to vertically space music to make it easier to read. Should be 7-9 lines per page (7-8 for the first one, 8-9 for the next one)
    - When picking between closer or farther:
        - if there is a multimeasure rest after a line break, make that one the page break
        - if the page break would put a rehearsal mark on a new page, do that
    """
    num_line_breaks_per_page = 0
    first_page = True

    first_elem, second_elem = None, None
    first_index, second_index = -1, -1
    for i in range(len(staff)):
        elem = staff[i]
        if first_page:
            cutoff = 7
        else:
            cutoff = 8

        if elem.tag != "Measure":
            continue #non-measure element found

        if elem.find("Voice") is not None and elem.find("voice").find("LayoutBreak") and not elem.attrib.get("_mm"):
            num_line_breaks_per_page += 1


        if num_line_breaks_per_page == cutoff and first_elem is None:
            first_elem = elem
            first_index = i
            num_line_breaks_per_page -= 1
            continue

        if num_line_breaks_per_page == cutoff and first_elem is not None:
            second_elem = elem
            second_index = i
            first_page = False

            #add page break based on criteria
            #first criteria
            next_elem = staff[second_index +1]
            first_next_elem = staff[first_index +1]
            if next_elem.find("voice").find("RehearsalMark") is not None:
                _add_page_break_to_measure(second_elem)
            elif first_next_elem.find("voice").find("RehearsalMark") is not None:
                _add_page_break_to_measure(second_elem)
            else:
                #second criteria
                if elem.find("Barline") is not None:
                    print("adding page break")
                    _add_page_break_to_measure(first_elem)
                else:
                    _add_page_break_to_measure(second_elem)
                
            num_line_breaks_per_page = 0
            first_elem = None
            second_elem = None
        


def final_pass_through(staff):
    """
    Adjusts poorly balanced lines. If a line has only 2 measures and the previous has 4+:
    - If prev has 4: remove the break before it.
    - If prev has >4: remove the break and move it to the midpoint.
    """
    line_lengths = []
    current_line = []
    in_mm = False

    for elem in staff:
        if elem.tag != "Measure":
            continue

        if elem.attrib.get("_mm") is not None:
            if in_mm:
                continue  # skip repeated mm rest measures
            in_mm = True
        else:
            in_mm = False

        current_line.append(elem)

        if elem.find("LayoutBreak") is not None:
            line_lengths.append(current_line)
            current_line = []

    if current_line:
        line_lengths.append(current_line)

    i = 1
    while i < len(line_lengths):
        this_line = line_lengths[i]
        prev_line = line_lengths[i - 1]

        if len(this_line) <= 2:
            if len(prev_line) == 4:
                # remove break at end of previous line
                for elem in reversed(prev_line):
                    lb = elem.find("LayoutBreak")
                    if lb is not None:
                        elem.remove(lb)
                        break
            elif len(prev_line) > 4:
                # remove existing line break
                for elem in reversed(prev_line):
                    lb = elem.find("LayoutBreak")
                    if lb is not None:
                        elem.remove(lb)
                        break
                # insert new one in midpoint
                split_index = len(prev_line) // 2
                _add_line_break_to_measure(prev_line[split_index])
        i += 1


        

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
            add_rehearsal_mark_double_bars(staff)
            add_double_bar_line_breaks(staff)
            add_regular_line_breaks(staff)
            cleanup_mm_rests(staff)
            final_pass_through(staff)

        
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
