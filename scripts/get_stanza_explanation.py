#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
POEM = 'rape-of-lucrece'
def extract_stanza(content, stanza_number):
    """Extract a specific stanza from the Venus and Adonis content"""
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

def create_explanation_file(stanza_number, stanza_text, explanation="[Explanation to be added from Gemini LLM]"):
    """Create explanation file for a stanza"""
    
    file_path = ROOT_DIR / f"content/{POEM}/explanation/{stanza_number}.md"
    
    content = f"""# Stanza {stanza_number} - Explanation

## Original Stanza
```
{stanza_text}
```

## Explanation Request for Gemini
**Prompt:** "Explain stanza by breaking down each part and then providing an overall meaning. Highlight any literary devices."

## Gemini Response
{explanation}
"""
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Created explanation file: {file_path}")
    return file_path

def main():
    # Read the Venus and Adonis file
    with open(ROOT_DIR / f"content/{POEM}/{POEM}.md", 'r') as f:
        content = f.read()
    
    # Test with stanza 1
    stanza_number = 1
    stanza_text = extract_stanza(content, stanza_number)
    
    print(f"Extracted Stanza {stanza_number}:")
    print(stanza_text)
    print("\n" + "="*50 + "\n")
    
    # Create explanation file template
    file_path = create_explanation_file(stanza_number, stanza_text)
    
    # Show the prompt that would be sent to Gemini
    print("Prompt for Gemini LLM:")
    print(f"Explain stanza by breaking down each part and then providing an overall meaning. Highlight any literary devices.\n\nStanza:\n{stanza_text}")

if __name__ == "__main__":
    main()
