import re
import json
import os

def extract_panels(input_file, output_file):
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the JSON spec
    # Looking for: var spec = { ... };
    # We can use a regex to capture everything between "var spec = " and the matching closing brace/semicolon.
    # Since it might be multi-line and complex, let's find the start and assume it ends before the next script tag or at the end of the script block.
    
    match = re.search(r'var spec = ({.*});', content, re.DOTALL)
    if not match:
        # Try without semicolon if it was missed
        match = re.search(r'var spec = ({.*})', content, re.DOTALL)
    
    if not match:
        print("Could not find 'var spec = ...' in the file.")
        return

    json_str = match.group(1)
    
    # The regex might capture too much if there is code after the semicolon.
    # A safer way for a large JSON blob in a file is to find the start index, count braces to find the end.
    start_marker = "var spec = "
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Start marker not found.")
        return
    
    start_idx += len(start_marker)
    
    # Simple brace counter to find the end of the JSON object
    brace_count = 0
    json_end_idx = start_idx
    found_start = False
    
    for i, char in enumerate(content[start_idx:], start=start_idx):
        if char == '{':
            brace_count += 1
            found_start = True
        elif char == '}':
            brace_count -= 1
        
        if found_start and brace_count == 0:
            json_end_idx = i + 1
            break
            
    json_str = content[start_idx:json_end_idx]
    
    try:
        full_spec = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return

    print("Successfully parsed full Vega-Lite spec.")
    
    datasets = full_spec.get('datasets', {})
    panels = []

    # Helper to create a standalone spec
    def create_panel_spec(source_spec):
        new_spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": source_spec.get("title", "Untitled Chart"),
            "mark": source_spec.get("mark"),
            "encoding": source_spec.get("encoding"),
            "title": source_spec.get("title"),
            "width": "container", # Responsive width
            "height": 300,
            "config": {
                "background": "transparent",
                "view": {"stroke": "transparent"},
                "axis": {
                    "domain": False,
                    "tickColor": "#4A7C59", # brand-sage
                    "labelColor": "#4A7C59",
                    "titleColor": "#4A7C59",
                    "gridColor": "#e5e7eb"
                },
                "legend": {
                    "labelColor": "#4A7C59",
                    "titleColor": "#4A7C59"
                },
                "title": {
                    "color": "#4A7C59",
                    "font": "Inter",
                    "fontSize": 16,
                    "anchor": "start"
                }
            }
        }
        
        # Handle Layered charts
        if "layer" in source_spec:
            new_spec.pop("mark", None)
            new_spec.pop("encoding", None)
            new_spec["layer"] = source_spec["layer"]
        
        # Resolve Data
        if "data" in source_spec and "name" in source_spec["data"]:
            data_name = source_spec["data"]["name"]
            if data_name in datasets:
                new_spec["data"] = {"values": datasets[data_name]}
        
        return new_spec

    # Navigate the specific structure of this file
    # Root -> vconcat
    vconcat = full_spec.get("vconcat", [])
    
    if len(vconcat) > 0:
        # 1. Deaths by date
        panels.append(create_panel_spec(vconcat[0]))
        
        if len(vconcat) > 1:
            # hconcat container
            hconcat = vconcat[1].get("hconcat", [])
            if len(hconcat) > 0:
                # 2. Death by rank (Layered)
                panels.append(create_panel_spec(hconcat[0]))
                
                if len(hconcat) > 1:
                    # vconcat container
                    inner_vconcat = hconcat[1].get("vconcat", [])
                    if len(inner_vconcat) > 0:
                        # 3. Top 10 deaths by surname
                        panels.append(create_panel_spec(inner_vconcat[0]))
                    if len(inner_vconcat) > 1:
                        # 4. Death by age
                        panels.append(create_panel_spec(inner_vconcat[1]))

    print(f"Extracted {len(panels)} panels.")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(panels, f, indent=2)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    input_path = "war_dead_panels.html"
    output_path = "frontend/src/data/war_dead_panels.json"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
    else:
        extract_panels(input_path, output_path)
