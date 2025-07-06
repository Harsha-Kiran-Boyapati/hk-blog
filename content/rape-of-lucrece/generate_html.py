#!/usr/bin/env python3
import os
import re
import markdown
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
def read_markdown_file(file_path):
    """Read and return markdown content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def markdown_to_html(markdown_content):
    """Convert markdown to HTML"""
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'codehilite'])
    return md.convert(markdown_content)

def create_navigation(stanza_number, total_stanzas):
    """Create navigation links for stanza"""
    nav_links = []
    
    # Previous link
    if stanza_number > 1:
        nav_links.append(f'<a href="{stanza_number-1}.html" class="nav-btn prev">← Stanza {stanza_number-1}</a>')
    else:
        nav_links.append('<span class="nav-btn disabled">← Previous</span>')
    
    # Overview link
    nav_links.append('<a href="index.html" class="nav-btn overview">📚 Overview</a>')
    
    # Next link
    if stanza_number < total_stanzas:
        nav_links.append(f'<a href="{stanza_number+1}.html" class="nav-btn next">Stanza {stanza_number+1} →</a>')
    else:
        nav_links.append('<span class="nav-btn disabled">Next →</span>')
    
    return f'<div class="navigation">{"".join(nav_links)}</div>'

def get_css_styles():
    """Return CSS styles for the HTML pages"""
    return """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fafafa;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #8B4513;
            border-bottom: 3px solid #D2691E;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        
        h2 {
            color: #A0522D;
            margin-top: 40px;
            margin-bottom: 20px;
            border-left: 4px solid #D2691E;
            padding-left: 15px;
        }
        
        h3 {
            color: #8B4513;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 16px;
            line-height: 1.8;
            border-left: 4px solid #D2691E;
            display: block;
            white-space: pre-wrap;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #f8f4f0;
            font-weight: bold;
            color: #8B4513;
        }
        
        tr:nth-child(even) {
            background-color: #fafafa;
        }
        
        .navigation {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #f8f4f0;
            border-radius: 8px;
            border: 2px solid #D2691E;
        }
        
        .nav-btn {
            padding: 10px 20px;
            text-decoration: none;
            background-color: #8B4513;
            color: white;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        
        .nav-btn:hover {
            background-color: #A0522D;
        }
        
        .nav-btn.disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        
        .overview {
            background-color: #D2691E !important;
        }
        
        .stanza-info {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #4682B4;
        }
        
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        
        .overview-card {
            background: #f8f4f0;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #D2691E;
            text-align: center;
        }
        
        .overview-card a {
            text-decoration: none;
            color: #8B4513;
            font-weight: bold;
        }
        
        .overview-card:hover {
            background: #f0e8d8;
            transform: translateY(-2px);
            transition: all 0.3s;
        }
        
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, #D2691E, transparent);
            margin: 30px 0;
        }
        
        em {
            font-style: italic;
            color: #666;
        }
        
        strong {
            color: #8B4513;
        }
    </style>
    """

def create_html_page(title, content, stanza_number=None, total_stanzas=None):
    """Create complete HTML page"""
    navigation = ""
    if stanza_number and total_stanzas:
        navigation = create_navigation(stanza_number, total_stanzas)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {get_css_styles()}
</head>
<body>
    <div class="container">
        {navigation}
        {content}
        {navigation}
    </div>
</body>
</html>"""
    return html

def create_overview_page(stanza_files):
    """Create overview/index page with links to all stanzas"""
    content = """
    <h1>🌹 The Rape of Lucrece - Literary Analysis</h1>
    <p><em>Shakespeare's narrative poem with detailed stanza-by-stanza analysis</em></p>
    
    <h2>📖 About The Rape of Lucrece</h2>
    <p>Shakespeare's <em>The Rape of Lucrece</em> is a narrative poem published in 1594, 
    telling the tragic story of Lucrece, a virtuous Roman matron, and the devastating 
    consequences of her rape by Tarquin. The poem explores themes of honor, shame, 
    tyranny, and justice, and is a powerful exploration of moral and political decay.</p>
    
    <p>This analysis provides detailed examination of each stanza, breaking down 
    Shakespeare's complex language and imagery to make the poem more accessible 
    to modern readers.</p>
    
    <div class="stanza-info">
        <strong>About this analysis:</strong> Each stanza includes line-by-line breakdowns, 
        phrase meanings, literary devices, and overall significance in the context of the poem.
    </div>
    
    <h2>📚 Stanza Navigation</h2>
    <div class="overview-grid">
    """
    
    for stanza_num in sorted(stanza_files):
        content += f"""
        <a href="{stanza_num}.html">
            <div class="overview-card">
                Stanza {stanza_num}
            </div>
        </a>
        """
    
    content += """
    </div>
    """
    
    return create_html_page("The Rape of Lucrece - Overview", content)

def main():
    explanation_dir = ROOT_DIR / "content" / "rape-of-lucrece" / "explanation"
    html_dir = ROOT_DIR / "docs" / "rape-of-lucrece"
    
    # Create HTML directory
    html_dir.mkdir(exist_ok=True)
    
    # Find all markdown files
    markdown_files = list(explanation_dir.glob("*.md"))
    stanza_files = []
    
    print("🔄 Converting markdown files to HTML...")
    
    for md_file in markdown_files:
        # Extract stanza number from filename
        match = re.match(r'(\d+)\.md', md_file.name)
        if match:
            stanza_num = int(match.group(1))
            stanza_files.append(stanza_num)
            
            # Read markdown content
            markdown_content = read_markdown_file(md_file)
            if markdown_content:
                # Convert to HTML
                html_content = markdown_to_html(markdown_content)
                
                # Create complete HTML page
                title = f"Stanza {stanza_num} - The Rape of Lucrece Analysis"
                complete_html = create_html_page(
                    title, 
                    html_content, 
                    stanza_num, 
                    len(markdown_files)
                )
                
                # Write HTML file
                html_file = html_dir / f"{stanza_num}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(complete_html)
                
                print(f"✅ Created {html_file}")
    
    # Create overview page
    overview_html = create_overview_page(stanza_files)
    overview_file = html_dir / "index.html"
    with open(overview_file, 'w', encoding='utf-8') as f:
        f.write(overview_html)
    
    print(f"✅ Created overview page: {overview_file}")
    print(f"\n🎉 HTML generation complete!")
    print(f"📂 Files created in: {html_dir}")
    print(f"🌐 Open {overview_file} in your browser to start browsing")
    print(f"📊 Total stanzas converted: {len(stanza_files)}")

if __name__ == "__main__":
    main()
