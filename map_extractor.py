import re
import json
import os

def extract_map_data(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract Circles: var circle_id = L.circle([lat, lon], ...
    # Regex to capture ID, Lat, Lon
    circle_pattern = re.compile(r'var\s+(circle_[a-f0-9]+)\s*=\s*L\.circle\(\s*\[([\d.-]+),\s*([\d.-]+)\]', re.MULTILINE)
    circles = {}
    for match in circle_pattern.finditer(content):
        c_id, lat, lon = match.groups()
        circles[c_id] = {'lat': float(lat), 'lon': float(lon)}
    
    print(f"Found {len(circles)} circles.")

    # 2. Extract HTML content: var html_id = $(`<div ...>...</div>`)[0];
    # We use backticks in the file.
    # Regex to capture ID and Content. Content is inside `...`
    html_pattern = re.compile(r'var\s+(html_[a-f0-9]+)\s*=\s*\$\(`([\s\S]*?)`\)\[0\];', re.MULTILINE)
    htmls = {}
    for match in html_pattern.finditer(content):
        h_id, html_content = match.groups()
        htmls[h_id] = html_content

    print(f"Found {len(htmls)} HTML blocks.")

    # 3. Extract Popup to HTML mapping: popup_id.setContent(html_id);
    popup_content_map = {}
    popup_content_pattern = re.compile(r'(popup_[a-f0-9]+)\.setContent\((html_[a-f0-9]+)\);')
    for match in popup_content_pattern.finditer(content):
        p_id, h_id = match.groups()
        popup_content_map[p_id] = h_id

    # 4. Extract Circle to Popup mapping: circle_id.bindPopup(popup_id)
    circle_popup_map = {}
    bind_pattern = re.compile(r'(circle_[a-f0-9]+)\.bindPopup\((popup_[a-f0-9]+)\)')
    for match in bind_pattern.finditer(content):
        c_id, p_id = match.groups()
        circle_popup_map[c_id] = p_id

    # Combine data
    results = []
    
    # Regex for parsing the HTML content
    # <h3>Name</h3>
    name_pattern = re.compile(r'<h3>(.*?)</h3>')
    # <p>There are X men commemorated here.</p>
    count_pattern = re.compile(r'<p>There are (\d+) men commemorated here\.</p>')

    for c_id, coords in circles.items():
        if c_id in circle_popup_map:
            p_id = circle_popup_map[c_id]
            if p_id in popup_content_map:
                h_id = popup_content_map[p_id]
                if h_id in htmls:
                    raw_html = htmls[h_id]
                    
                    # Extract metadata from HTML
                    name_match = name_pattern.search(raw_html)
                    cemetery_name = name_match.group(1) if name_match else "Unknown Cemetery"
                    
                    count_match = count_pattern.search(raw_html)
                    num_commemorated = int(count_match.group(1)) if count_match else 0
                    
                    results.append({
                        "cemetery_name": cemetery_name,
                        "coordinates": [coords['lat'], coords['lon']],
                        "bio_html": raw_html,
                        "num_commemorated": num_commemorated
                    })

    print(f"Extracted {len(results)} data points.")

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    input_path = "war_dead.html"
    output_path = "frontend/src/data/war_dead_points.json"
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
    else:
        extract_map_data(input_path, output_path)
