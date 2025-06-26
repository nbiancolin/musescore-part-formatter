import ms_secrets

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
        
        # Convert XML to string
        xml_string = ET.tostring(root, encoding='unicode')

        from google import genai
        #genai.configure
        
        client = genai.Client(api_key=GEMINI_KEY)
        payload = {
            "prompt": "This is a Musescore mscx file. Please add layout (line) breaks such that no given line is longer than 8 measures, or shorter than 4 measures. To add a line break, add Add a double bar line before all rehearsal marks. Only return the new, formatted XML file",
            "data": xml_string
        }

        import json

        response = client.models.generate_content(
            contents=json.dumps(payload),
            model="gemini-2.5-flash-lite-preview-06-17"
        )
        
        # Handle the response

        print("Response from Google Gemini:")

        with open("out.mscx", "w", encoding="utf-8") as file:
            file.write(response.text)

    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        sys.exit(1)
    except ET.ParseError:
        print(f"Error: Failed to parse the XML file '{mscx_path}'.")
        sys.exit(1)