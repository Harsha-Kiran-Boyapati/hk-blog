#!/usr/bin/env python3
import os
import re
from pathlib import Path
import google.generativeai as genai
import time

ROOT_DIR = Path(__file__).parent.parent
POEM = 'rape-of-lucrece'
GENERATION_MODEL = "models/gemini-2.0-flash-lite"  # Use Gemini Flash model
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=API_KEY)


def extract_stanza(content, stanza_number):
    """Extract a specific stanza from the poem content"""
    lines = content.split('\n')
    stanza_lines = []
    in_stanza = False
    
    for line in lines:
        if line.strip() == f'## Stanza {stanza_number}':
            in_stanza = True
            continue
        elif line.strip().startswith('## Stanza ') and in_stanza:
            break
        elif in_stanza and line.strip():  # Skip empty lines
            stanza_lines.append(line)
    
    return '\n'.join(stanza_lines).strip()

def get_gemini_explanation(stanza_text, stanza_number):
    prompt = (
        f"Explain the following stanza from Shakespeare's 'The Rape of Lucrece' by breaking down each part and then providing an overall meaning. "
        f"Highlight any literary devices.\n\nStanza {stanza_number}:\n{stanza_text}"
    )
    try:
        model = genai.GenerativeModel(GENERATION_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini API failed for stanza {stanza_number}: {e}")
        return "[Gemini API call failed]"

def create_explanation_file(stanza_number, stanza_text, explanation):
    """Create explanation file for a stanza"""
    dir_path = ROOT_DIR / f"content/{POEM}/explanation"
    os.makedirs(dir_path, exist_ok=True)
    file_path = dir_path / f"{stanza_number}.md"
    content = f"""# Stanza {stanza_number} - Explanation

## Original Stanza
```
{stanza_text}
```

## 🔍 Line-by-Line Analysis
{explanation}
"""
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Created explanation file: {file_path}")
    return file_path

def list_gemini_models():
    try:
        models = genai.list_models()
        print("Available Gemini models:")
        for m in models:
            print(f"- {m.name} (methods: {m.supported_generation_methods})")
    except Exception as e:
        print(f"[ERROR] Could not list Gemini models: {e}")

def main():
    # Read the Rape of Lucrece file
    with open(ROOT_DIR / f"content/{POEM}/{POEM}.md", 'r') as f:
        content = f.read()
    # Find all stanza numbers
    stanza_numbers = [int(num) for num in range(1, 2)]
    for stanza_number in stanza_numbers:
        stanza_text = extract_stanza(content, stanza_number)
        if stanza_text:
            file_path = ROOT_DIR / f"content/{POEM}/explanation/{stanza_number}.md"
            explanation = get_gemini_explanation(stanza_text, stanza_number)
            create_explanation_file(stanza_number, stanza_text, explanation)
            time.sleep(1)  # Avoid rate limits
    print(f"Generated explanations for {len(stanza_numbers)} stanzas.")

if __name__ == "__main__":
    # list_gemini_models()
    main()
