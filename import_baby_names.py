import csv
import os
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

def import_baby_names():
    file_path = "Baby Names.csv"
    table_name = "baby_names_archive"
    
    print(f"Reading {file_path}...")
    
    # Dictionary to aggregate data: (name, sex, year) -> {count, rank}
    data_map = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # CSV Columns: ['', 'Name', 'Gender', 'Value', 'Year', 'Measure']
            
            count = 0
            for row in reader:
                count += 1
                if count % 100000 == 0:
                    print(f"Processed {count} rows...")
                
                name = row['Name']
                gender = row['Gender'] # 'boy' or 'girl'
                year = int(row['Year'])
                value = int(row['Value']) if row['Value'] else 0
                measure = row['Measure'] # 'Count' or 'Rank'
                
                # Normalize sex
                sex = 'M' if gender.lower() == 'boy' else 'F'
                
                key = (name, sex, year)
                
                if key not in data_map:
                    data_map[key] = {'count': None, 'rank': None}
                
                if measure == 'Count':
                    data_map[key]['count'] = value
                elif measure == 'Rank':
                    data_map[key]['rank'] = value

        print(f"Aggregation complete. Found {len(data_map)} unique records.")
        
        # Prepare for bulk insert
        records = []
        for (name, sex, year), values in data_map.items():
            records.append({
                "name": name,
                "sex": sex,
                "year": year,
                "count": values['count'],
                "rank": values['rank']
            })
        
        # Batch insert
        batch_size = 1000
        total_batches = (len(records) + batch_size - 1) // batch_size
        
        print(f"Starting upload of {len(records)} records in {total_batches} batches...")
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            try:
                supabase.table(table_name).insert(batch).execute()
                if (i // batch_size) % 10 == 0:
                    print(f"Uploaded batch {i//batch_size + 1}/{total_batches}")
            except Exception as e:
                print(f"Error uploading batch {i//batch_size + 1}: {e}")
                # Optional: break or continue? Continue might result in partial data.
                # For now, let's just print error.
        
        print("Upload complete.")

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_baby_names()
