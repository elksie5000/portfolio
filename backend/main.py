import os
import random
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default
    "http://127.0.0.1:5173",
    "https://portfolio-three-livid-76.vercel.app", # Vercel Production
    "*" # Fallback
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow ALL origins to fix CORS issues
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Setup
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Optional[Client] = None

if url and key:
    supabase = create_client(url, key)
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found. Database logging will be disabled.")

class Question(BaseModel):
    question: str

@app.post("/api/submit-question")
async def submit_question(q: Question):
    answer = random.choice(["Yes", "No"])
    
    # Log to Supabase if configured, otherwise log to local JSON
    if supabase:
        try:
            data = {
                "question": q.question,
                "answer": answer,
            }
            supabase.table("tarot_logs").insert(data).execute()
        except Exception as e:
            print(f"Error logging to Supabase: {e}")
    else:
        # Fallback: Log to local JSON file
        import json
        from datetime import datetime
        
        log_file = "backend/data/tarot_history.json"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": q.question,
            "answer": answer
        }
        
        try:
            history = []
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    try:
                        history = json.load(f)
                    except json.JSONDecodeError:
                        history = []
            
            history.append(log_entry)
            
            with open(log_file, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error logging to local file: {e}")

    return {"answer": answer}

@app.get("/")
async def root():
    return {"message": "Elksie5000 API is running"}

@app.get("/api/war-dead/all")
async def get_all_war_dead():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        response = supabase.table("war_dead_archive").select("*").execute()
        return response.data
    except Exception as e:
        # If the table doesn't exist, this will error
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crime/all")
async def get_all_crime_data():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        # Select all columns
        response = supabase.table("crime_data_archive").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sexes/time-series")
async def get_sexes_time_series():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        response = supabase.table("sexes_time_series_archive").select("*").order("year").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sexes/summary")
async def get_sexes_summary():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        response = supabase.table("sexes_summary_archive").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regions/time-series")
async def get_regions_time_series():
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        response = supabase.table("regions_time_series_archive").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/baby-names/search")
async def search_baby_names(query: str):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        # ILIKE for case-insensitive prefix search
        # We use a raw SQL query or rpc if possible, but simple select with ilike works
        # Note: distinct on a large table can be slow. 
        # Ideally we'd have a separate table of unique names, but let's try this first.
        # Or we can limit the search.
        
        # Using .ilike() on the 'name' column
        response = supabase.table("baby_names_archive") \
            .select("name") \
            .ilike("name", f"{query}%") \
            .limit(10) \
            .execute()
            
        # Extract unique names from the result (Supabase might return duplicates if we don't use distinct)
        # Supabase-py doesn't easily support DISTINCT in the builder chain without .rpc() or raw sql.
        # But for a simple autocomplete, fetching a few matches and deduplicating in python is okay for now,
        # though inefficient for "John" which has 100s of rows.
        # A better approach is a separate "unique_names" table or an RPC.
        # Let's assume for now we just return what we find and the frontend handles it, 
        # or we try to be smarter.
        
        # Actually, for autocomplete, we really want unique names.
        # Let's try to fetch a bit more and dedupe.
        
        names = list(set([item['name'] for item in response.data]))
        return sorted(names)[:10]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/baby-names/trends")
async def get_baby_name_trends(names: str):
    # names is a comma-separated string
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    name_list = [n.strip() for n in names.split(',')]
    
    try:
        response = supabase.table("baby_names_archive") \
            .select("*") \
            .in_("name", name_list) \
            .order("year") \
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_tables():
    """
    Function to print SQL for creating tables.
    """
    print("--- SQL for War Dead Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS war_dead_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        cemetery_name TEXT,
        coordinates JSONB,
        bio_html TEXT,
        num_commemorated INTEGER
    );
    """)
    
    print("\n--- SQL for Crime Data Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS crime_data_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        crime_type TEXT,
        location TEXT,
        coordinates JSONB,
        original_color TEXT
    );
    """)

    print("\n--- SQL for Sexes Time Series Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS sexes_time_series_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        year INTEGER,
        adm_per_male FLOAT,
        adm_per_female FLOAT,
        adm_per_male_rebased FLOAT,
        adm_per_female_rebased FLOAT,
        admissions_total BIGINT
    );
    """)

    print("\n--- SQL for Sexes Summary Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS sexes_summary_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        gender TEXT,
        admissions FLOAT,
        percentage FLOAT
    );
    """)

    print("\n--- SQL for Regions Time Series Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS regions_time_series_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        region TEXT,
        major_region TEXT,
        year INTEGER,
        adm_per_100k FLOAT,
        admissions_total BIGINT
    );
    """)
    
    print("\n--- SQL for Baby Names Table ---")
    print("""
    CREATE TABLE IF NOT EXISTS baby_names_archive (
        id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        name TEXT NOT NULL,
        sex TEXT NOT NULL,
        year INTEGER NOT NULL,
        count INTEGER,
        rank INTEGER
    );
    CREATE INDEX IF NOT EXISTS idx_baby_names_name ON baby_names_archive (name);
    """)

if __name__ == "__main__":
    create_tables()
