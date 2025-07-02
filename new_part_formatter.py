import sys
import json
from lxml import etree as ET
from google import genai

import ms_secrets
from prompts import Prompts


def prepare_prompts(staves):
    return [ET.tostring(staff, encoding="unicode") for staff in staves]


def generate_modified_staves(data_prompts, prompt_template):
    new_staves = []
    client = genai.Client(api_key=ms_secrets.GEMINI_KEY)

    for data_prompt in data_prompts:
        payload = {
            "prompt": prompt_template,
            "data": data_prompt
        }
        response = client.models.generate_content(
            contents=json.dumps(payload),
            model="gemini-2.5-flash-lite-preview-06-17"
        )

        try:
            new_staff = ET.fromstring(response.text.encode("utf-8"))
            new_staves.append(new_staff)
        except ET.XMLSyntaxError:
            print("Warning: Invalid XML received from Gemini. Saving raw output.")
            with open("out_invalid.xml", "w", encoding="utf-8") as f:
                f.write(response.text)
            sys.exit(1)

    return new_staves


def replace_staves_in_score(score, new_staves):
    original_staves = score.findall("Staff")
    if len(original_staves) != len(new_staves):
        print("Warning: Mismatch between original and new staves. Proceeding with replacement.")

    for i, new_staff in enumerate(new_staves):
        if i < len(original_staves):
            original = original_staves[i]
            # Clear original content
            original.clear()
            # Copy attributes
            original.attrib.clear()
            original.attrib.update(new_staff.attrib)
            # Copy children
            for child in new_staff:
                original.append(child)
        else:
            score.append(new_staff)


def main(mscx_path):
    try:
        parser = ET.XMLParser(remove_blank_text=False)
        tree = ET.parse(mscx_path, parser)
        root = tree.getroot()
        score = root.find("Score")
        if score is None:
            raise ValueError("No <Score> tag found in the XML.")

        staves = score.findall("Staff")
        data_prompts = prepare_prompts(staves)

        # Optional debug: write the first extracted staff
        with open("temp_xml.xml", "w", encoding="utf-8") as f:
            f.write(data_prompts[0])

        prompts = Prompts()
        new_staves = generate_modified_staves(data_prompts, prompts.alt_generate())

        with open("temp_xml.xml", "w", encoding="utf-8") as f:
            f.write(ET.tostring(new_staves[0], encoding="unicode", pretty_print=True))

        replace_staves_in_score(score, new_staves)

        with open("out.mscx", "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)
        print("Output written to out.mscx")

    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        sys.exit(1)
    except ET.XMLSyntaxError as e:
        print(f"Error: Failed to parse XML from '{mscx_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unhandled error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python part_formatter.py <mscx file>")
        sys.exit(1)

    main(sys.argv[1])
