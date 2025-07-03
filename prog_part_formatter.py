import ms_secrets

from prompts import Prompts

import sys
import xml.etree.ElementTree as ET
import requests
import json
from google import genai


stashed_measures = {}

# def remove_multimeasure_rest_measures(score):
#     staves = []
#     stashed_per_staff = []
#     for staff in score.findall("Staff"):
#         staves.append(staff)


#         measures = list(staff.findall("Measure"))
#         i = 0
#         while i < len(measures):
#             measure = measures[i]
#             len_attr = measure.attrib.get("len")
#             if len_attr is not None:
#                 #stash this measure
#                 to_stash = measures[i]
#                 stashed.append(to_stash)

                

#                 num1, num2 = len_attr.split("/")
#                 n = int(num1) // int(num2)
#                 stashed = []
#                 for j in range(1, n + 1):
#                     if i + j < len(measures):
#                         to_stash = measures[i + j]
#                         stashed.append(to_stash)
#                 # Remove stashed measures from staff (iterate over a copy)
#                 for m in stashed:
#                     staff.remove(m)
#                 stashed_measures[i] = stashed
#                 i += n  # Skip the stashed measures
#             i += 1
#         stashed_per_staff.append(stashed_measures)
#     return staves, stashed_per_staff

# def remove_confusing_measures(score):
#     staves = []
#     stashed_per_staff = []
#     for staff in score.findall("Staff"):
#         staves.append(staff)


#         measures = list(staff.findall("Measure"))
#         i = 0
#         while i < len(measures):
#             measure = measures[i]
#             len_attr = measure.attrib.get("len")
#             if len_attr is not None:
#                 num1, num2 = len_attr.split("/")
#                 n = int(num1) // int(num2)
#                 stashed = []
#                 for j in range(1, n + 1):
#                     if i + j < len(measures):
#                         to_stash = measures[i + j]
#                         stashed.append(to_stash)
#                 # Remove stashed measures from staff (iterate over a copy)
#                 for m in stashed:
#                     staff.remove(m)
#                 stashed_measures[i] = stashed
#                 i += n  # Skip the stashed measures
#             i += 1
#         stashed_per_staff.append(stashed_measures)
#     return staves, stashed_per_staff



# def add_back_confusing_measures(staves, stashed_per_staff):
#     for staff, stashed_measures in zip(staves, stashed_per_staff):
#         # Insert stashed measures at the correct position, sorted ascending
#         for idx in stashed_measures.keys():
#             stashed = stashed_measures[idx]
#             # Insert each measure in order, incrementing the index each time
#             insert_pos = idx +2
#             for m in stashed:
#                 staff.insert(insert_pos, m)
#                 insert_pos += 1
#     return staves


def add_line_break_before_rehearsal_mark(staves):
    Layout_break_elem = ET.Element("LayoutBreak")
    temp = ET.SubElement(Layout_break_elem, "subtype")
    temp.text = "line"

    for staff in staves:
        measures = staff.findall("Measure")
        i = 0
        for i in range(1, len(measures)):
            for elem in measures[i]:
                if elem.tag == "voice":
                    for music_elem in elem:
                        #check if a rehearsal mark is present:
                        if music_elem.tag == "RehearsalMark":
                            #add a line break before it

test = False

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python part_formatter.py <mscx file name>")
        sys.exit(1)

    mscx_path = sys.argv[1]
    
    try:
        # Load and parse the XML file
        tree = ET.parse(mscx_path)
        root = tree.getroot()

        #only pass Gemini the STAFF tag
        staves = []
        score = root.find("Score")

        staves, stashed_per_staff = remove_confusing_measures(score)
        

        data_prompts = []
        for staff in staves:
            data_prompts.append(ET.tostring(staff, encoding='utf8').decode('utf-8'))

        
        with open("temp_xml.xml", "w", encoding="utf-8") as file:
            file.write(data_prompts[0])

        p = Prompts()
        new_staves = []
        for data_prompt in data_prompts:
            client = genai.Client(api_key=ms_secrets.GEMINI_KEY)
            payload = {
                "prompt": p.alt_generate(),
                "data": data_prompts[0]
            }

            

            response = client.models.generate_content(
                contents=json.dumps(payload),
                model="gemini-2.5-flash-lite-preview-06-17"
            )

            #add response back to new
            new_staves.append(ET.fromstring(response.text))
        # Handle the response

        print("Response from Google Gemini!")

        #parse response back into xml
        try:
            #write the code
            staves = add_back_confusing_measures(new_staves, stashed_per_staff)

            for staff in staves:
                #replace each measure in score with the measure with the same eid
                for measure in staff.findall("Measure"):
                    measure_id = measure.attrib.get('eid')
                    if measure_id:
                        # Find the corresponding measure in the score
                        existing_measure = score.find(f".//Measure[@eid='{measure_id}']")
                        if existing_measure is not None:
                            # Replace the existing measure with the new one
                            score.remove(existing_measure)
                            score.append(measure)
                        else:
                            # If not found, just append the new measure
                            score.append(measure)





            # response_xml = staves[0]
            # # Find the staff in score that matches response_xml (by id or index)
            # # Assume Staff elements have an 'id' attribute to match
            # response_staff_id = response_xml.attrib.get('id')
            # replaced = False
            # for i, staff in enumerate(score.findall("Staff")):
            #     if staff.attrib.get('id') == response_staff_id:
            #         score.remove(staff)
            #         score.insert(i, response_xml)
            #         replaced = True
            #         break
            #     #modify xml file such that the measure tags are the last ones
            #     for measure in list(staff.findall("Measure")):
            #         staff.remove(measure)
            #         staff.append(measure)

            # if not replaced:
            #     # If not found, just append
            #     #score.append(response_xml)
            #     print("Warning: No matching staff found in the score to replace with the response.")
            
            with open("out.mscx", "w", encoding="utf-8") as file:
                tree.write(file, encoding="unicode", xml_declaration=True)


        except ET.ParseError:
            print("GPT Sentback the wrong thing, writing to file")
            with open("out.mscx", "w", encoding="utf-8") as file:
                file.write(response.text)




    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        sys.exit(1)
    except ET.ParseError:
        print(f"Error: Failed to parse the XML file '{mscx_path}'.")
        sys.exit(1)