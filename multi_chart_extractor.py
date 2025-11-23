import re
import json
import os

def extract_spec(file_path):
    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find the spec variable
    # var spec = { ... };
    match = re.search(r'var\s+spec\s*=\s*(\{.*?\});', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return None
    else:
        print(f"No spec found in {file_path}")
        return None

def process_charts():
    charts = [
        {
            "file": "line_charts_sexes.html",
            "data_output": "frontend/src/data/sexes_time_series.json",
            "spec_output": "frontend/src/data/line_chart_spec.json",
            "data_key": "datasets" # Data is in datasets object
        },
        {
            "file": "donut_sexes.html",
            "data_output": "frontend/src/data/sexes_summary.json",
            "spec_output": "frontend/src/data/donut_chart_spec.json",
            "data_key": "datasets"
        },
        {
            "file": "regions_dropdown.html",
            "data_output": "frontend/src/data/regions_time_series.json",
            "spec_output": "frontend/src/data/regions_chart_spec.json",
            "data_key": "datasets"
        }
    ]

    for chart in charts:
        spec = extract_spec(chart["file"])
        if not spec:
            continue

        # Extract Data
        data = []
        if "datasets" in spec:
            # Usually datasets is a dict where keys are random strings "data-..."
            # We take the first value found
            for key, values in spec["datasets"].items():
                data = values
                break
        elif "data" in spec and "values" in spec["data"]:
            data = spec["data"]["values"]
        
        # Save Data
        os.makedirs(os.path.dirname(chart["data_output"]), exist_ok=True)
        with open(chart["data_output"], 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Saved data to {chart['data_output']} ({len(data)} records)")

        # Clean Spec (remove data)
        if "datasets" in spec:
            del spec["datasets"]
        if "data" in spec:
            # If data was named, keep the name but remove values if present (though usually with datasets it's just a name ref)
            if "values" in spec["data"]:
                del spec["data"]["values"]
            # We will inject data via URL or values at runtime, so we can set data to empty or name
            spec["data"] = {"name": "table"} # Standardize

        # Save Spec
        with open(chart["spec_output"], 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2)
        print(f"Saved spec to {chart['spec_output']}")

if __name__ == "__main__":
    process_charts()
