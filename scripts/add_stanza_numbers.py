#!/usr/bin/env python3

def add_stanza_numbers(input_file, output_file):
    """Add stanza numbers to Shakespeare's Venus and Adonis poem respecting existing stanza breaks"""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split by double newlines (empty lines that separate stanzas)
    stanzas = content.strip().split('\n\n')
    
    output_lines = []
    stanza_number = 1
    
    for stanza in stanzas:
        if stanza.strip():  # Skip any empty stanzas
            output_lines.append(f'## Stanza {stanza_number}\n')
            output_lines.append(stanza.strip() + '\n\n')
            stanza_number += 1
    
    # Remove the last extra newline
    if output_lines:
        output_lines[-1] = output_lines[-1].rstrip() + '\n'
    
    # Write the output
    with open(output_file, 'w') as f:
        f.writelines(output_lines)
    
    print(f"Added stanza numbers to {stanza_number - 1} stanzas")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    add_stanza_numbers('../content/venus-and-adonis.md', 
                      '../content/venus-and-adonis-numbered.md')
