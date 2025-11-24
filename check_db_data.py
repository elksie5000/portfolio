import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def check_data():
    tables = ["sexes_time_series_archive", "sexes_summary_archive", "regions_time_series_archive"]
    
    for table in tables:
        print(f"\n--- Checking {table} ---")
        try:
            response = supabase.table(table).select("*").limit(5).execute()
            data = response.data
            print(f"Count: {len(data)} (showing first 5)")
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_data()
