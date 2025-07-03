#!/usr/bin/env python3
"""
Static Site Builder for Harsha Kiran's Blog
Generates HTML files from content into public/ folder
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def clean_public_dir():
    """Clean and recreate public directory"""
    public_dir = Path("../public")
    if public_dir.exists():
        shutil.rmtree(public_dir)
    
    # Create directory structure
    directories = [
        "public",
        "public/assets",
        "public/venus-and-adonis",
        "public/literature", 
        "public/tech",
        "public/about"
    ]
    
    for dir_path in directories:
        Path(f"../{dir_path}").mkdir(parents=True, exist_ok=True)
    
    print("✅ Cleaned and created public directory structure")

def copy_static_assets():
    """Copy CSS, images, and other static assets"""
    # Copy CSS
    if Path("../assets/style.css").exists():
        shutil.copy("../assets/style.css", "../public/assets/")
    
    # Copy interactive HTML demos
    if Path("../venus-adonis-interactive.html").exists():
        shutil.copy("../venus-adonis-interactive.html", "../public/")
    
    print("✅ Copied static assets")

def copy_venus_adonis_html():
    """Copy Venus and Adonis HTML files"""
    html_dir = Path("../content/venus-and-adonis/html")
    if html_dir.exists():
        # Copy all HTML files from content to public
        for html_file in html_dir.glob("*.html"):
            shutil.copy(html_file, "../public/venus-and-adonis/")
        print(f"✅ Copied {len(list(html_dir.glob('*.html')))} Venus and Adonis HTML files")
    else:
        print("⚠️  Venus and Adonis HTML directory not found")

def copy_main_files():
    """Copy main HTML files"""
    # Copy homepage
    if Path("../index.html").exists():
        shutil.copy("../index.html", "../public/")
    
    print("✅ Copied main HTML files")

def create_venus_adonis_index():
    """Create Venus and Adonis index page with links to all stanzas"""
    
    # Check if we have HTML files
    html_files = list(Path("../public/venus-and-adonis").glob("[0-9]*.html"))
    stanza_numbers = sorted([int(f.stem) for f in html_files if f.stem.isdigit()])
    
    # Create stanza grid HTML
    stanza_grid = ""
    for i in range(0, len(stanza_numbers), 10):
        stanza_grid += '<div class="stanza-row">\n'
        for stanza_num in stanza_numbers[i:i+10]:
            stanza_grid += f'  <a href="{stanza_num}.html" class="stanza-link">Stanza {stanza_num}</a>\n'
        stanza_grid += '</div>\n'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venus and Adonis: Complete Commentary | Harsha Kiran's Blog</title>
    <link rel="stylesheet" href="../assets/style.css">
    <style>
        .content-wrapper {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .back-nav {{
            margin-bottom: 2rem;
        }}
        .back-nav a {{
            color: #0366d6;
            text-decoration: none;
            font-weight: 500;
        }}
        .back-nav a:hover {{
            text-decoration: underline;
        }}
        .stanza-grid {{
            margin: 2rem 0;
        }}
        .stanza-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        .stanza-link {{
            display: block;
            padding: 0.8rem 1.2rem;
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            text-decoration: none;
            color: #0366d6;
            font-weight: 500;
            transition: all 0.2s ease;
            min-width: 120px;
            text-align: center;
        }}
        .stanza-link:hover {{
            background: #0366d6;
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .stats {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
            text-align: center;
        }}
        .stats h3 {{
            margin: 0 0 1rem 0;
            color: #24292e;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #0366d6;
            display: block;
        }}
        .stat-label {{
            color: #586069;
            font-size: 0.9rem;
        }}
        @media (max-width: 768px) {{
            .stanza-row {{
                justify-content: center;
            }}
            .stanza-link {{
                min-width: 100px;
                padding: 0.6rem 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <h1><a href="/">Harsha Kiran's Blog</a></h1>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/literature/">Literature</a></li>
                <li><a href="/tech/">Technology</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </nav>
    </header>

    <main class="content-wrapper">
        <div class="back-nav">
            <a href="/">← Back to Home</a>
        </div>
        
        <h1>🎭 Venus and Adonis: Complete Commentary</h1>
        <p><em>Comprehensive stanza-by-stanza literary analysis of Shakespeare's narrative poem</em></p>
        
        <div class="stats">
            <h3>📊 Analysis Overview</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-number">{len(stanza_numbers)}</span>
                    <span class="stat-label">Stanzas Analyzed</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{len(stanza_numbers) * 6}</span>
                    <span class="stat-label">Lines Covered</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">199</span>
                    <span class="stat-label">Total Stanzas</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{round(len(stanza_numbers)/199*100)}%</span>
                    <span class="stat-label">Completion</span>
                </div>
            </div>
        </div>
        
        <h2>📖 Browse by Stanza</h2>
        <p>Click any stanza below to read the detailed literary analysis:</p>
        
        <div class="stanza-grid">
            {stanza_grid}
        </div>
        
        <div class="stats">
            <h3>🔧 About This Analysis</h3>
            <p>This comprehensive analysis was generated using custom Python scripts that leverage AI language models for detailed literary commentary. Each stanza includes:</p>
            <ul style="text-align: left; max-width: 600px; margin: 1rem auto;">
                <li><strong>Line-by-line analysis</strong> - Detailed explanations of phrases and meanings</li>
                <li><strong>Literary devices</strong> - Identification of metaphors, imagery, and techniques</li>
                <li><strong>Historical context</strong> - Renaissance literature and cultural background</li>
                <li><strong>Thematic significance</strong> - How each stanza contributes to the overall poem</li>
            </ul>
        </div>
    </main>

    <footer>
        <p>&copy; 2025 Harsha Kiran. Generated on {datetime.now().strftime("%B %d, %Y")}</p>
    </footer>
</body>
</html>"""
    
    with open("../public/venus-and-adonis/index.html", 'w') as f:
        f.write(html)
    
    print(f"✅ Created Venus and Adonis index with {len(stanza_numbers)} stanzas")

def create_github_pages_config():
    """Create necessary files for GitHub Pages"""
    
    # Create .nojekyll file to prevent Jekyll processing
    with open("../public/.nojekyll", 'w') as f:
        f.write("")
    
    print("✅ Created GitHub Pages configuration")

def main():
    """Main build process"""
    print("🚀 Building static site...")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Build steps
    clean_public_dir()
    copy_static_assets()
    copy_venus_adonis_html()
    copy_main_files()
    create_venus_adonis_index()
    create_github_pages_config()
    
    print("=" * 50)
    print("🎉 Site built successfully!")
    print("📂 Files are in the public/ directory")
    print("🌐 Ready for GitHub Pages deployment")
    
    # Show structure
    print("\n📁 Public directory structure:")
    for root, dirs, files in os.walk("../public"):
        level = root.replace("../public", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    main()
