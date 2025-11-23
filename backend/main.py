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
    allow_origins=origins,
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
