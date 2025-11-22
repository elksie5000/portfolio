import json
import os
import re
import shutil

# Configuration
ARTICLES_DIR = "public/articles"
MAPPING_FILE = os.path.join(ARTICLES_DIR, "mapping.json")
PORTFOLIO_FILE = "src/data/portfolio.json"

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {} if filepath.endswith("mapping.json") else []

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def clean_filename(filename):
    # Remove unicode characters like ●, ’, etc.
    # Keep alphanumeric, underscores, hyphens, dots.
    # Also fix double underscores if any.
    
    # Decode/Encode to remove non-ascii might be too aggressive if we want to keep accents?
    # But user specifically asked to remove \u25cf (●) and \u2019 (’)
    
    # Replace specific chars first
    filename = filename.replace("●", "")
    filename = filename.replace("’", "")
    filename = filename.replace("‘", "")
    filename = filename.replace("“", "")
    filename = filename.replace("”", "")
    
    # Remove other non-ascii
    filename = re.sub(r'[^\x00-\x7F]+', '', filename)
    
    # Replace spaces with underscores (should be already done but just in case)
    filename = filename.replace(" ", "_")
    
    # Remove weird chars
    filename = re.sub(r'[^\w\-\.]', '', filename)
    
    # Fix multiple underscores
    filename = re.sub(r'_{2,}', '_', filename)
    
    # Remove leading/trailing underscores (before extension)
    base, ext = os.path.splitext(filename)
    base = base.strip('_')
    
    return f"{base}{ext}"

def execute_cleanup():
    print("Starting cleanup...")
    mapping = load_json(MAPPING_FILE)
    portfolio = load_json(PORTFOLIO_FILE)
    
    # 1. Identify duplicates
    # We look for keys in mapping like "X.pdf" and "X_edited.pdf"
    # Or just scan the directory for files that look like duplicates?
    # The user said: "pairs like Title.pdf and Title_1.pdf" in the new filenames.
    # But the mapping keys are the ORIGINAL filenames.
    # Let's look at the MAPPING keys to find pairs.
    
    original_files = list(mapping.keys())
    groups = {}
    
    for f in original_files:
        base = f.replace("_edited.pdf", ".pdf")
        if base not in groups:
            groups[base] = []
        groups[base].append(f)
        
    # 2. Process groups
    files_to_delete = []
    renames = {} # old_new_name -> cleaned_new_name
    
    # We need to track changes to the "current" filename on disk
    # The mapping values are the current filenames on disk.
    
    new_mapping = mapping.copy()
    
    for base, files in groups.items():
        if len(files) > 1:
            # We have duplicates (e.g. ['Renew1.pdf', 'Renew1_edited.pdf'])
            # Prefer _edited
            edited_version = None
            original_version = None
            
            for f in files:
                if "_edited" in f:
                    edited_version = f
                else:
                    original_version = f
            
            if edited_version and original_version:
                print(f"Found duplicate pair: {original_version} / {edited_version}")
                
                # We want to keep the content of edited_version
                # But maybe we want the filename of the original_version's destination?
                # Actually, the user said: "Keep the _edited version... rename it to the clean title"
                # The 'clean title' is likely the one without '_1' suffix if possible.
                
                dest_edited = mapping[edited_version]
                dest_original = mapping[original_version]
                
                # Check which one is better? Usually the one without _1 is better, 
                # but sometimes _edited mapped to the _1 version because original took the main name.
                
                # We will keep dest_edited file.
                # We will delete dest_original file.
                # We will update mapping: original_version -> dest_edited (or cleaned version of it)
                
                files_to_delete.append(dest_original)
                
                # If dest_edited has a _1 suffix, try to remove it?
                # Only if it doesn't conflict with something else (but we just deleted the conflict!)
                
                final_dest = dest_edited
                if dest_original != dest_edited:
                    # If the original destination was "better" (shorter?), maybe use that name for the edited file?
                    # But dest_original might be the "bad" one (unedited content).
                    # Let's just stick to dest_edited for now, but clean it.
                    pass
                
                # Remove the original entry from mapping? 
                # No, the user might reference the original filename in legacy code.
                # So mapping[original_version] should point to the NEW kept file.
                new_mapping[original_version] = final_dest
                
            else:
                # Multiple files but not clear pair?
                pass
        else:
            # Single file
            pass

    # 3. Sanitize all filenames
    # Iterate through all current values in new_mapping
    # Calculate clean name.
    # If clean name != current name, rename.
    
    # We need a map of current_disk_name -> clean_disk_name
    disk_renames = {}
    
    for original_key, current_val in new_mapping.items():
        if current_val in files_to_delete:
            # This file is slated for deletion, but we remapped the key to the kept file above.
            # Wait, if we remapped new_mapping[original_version] = dest_edited,
            # then current_val is now dest_edited.
            # So we are good.
            pass
            
        clean_val = clean_filename(current_val)
        
        # Also remove _1 suffix if it was introduced by duplication and we deleted the other?
        # This is tricky to detect automatically without context.
        # But we can try to remove _1 if it's at the end of the basename.
        if clean_val.endswith("_1.pdf"):
             # Check if the version without _1 exists or is being renamed to
             base_clean = clean_val[:-6] + ".pdf"
             # If base_clean is NOT in the target list, we can use it.
             # But we are building the target list now.
             # Let's be safe and just clean unicode for now.
             pass

        if clean_val != current_val:
            disk_renames[current_val] = clean_val
            new_mapping[original_key] = clean_val

    # 4. Execute Deletions
    print(f"Deleting {len(files_to_delete)} duplicate files...")
    for f in files_to_delete:
        path = os.path.join(ARTICLES_DIR, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {f}")
        else:
            print(f"File to delete not found: {f}")

    # 5. Execute Renames
    # Handle collisions?
    # If A -> B, and B exists?
    # We should do this carefully.
    
    print(f"Renaming {len(disk_renames)} files...")
    for old, new in disk_renames.items():
        if old in files_to_delete:
            continue # Already deleted
            
        old_path = os.path.join(ARTICLES_DIR, old)
        new_path = os.path.join(ARTICLES_DIR, new)
        
        if not os.path.exists(old_path):
            # Maybe it was already renamed? (e.g. multiple keys pointing to same file)
            continue
            
        if old_path == new_path:
            continue
            
        if os.path.exists(new_path):
            print(f"Warning: Target {new} exists. Skipping rename of {old}.")
            continue
            
        os.rename(old_path, new_path)
        print(f"Renamed {old} -> {new}")

    # 6. Update Portfolio JSON
    print("Updating portfolio.json...")
    for item in portfolio:
        if item.get("pdf_path"):
            # pdf_path is like "/articles/Filename.pdf"
            current_pdf = os.path.basename(item["pdf_path"])
            
            # Find what this maps to now
            # We need to find the original key that produced this current_pdf
            # Or just check if current_pdf was renamed?
            
            # If the item was pointing to a deleted file, we need to point it to the kept file.
            # But we don't easily know which original key generated this item.
            # Wait, we stored "original_pdf" in the item!
            
            original_key = item.get("original_pdf")
            if original_key and original_key in new_mapping:
                new_filename = new_mapping[original_key]
                item["pdf_path"] = f"/articles/{new_filename}"
            elif current_pdf in disk_renames:
                 # Fallback if original_key missing
                 new_filename = disk_renames[current_pdf]
                 item["pdf_path"] = f"/articles/{new_filename}"

    # 7. Save
    save_json(MAPPING_FILE, new_mapping)
    save_json(PORTFOLIO_FILE, portfolio)
    print("Cleanup complete.")

if __name__ == "__main__":
    execute_cleanup()
