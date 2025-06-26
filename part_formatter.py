


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
        
        # Prepare the API request
        api_url = "https://api.google.com/gemini"  # Replace with the actual API endpoint
        headers = {
            "Authorization": "Bearer AIzaSyAdh0Ko2I4K8JGqjcnTyQInPI5OKL24qOw",  # Replace with your API key
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": "This is a Musescore mscx file. Please add layout (line) breaks such that no given line is longer than 8 measures, or shorter than 4 measures. Add a double bar line before all rehearsal marks. Only return the new, formatted XML file",
            "data": xml_string
        }
        
        # Send the request
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Handle the response
        if response.status_code == 200:
            print("Response from Google Gemini:")
            print(response.json())  # Assuming the response is in JSON format

            with open("out.mscx", "w", encoding="utf-8") as file:
                file.write(response.json())
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)


    except FileNotFoundError:
        print(f"Error: File '{mscx_path}' not found.")
        sys.exit(1)
    except ET.ParseError:
        print(f"Error: Failed to parse the XML file '{mscx_path}'.")
        sys.exit(1)