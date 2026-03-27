#!/usr/bin/env python3
"""
Script to compile all numbered HTML files in docs/rape-of-lucrece into a single PDF.
Each HTML file becomes a page in the final PDF.
"""

import os
import sys
from pathlib import Path
import tempfile
import re
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def get_numbered_html_files(directory):
    """Get all numbered HTML files and sort them numerically."""
    html_files = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'index.html':
            # Extract number from filename (e.g., "123.html" -> 123)
            match = re.match(r'^(\d+)\.html$', filename)
            if match:
                number = int(match.group(1))
                html_files.append((number, filename))
    
    # Sort by number
    html_files.sort(key=lambda x: x[0])
    return [filename for number, filename in html_files]

def create_combined_html(input_directory, html_files):
    """Create a single HTML file combining all individual HTML files."""
    
    # Start building the combined HTML with fixed page layout
    combined_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Rape of Lucrece - Complete Analysis</title>
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.3;
            color: #333;
            font-size: 10pt;
        }}
        
        /* Each page container - exactly one page */
        .page {{
            width: 8.5in;
            height: 11in;
            padding: 0.5in;
            page-break-after: always;
            page-break-inside: avoid;
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        
        /* Content wrapper with scroll behavior controlled */
        .page-content {{
            flex: 1;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}
        
        /* Container styling adjusted for page constraints */
        .container {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            flex: 1;
            overflow: hidden;
        }}
        
        h1 {{
            color: #8B4513;
            border-bottom: 2px solid #D2691E;
            padding-bottom: 5px;
            margin-bottom: 10px;
            font-size: 14pt;
            line-height: 1.2;
        }}
        
        h2 {{
            color: #A0522D;
            margin-top: 15px;
            margin-bottom: 8px;
            border-left: 3px solid #D2691E;
            padding-left: 8px;
            font-size: 12pt;
            line-height: 1.2;
        }}
        
        h3 {{
            color: #8B4513;
            margin-top: 10px;
            margin-bottom: 5px;
            font-size: 11pt;
            line-height: 1.2;
        }}
        
        p {{
            margin-bottom: 8px;
            line-height: 1.3;
        }}
        
        ul, ol {{
            margin-left: 15px;
            margin-bottom: 8px;
        }}
        
        li {{
            margin-bottom: 3px;
            line-height: 1.2;
        }}
        
        code {{
            background-color: #f5f5f5;
            padding: 8px;
            border-radius: 3px;
            display: block;
            margin: 8px 0;
            font-size: 9pt;
            line-height: 1.2;
            overflow: hidden;
            word-wrap: break-word;
        }}
        
        blockquote {{
            margin: 8px 0;
            padding-left: 10px;
            border-left: 3px solid #ddd;
            font-style: italic;
        }}
        
        /* Ensure no content overflows the page */
        .page-content * {{
            max-width: 100%;
            word-wrap: break-word;
        }}
        
        /* Hide overflow content that doesn't fit on the page */
        .content-wrapper {{
            height: 100%;
            overflow: hidden;
        }}
    </style>
</head>
<body>
"""

    # Add content from each HTML file
    for i, html_file in enumerate(html_files):
        file_path = os.path.join(input_directory, html_file)
        print(f"Processing {html_file} ({i+1}/{len(html_files)})")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the body content (everything between <body> and </body>)
        body_start = content.find('<body>') + len('<body>')
        body_end = content.find('</body>')
        
        if body_start > len('<body>') - 1 and body_end != -1:
            body_content = content[body_start:body_end].strip()
            
            # Wrap each HTML file's content in a page container
            combined_html += f'''
<div class="page">
    <div class="page-content">
        <div class="content-wrapper">
            {body_content}
        </div>
    </div>
</div>
'''
    
    combined_html += """
</body>
</html>
"""
    
    return combined_html

def main():
    # Set up paths
    current_dir = Path(__file__).parent
    lucrece_dir = current_dir / "docs" / "rape-of-lucrece"
    output_file = current_dir / "The_Rape_of_Lucrece_Complete_Analysis.pdf"
    
    if not lucrece_dir.exists():
        print(f"Error: Directory {lucrece_dir} not found!")
        sys.exit(1)
    
    print("Finding numbered HTML files...")
    html_files = get_numbered_html_files(lucrece_dir)
    
    if not html_files:
        print("No numbered HTML files found!")
        sys.exit(1)
    
    print(f"Found {len(html_files)} HTML files (from {html_files[0]} to {html_files[-1]})")
    
    print("Creating combined HTML...")
    combined_html = create_combined_html(lucrece_dir, html_files)
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8', delete=False) as temp_file:
        temp_file.write(combined_html)
        temp_html_path = temp_file.name
    
    try:
        print("Converting to PDF...")
        print("This may take several minutes for 265 pages...")
        
        # Configure fonts for better rendering
        font_config = FontConfiguration()
        
        # Create CSS for better PDF formatting
        css = CSS(string='''
            @page {
                size: 8.5in 11in;
                margin: 0;
            }
            
            body {
                margin: 0;
                padding: 0;
            }
            
            .page {
                width: 8.5in;
                height: 11in;
                padding: 0.5in;
                page-break-after: always;
                page-break-inside: avoid;
                overflow: hidden;
                box-sizing: border-box;
            }
            
            /* Remove the page break from the last page */
            .page:last-child {
                page-break-after: avoid;
            }
        ''', font_config=font_config)
        
        # Convert HTML to PDF
        html_doc = HTML(filename=temp_html_path)
        html_doc.write_pdf(output_file, stylesheets=[css], font_config=font_config)
        
        print(f"✅ Successfully created PDF: {output_file}")
        print(f"📄 Total pages: {len(html_files)}")
        print(f"📁 File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        sys.exit(1)
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_html_path)
        except:
            pass

if __name__ == "__main__":
    main()
