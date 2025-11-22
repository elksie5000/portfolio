def fix_double_text(text):
    """Fixes text that looks like 'TTHHEE QQUUIICCKK' -> 'THE QUICK'."""
    # Check if a significant portion of the text follows the double pattern
    # Pattern: char1 == char2, char3 == char4, etc.
    # We'll check the first few words
    if len(text) < 10:
        return text
        
    # Heuristic: Check if > 80% of characters are doubled
    doubled_count = 0
    check_len = min(len(text), 50)
    # The previous logic was: for i in range(0, check_len - 1, 2):
    # But what if it starts with a single char? Or spaces are not doubled?
    # Let's try to see if removing every second char makes sense.
    
    # Test string from user: "TTHHEE FFAANNTTAASSYY WWOORRLLDD OOFF ‘‘CCAAPPTTAAIINN CCAADD’’"
    # T T H H E E   F F A A ...
    # 0 1 2 3 4 5   6 7 8 9
    
    for i in range(0, check_len - 1, 2):
        if text[i] == text[i+1]:
            doubled_count += 1
            
    ratio = doubled_count / (check_len / 2)
    print(f"Ratio: {ratio}")
    
    if ratio > 0.8:
        # It's likely doubled. Deduplicate.
        return text[::2]
    return text

test_str = "TTHHEE FFAANNTTAASSYY WWOORRLLDD OOFF ‘‘CCAAPPTTAAIINN CCAADD’’"
print(f"Original: {test_str}")
print(f"Fixed:    {fix_double_text(test_str)}")

test_str_2 = "Community devastated after loss of popular venue"
print(f"Original: {test_str_2}")
print(f"Fixed:    {fix_double_text(test_str_2)}")
