import ms_secrets

from prompts import Prompts


# def remove_confusing_measures(tree):
#     ghost_measures = []
#     for 



# def add_back_confusing_measures()


test = False

if __name__ == "__main__":


    import sys
    import xml.etree.ElementTree as ET
    import requests

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
        if score is not None:
            for staff in score.findall("Staff"):
                staves.append(staff)
        # Convert XML to string

        data_prompts = []
        for staff in staves:
            data_prompts.append(str(ET.tostring(staff)))

        with open("temp_xml.xml", "w", encoding="utf-8") as file:
            file.write(data_prompts[0])

        if test:
            score = root.find("Score")
            if score is not None:
                for staff in score.findall("Staff"):
                    for measure in staff.findall("Measure"):
                        print(measure.attrib)
            else:
                print("here")




        else:
            from google import genai
            #genai.configure

            p = Prompts()
            
            client = genai.Client(api_key=ms_secrets.GEMINI_KEY)
            payload = {
                "prompt": p.alt_generate(),
                "data": data_prompts[0]
            }

            import json

            response = client.models.generate_content(
                contents=json.dumps(payload),
                model="gemini-2.5-flash-lite-preview-06-17"
            )
            
            # Handle the response

            print("Response from Google Gemini!")

            #parse response back into xml
            try:
                response_xml = ET.fromstring(response.text)
                # Find the staff in score that matches response_xml (by id or index)
                if score is not None:
                    # Assume Staff elements have an 'id' attribute to match
                    response_staff_id = response_xml.attrib.get('id')
                    replaced = False
                    for i, staff in enumerate(score.findall("Staff")):
                        if staff.attrib.get('id') == response_staff_id:
                            score.remove(staff)
                            score.insert(i, response_xml)
                            replaced = True
                            break
                    if not replaced:
                        # If not found, just append
                        score.append(response_xml)
                    
                    with open("out.mscx", "w", encoding="utf-8") as file:
                        tree.write(file, encoding="unicode", xml_declaration=True)

                else:
                    print("No <Score> element found in XML.")

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