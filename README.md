# Harsha Kiran's Blog

Personal blog covering literature, technology, and various topics of interest. Features detailed literary analysis, coding projects, and thoughtful commentary.

## Repository Structure

```
hk-blog/
├── _config.yml           # Jekyll configuration
├── index.md             # Homepage
├── Gemfile              # Ruby dependencies
├── README.md            # This file
│
├── _shakespeare/        # Jekyll collection for Shakespeare content
│   ├── venus-and-adonis-complete-commentary.md
│   ├── lucrece-explanation.md
│   └── quotes.md
│
├── scripts/             # Content generation tools
│   ├── *.py            # Python scripts for LLM-based content generation
│   ├── *.sh            # Shell scripts for processing
│   ├── .env            # Environment variables
│   └── __pycache__/    # Python cache
│
├── content/            # Raw markdown content and source materials
│   ├── *.md           # Generated markdown files
│   └── venus-and-adonis/  # Individual stanza files
│
└── assets/            # Static assets
    ├── *.css         # Stylesheets
    └── *.xml         # Metadata files
```

## Folder Purpose

### `/scripts/` - Content Generation Tools
Contains Python scripts and tools used to generate explanations using LLM APIs:
- `explain_all_stanzas.py` - Batch explanation generator
- `gemini_explainer.py` - Google Gemini API integration
- `stanza_analyzer.py` - Literary analysis tools
- `kindle-book-generator.py` - E-book generation
- And other utility scripts

### `/content/` - Source Content
Raw markdown files and source materials:
- Original Shakespeare texts
- Generated explanations before Jekyll processing
- Individual stanza files

### `/_shakespeare/` - Jekyll Collection
Processed content ready for web publication:
- Properly formatted for Jekyll
- Will be served at `/literature/shakespeare/`
- Contains comprehensive literary analyses

### `/assets/` - Static Files
CSS, images, and other static assets:
- Custom stylesheets
- Metadata files
- Will be served directly by Jekyll

## Development

### Local Development
```bash
bundle install
bundle exec jekyll serve
```

### Deployment
Push to GitHub - GitHub Pages will automatically build and deploy the Jekyll site.

## Content Generation Workflow

1. **Create/Update Content**: Use scripts in `/scripts/` to generate explanations
2. **Process for Web**: Move processed content to `/_shakespeare/` collection
3. **Deploy**: Push to GitHub for automatic deployment

## Live Site

The blog will be available at: `https://harsha-kiran-boyapati.github.io/hk-blog/`

## Features

- **Literature Analysis**: Comprehensive Shakespeare commentary
- **Responsive Design**: Works on all devices
- **SEO Optimized**: Jekyll SEO plugin integration
- **Fast Loading**: Static site generation
- **Easy Maintenance**: Organized file structure
