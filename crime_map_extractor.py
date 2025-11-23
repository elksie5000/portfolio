import re
import json
import os

def extract_crime_data(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find circles
    # var circle_1 = L.circle([52.768641, -1.954664], 100, {
    #                       color: '#cab2d6',
    #                       fillColor: '#cab2d6',
    #                       fillOpacity: 0.6
    #                       });
    # circle_1.bindPopup("<h2>Violence and sexual offences</h2><p>On or near Pump Lane</p>");

    # We need to capture:
    # 1. Variable name (to link circle to popup)
    # 2. Coordinates
    # 3. Color (optional)
    # 4. Popup content

    # Pattern for circle definition
    # Captures: var_name, lat, lon, color
    circle_pattern = re.compile(r'var\s+(\w+)\s*=\s*L\.circle\(\s*\[([\d.-]+),\s*([\d.-]+)\],\s*\d+,\s*\{.*?color:\s*[\'"](#[\w\d]+)[\'"]', re.DOTALL)
    
    # Pattern for popup binding
    # Captures: var_name, crime_type, location
    popup_pattern = re.compile(r'(\w+)\.bindPopup\("<h2>(.*?)</h2><p>(.*?)</p>"\)', re.DOTALL)

    circles = {}
    
    # Find all circles
    for match in circle_pattern.finditer(content):
        var_name = match.group(1)
        lat = float(match.group(2))
        lon = float(match.group(3))
        color = match.group(4)
        
        circles[var_name] = {
            "coordinates": [lat, lon],
            "color": color
        }

    print(f"Found {len(circles)} circles.")

    results = []
    
    # Find all popups and link to circles
    for match in popup_pattern.finditer(content):
        var_name = match.group(1)
        crime_type = match.group(2)
        location = match.group(3)
        
        if var_name in circles:
            circle_data = circles[var_name]
            results.append({
                "crime_type": crime_type,
                "location": location,
                "coordinates": circle_data["coordinates"],
                "original_color": circle_data["color"]
            })

    print(f"Extracted {len(results)} crime records.")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    input_path = "crime_map.html"
    output_path = "frontend/src/data/crime_data.json"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
    else:
        extract_crime_data(input_path, output_path)
