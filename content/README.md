# Shakespeare Venus and Adonis Analysis

A comprehensive literary analysis project for Shakespeare's narrative poem "Venus and Adonis" using AI-powered explanations.

## 📁 Project Structure

```
/Users/hk/books/shakespeare/
├── venus-and-adonis.md              # Original poem with numbered stanzas
├── venus-and-adonis/
│   ├── explanation/                 # Individual stanza analysis files
│   │   ├── 1.md
│   │   ├── 2.md
│   │   └── ...
│   └── html/                        # HTML versions for web viewing
├── stanza_analyzer.py               # 🔧 Shared analysis module
├── gemini_explainer.py              # Single stanza processor
├── explain_all_stanzas.py           # Sequential batch processor  
├── explain_stanzas_parallel.py      # Parallel batch processor
├── generate_html.py                 # HTML generator (needs markdown lib)
└── .env                            # API key configuration
```

## 🔧 Core Module: `stanza_analyzer.py`

The shared module that handles all common functionality:
- **`get_gemini_explanation()`** - Calls Gemini LLM API using requests
- **`write_stanza_explanation()`** - Creates formatted markdown files
- **`analyze_and_write_stanza()`** - Complete pipeline function
- **`load_env_file()`** - Environment variable loading

### Dependencies
- `requests` - HTTP library for API calls (cleaner than subprocess/curl)
- `pathlib` - Modern path handling

## 🖥️ Scripts

### `gemini_explainer.py`
- Process a single stanza (default: stanza 1)
- Good for testing and development
- Usage: `python3 gemini_explainer.py`

### `explain_all_stanzas.py`
- Process all stanzas sequentially
- Includes rate limiting (1 second between requests)
- Usage: `python3 explain_all_stanzas.py`

### `explain_stanzas_parallel.py`
- Process first 20 stanzas in parallel
- Uses ThreadPoolExecutor with 5 workers
- Faster but more API intensive
- Usage: `python3 explain_stanzas_parallel.py`

### `generate_html.py`
- Convert markdown explanations to HTML
- Creates navigation between stanzas
- Requires: `pip install markdown`
- Usage: `python3 generate_html.py`

## 📝 Explanation Format

Each explanation file follows this structure:

1. **Title** - Stanza number and subtitle
2. **Original Stanza** - Raw text in code block
3. **Line-by-Line Analysis** - Each line as heading with:
   - Phrase explanations as bullet points
   - Overall line meaning as bullet point
4. **Literary Devices** - Table format
5. **Overall Meaning & Significance** - Context analysis

### Example Format:
```markdown
### Line 1: "Even as the sun with purple-colour'd face"
*   **"Even as"**: Just as, at the very moment...
*   **"purple-colour'd face"**: Refers to the sun at dawn...
*   **Meaning:** "Just as the sun, appearing with its deep reddish-purple dawn color,"
---
```

## 🔑 Setup

1. Get Gemini API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs)
2. Install dependencies: `pip install requests`
3. Create `.env` file:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```
4. Run desired script

## 📊 Status

- ✅ Scripts refactored to use shared module
- ✅ No code duplication
- ✅ Consistent formatting across all tools
- ✅ Bullet point format for phrase explanations and meanings
- ✅ Error handling and template generation
- 🔄 HTML generation ready (needs markdown library)

## 🚀 Quick Start

```bash
# Process single stanza
python3 gemini_explainer.py

# Process all stanzas
python3 explain_all_stanzas.py

# Process first 20 in parallel
python3 explain_stanzas_parallel.py

# Generate HTML (after installing markdown)
pip install markdown
python3 generate_html.py
