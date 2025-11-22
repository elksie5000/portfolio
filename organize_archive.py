import os
import hashlib
import shutil
import re
from pypdf import PdfReader
from datetime import datetime

# Configuration
SOURCE_DIR = "public/articles"
DUPLICATES_DIR = os.path.join(SOURCE_DIR, "_duplicates")

def calculate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_text_from_pdf(filepath):
    """Extracts text from the first page of a PDF."""
    try:
        reader = PdfReader(filepath)
        if len(reader.pages) > 0:
            return reader.pages[0].extract_text()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return ""

def fix_double_text(text):
    """Fixes text that looks like 'TTHHEE QQUUIICCKK' -> 'THE QUICK'."""
    if len(text) < 10:
        return text
        
    # Check if > 80% of NON-SPACE characters are doubled
    # We iterate through the string, skipping spaces
    non_space_chars = [c for c in text if not c.isspace()]
    if len(non_space_chars) < 4:
        return text
        
    doubled_count = 0
    # Check pairs in non_space_chars
    # T T H H E E F F ...
    for i in range(0, len(non_space_chars) - 1, 2):
        if non_space_chars[i] == non_space_chars[i+1]:
            doubled_count += 1
            
    ratio = doubled_count / (len(non_space_chars) / 2)
    
    if ratio > 0.8:
        # It's likely doubled. Deduplicate.
        # We need to reconstruct carefully. 
        # If spaces are single but letters are double:
        # TTHHEE FFAA -> THE FA
        # We can just take every character that is DIFFERENT from the previous one?
        # No, 'BOOK' -> 'BOK'.
        # We should iterate and take char if it matches next char, skipping spaces?
        # Or just simple: take every 2nd char if it's not a space?
        # Actually, if spaces are single, we can't just do text[::2].
        # TTHHEE FFAA
        # 01234567890
        # T T H H E E   F F A A
        # Keep 0, 2, 4, 6(space), 7(skip), 8(keep)... tricky.
        
        # Simpler approach:
        # Reconstruct: Iterate through text. If char == next_char, take it and skip next. 
        # If char is space, take it.
        result = []
        i = 0
        while i < len(text):
            if text[i].isspace():
                result.append(text[i])
                i += 1
            elif i + 1 < len(text) and text[i] == text[i+1]:
                result.append(text[i])
                i += 2
            else:
                # Mismatch or end of string. 
                # If we are in "double mode", this might be a typo or just a single char.
                # Let's just keep it.
                result.append(text[i])
                i += 1
        return "".join(result)
        
    return text

def clean_filename(text):
    """Cleans text to be safe for filenames."""
    # Remove invalid characters
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    # Replace spaces with underscores
    text = text.replace(" ", "_")
    # Limit length - Increased to 200
    return text[:200]

def is_noise(line):
    """Checks if a line is likely noise (header, footer, URL, date only)."""
    original_line = line.strip()
    line_lower = original_line.lower()
    
    # Normalize for spaced out text check (e.g. "w w w .")
    normalized_line = line_lower.replace(" ", "")
    
    if not original_line:
        return True
    if len(normalized_line) < 4: # Too short
        return True
    
    # Check normalized (no spaces) for URL patterns
    if "www." in normalized_line or ".co.uk" in normalized_line or ".com" in normalized_line:
        return True
    if "thesentinel" in normalized_line:
        return True
    if "midlandsnewspaperoftheyear" in normalized_line:
        return True
    if "davidelks" in normalized_line: # Skip author name
        return True
    if "regionalnews" in normalized_line:
        return True
    if "sentinelbusiness" in normalized_line:
        return True
    
    if line_lower.startswith("by "): # Skip bylines
        return True
    if line_lower.endswith("inside") or line_lower.endswith("inside."): # Skip promos
        return True
    if "intrusion" in line_lower and "harassment" in line_lower: # Skip legal boilerplate
        return True
    if "write to the editor" in line_lower:
        return True
    if "commission at" in line_lower:
        return True
    if "dissatisfied" in line_lower:
        return True
        
    # Page numbers and dates
    if re.match(r'^\d+$', original_line): 
        return True
    if re.match(r'^(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?', line_lower): 
        return True
        
    return False

def analyze_text(text):
    """Analyzes text to find a potential title and date."""
    lines = text.split('\n')
    title = "Unknown_Title"
    date_str = None
    
    # Heuristic for Date: Look for common date formats anywhere in the text first
    # YYYY-MM-DD, DD/MM/YYYY, DD Month YYYY, Month DD, YYYY
    date_patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
        r'\b(\d{2}/\d{2}/\d{4})\b',  # DD/MM/YYYY
        r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b', # DD Month YYYY
        r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b' # Month DD, YYYY
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            # Try to normalize date to YYYY-MM-DD
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%d %B %Y", "%B %d, %Y"]:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    date_str = dt.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    continue
            break

    # Heuristic for Title:
    # 1. Filter out noise lines (including author name).
    # 2. Look for the first "substantial" line (likely the start of the first paragraph).
    # 3. Fallback to the first clean line.
    
    clean_lines = [line.strip() for line in lines if not is_noise(line)]
    
    if clean_lines:
        # Strategy 1: Look for the first substantial line (likely the first paragraph)
        # We define "substantial" as having a reasonable length (e.g., > 30 chars)
        for i, line in enumerate(clean_lines):
            line = fix_double_text(line) # Fix encoding if needed
            if len(line) > 30: 
                title = line
                
                # Check if we should append the next line
                # Conditions:
                # 1. Title is short (< 80 chars)
                # 2. Title ends with a connector word (preposition/conjunction)
                # 3. Next line exists
                
                should_append = False
                if len(title) < 80:
                    should_append = True
                
                lower_title = title.lower()
                connectors = [" from", " at", " of", " in", " to", " with", " and", " or", " but", " for", " on", " as", " by", " the"]
                if any(lower_title.endswith(c) for c in connectors):
                    should_append = True
                    
                if should_append and i + 1 < len(clean_lines):
                     next_line = fix_double_text(clean_lines[i+1])
                     # Don't append if next line is noise or date (though noise is filtered)
                     title += " " + next_line
                break
        
        # Strategy 2: If no long line found, just take the first clean line
        if title == "Unknown_Title":
            for line in clean_lines:
                # Avoid using the date string as the title
                if date_str and date_str in line:
                    continue
                title = fix_double_text(line)
                break
            
    return title, date_str

def scan_and_organize(directory, dry_run=True):
    print(f"Scanning {directory}...")
    print(f"Dry Run: {dry_run}\n")

    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    seen_hashes = {}
    
    # Plan storage
    moves = [] # (src, dest, reason)

    for filename in files:
        filepath = os.path.join(directory, filename)
        file_hash = calculate_file_hash(filepath)

        if file_hash in seen_hashes:
            # Duplicate found
            original_file = seen_hashes[file_hash]
            dest = os.path.join(DUPLICATES_DIR, filename)
            moves.append((filepath, dest, f"Duplicate of {original_file}"))
        else:
            seen_hashes[file_hash] = filename
            
            # Analyze for rename
            text = extract_text_from_pdf(filepath)
            title, date = analyze_text(text)
            
            clean_title = clean_filename(title)
            
            if date:
                new_filename = f"{date}_{clean_title}.pdf"
            else:
                # Fallback if title found but no date, or just analyzed
                if title != "Unknown_Title":
                    new_filename = f"{clean_title}.pdf"
                else:
                    base, ext = os.path.splitext(filename)
                    new_filename = f"{base}_analyzed{ext}"

            if new_filename != filename:
                dest = os.path.join(directory, new_filename)
                moves.append((filepath, dest, f"Renaming based on content: Title='{title}', Date='{date}'"))

    # Execute or Print Plan
    import json
    mapping = {}
    
    if dry_run:
        print("--- DRY RUN PLAN ---")
        if not moves:
            print("No changes needed.")
        for src, dest, reason in moves:
            print(f"[MOVE] {os.path.basename(src)} -> {os.path.basename(dest)}")
            print(f"       Reason: {reason}")
            if "_duplicates" in dest:
                 print(f"       (Will create {DUPLICATES_DIR} if not exists)")
    else:
        print("--- EXECUTING CHANGES ---")
        if not os.path.exists(DUPLICATES_DIR) and any("_duplicates" in m[1] for m in moves):
            os.makedirs(DUPLICATES_DIR)
            print(f"Created {DUPLICATES_DIR}")

        for src, dest, reason in moves:
            try:
                # Check for collision in destination
                if os.path.exists(dest) and src != dest:
                    base, ext = os.path.splitext(dest)
                    counter = 1
                    while os.path.exists(dest):
                        dest = f"{base}_{counter}{ext}"
                        counter += 1
                
                shutil.move(src, dest)
                print(f"Moved: {os.path.basename(src)} -> {os.path.basename(dest)}")
                
                # Store mapping (relative paths for portability)
                mapping[os.path.basename(src)] = os.path.basename(dest)
                
            except Exception as e:
                print(f"Error moving {src} to {dest}: {e}")
        
        # Save mapping to JSON
        mapping_file = os.path.join(directory, "mapping.json")
        with open(mapping_file, "w") as f:
            json.dump(mapping, f, indent=2)
        print(f"Mapping saved to {mapping_file}")

if __name__ == "__main__":
    # Execute for real
    scan_and_organize(SOURCE_DIR, dry_run=False)
