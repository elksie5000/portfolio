import json
import os
import re
from bs4 import BeautifulSoup

# Configuration
MAPPING_FILE = "public/articles/mapping.json"
TEMPLATES_DIR = "templates"
OUTPUT_FILE = "src/data/portfolio.json"

def load_mapping():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

def clean_text(text):
    if not text:
        return ""
    # Remove extra whitespace
    return " ".join(text.split())

def extract_pdf_filename(href):
    # Handle weird f-string syntax in HTML if present: href=f"/articles/..."
    if href.startswith('f"'):
        href = href[2:-1]
    
    # Standardize path separators
    href = href.replace("\\", "/")
    
    # Extract basename
    return os.path.basename(href)

def parse_html_file(filepath, category, mapping, start_id=1):
    items = []
    current_id = start_id
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return items, current_id

    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Strategy: Iterate through elements to find groupings of H2 -> P -> PDF
    # This is a bit loose because the HTML structure isn't strictly semantic containers.
    # We'll assume an H2 starts a new section.
    
    content_div = soup.find("div", class_="container") or soup.find("div", class_="markdown-body")
    if not content_div:
        content_div = soup.body

    current_item = None
    
    for element in content_div.find_all(["h2", "p", "a", "h3"]):
        if element.name == "h2":
            # Save previous item if valid
            if current_item:
                items.append(current_item)
                current_id += 1
            
            # Start new item
            title = clean_text(element.get_text())
            current_item = {
                "id": current_id,
                "title": title,
                "category": category,
                "summary": "",
                "pdf_path": None,
                "original_pdf": None
            }
        
        elif element.name == "p":
            if current_item:
                text = clean_text(element.get_text())
                if text:
                    if current_item["summary"]:
                        current_item["summary"] += " " + text
                    else:
                        current_item["summary"] = text
        
        elif element.name == "a":
            href = element.get("href")
            if href and (".pdf" in href.lower()):
                pdf_name = extract_pdf_filename(href)
                
                # If we have a current item, associate this PDF with it
                if current_item:
                    # If item already has a PDF, maybe duplicate item? 
                    # The legacy page lists multiple PDFs under one H2 sometimes (e.g. Royal Doulton).
                    # In that case, we should probably create a new item for each PDF, 
                    # inheriting the title/summary of the section.
                    
                    if current_item["pdf_path"]:
                        # Create a clone for this new PDF
                        items.append(current_item)
                        current_id += 1
                        current_item = current_item.copy()
                        current_item["id"] = current_id
                        # Reset PDF info for the new clone
                        current_item["pdf_path"] = None
                        current_item["original_pdf"] = None
                    
                    current_item["original_pdf"] = pdf_name
                    if pdf_name in mapping:
                        current_item["pdf_path"] = f"/articles/{mapping[pdf_name]}"
                    else:
                        current_item["pdf_path"] = f"/articles/{pdf_name}" # Fallback
                else:
                    # Orphan PDF? Create an item for it
                    current_item = {
                        "id": current_id,
                        "title": pdf_name, # Temporary title
                        "category": category,
                        "summary": "",
                        "pdf_path": None,
                        "original_pdf": pdf_name
                    }
                    if pdf_name in mapping:
                        current_item["pdf_path"] = f"/articles/{mapping[pdf_name]}"
                        # Try to make a better title from the new filename
                        new_name = mapping[pdf_name]
                        # Remove date and extension
                        parts = new_name.split("_", 1)
                        if len(parts) > 1:
                            raw_title = parts[1].replace(".pdf", "").replace("_", " ")
                            current_item["title"] = raw_title
                    else:
                        current_item["pdf_path"] = f"/articles/{pdf_name}"

    # Append the last item
    if current_item:
        items.append(current_item)
        current_id += 1
        
    return items, current_id

def main():
    mapping = load_mapping()
    all_items = []
    next_id = 1
    
    # Parse Articles
    print("Parsing articles.html...")
    articles, next_id = parse_html_file(os.path.join(TEMPLATES_DIR, "articles.html"), "Articles", mapping, next_id)
    all_items.extend(articles)
    
    # Parse Portfolio (if needed, though user mentioned flask_app.py lists projects)
    # The user said: "Parse flask_app.py to find the data structures... Cross-Reference the old PDF filenames"
    # But also "If you find hardcoded text in the HTML templates... extract that too"
    # I looked at flask_app.py and it didn't seem to have the list. It had routes rendering templates.
    # So parsing templates is the right way.
    
    print("Parsing portfolio.html...")
    portfolio, next_id = parse_html_file(os.path.join(TEMPLATES_DIR, "portfolio.html"), "Portfolio", mapping, next_id)
    all_items.extend(portfolio)

    # Ensure output dir exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_items, f, indent=2)
        
    print(f"Extracted {len(all_items)} items to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
