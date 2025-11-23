import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found.")
    exit(1)

supabase: Client = create_client(url, key)

def clean_float(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None

def import_sexes_time_series():
    json_path = "frontend/src/data/sexes_time_series.json"
    table_name = "sexes_time_series_archive"
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print(f"Importing {len(data)} records into {table_name}...")
    
    # Clean data if necessary
    cleaned_data = []
    for item in data:
        cleaned_data.append({
            "year": item.get("year"),
            "adm_per_male": clean_float(item.get("adm_per_male")),
            "adm_per_female": clean_float(item.get("adm_per_female")),
            "adm_per_male_rebased": clean_float(item.get("adm_per_male_rebased")),
            "adm_per_female_rebased": clean_float(item.get("adm_per_female_rebased")),
            "admissions_total": int(item.get("admissions_total", 0))
        })

    try:
        supabase.table(table_name).insert(cleaned_data).execute()
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Ensure table {table_name} exists.")

def import_sexes_summary():
    json_path = "frontend/src/data/sexes_summary.json"
    table_name = "sexes_summary_archive"
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print(f"Importing {len(data)} records into {table_name}...")
    
    cleaned_data = []
    for item in data:
        cleaned_data.append({
            "gender": item.get("Gender"),
            "admissions": clean_float(item.get("Admissions")),
            "percentage": clean_float(item.get("Percentage"))
        })

    try:
        supabase.table(table_name).insert(cleaned_data).execute()
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Ensure table {table_name} exists.")

def import_regions_time_series():
    json_path = "frontend/src/data/regions_time_series.json"
    table_name = "regions_time_series_archive"
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print(f"Importing {len(data)} records into {table_name}...")
    
    cleaned_data = []
    for item in data:
        cleaned_data.append({
            "region": item.get("region"),
            "major_region": item.get("major_region"),
            "year": item.get("year"),
            "adm_per_100k": clean_float(item.get("adm_per_100_000_all")),
            "admissions_total": int(item.get("admissions_total", 0))
        })

    # Batch insert
    batch_size = 100
    for i in range(0, len(cleaned_data), batch_size):
        batch = cleaned_data[i:i+batch_size]
        try:
            supabase.table(table_name).insert(batch).execute()
            print(f"Inserted batch {i//batch_size + 1}")
        except Exception as e:
            print(f"Error inserting batch {i//batch_size + 1}: {e}")
            print(f"Ensure table {table_name} exists.")
            return

if __name__ == "__main__":
    import_sexes_time_series()
    import_sexes_summary()
    import_regions_time_series()
