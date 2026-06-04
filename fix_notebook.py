import json

# Read current content
with open('analisis_kesehatan_mental.ipynb', 'r', encoding='utf-8') as f:
    text = f.read()

# Try to find the correct ending and fix it
# The root JSON object must end with nbformat and nbformat_minor
import re
# Just rebuild the JSON structure manually from the cell data
try:
    # Find everything up to the metadata block
    # It starts with "metadata": {
    # Let's just find the last valid array of cells
    cells_end = text.find('  ],\n "metadata": {')
    if cells_end == -1:
        cells_end = text.rfind('  ]\n }')
        
    # Let's do it simply:
    # Cut off anything after "language_info" block and append the correct nbformat
    cutoff = text.find('"version": "3.12.0"')
    if cutoff != -1:
        # 23 characters after version is the end of the language_info block
        end_of_lang = text.find('}', cutoff) + 1
        end_of_metadata = text.find('}', end_of_lang) + 1
        
        fixed = text[:end_of_metadata] + ',\n "nbformat": 4,\n "nbformat_minor": 4\n}'
        
        # Verify it parses
        data = json.loads(fixed)
        
        # Write it back
        with open('analisis_kesehatan_mental.ipynb', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1)
        print("Successfully fixed and parsed JSON!")
    else:
        print("Could not find version block")
except Exception as e:
    print("Error:", e)
