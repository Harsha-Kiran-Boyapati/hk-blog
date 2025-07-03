# Kindle Conversion Guide
*Converting Venus and Adonis Commentary to Kindle Format*

## ⭐ IMPORTANT: AZW3 is the RECOMMENDED format for modern Kindles!

### Kindle Format Compatibility:
- **AZW3** - ⭐ **RECOMMENDED** for modern Kindles (2014+)
- **KFX** - 🆕 **NEWEST** format for latest Kindles (2016+)  
- **EPUB** - 📱 For other e-readers (NOT optimal for Kindle)
- **MOBI** - 📱 Legacy format (deprecated by Amazon)

---

## Method 1: Using Pandoc + Calibre (RECOMMENDED)

### Step 1: Install Required Tools
You already have Pandoc installed! ✅

**REQUIRED: Install Calibre for AZW3 conversion:**
```bash
brew install --cask calibre
```

### Step 2: Recommended Conversion Commands

#### Convert to AZW3 (RECOMMENDED for Kindle)
```bash
# First create EPUB intermediate file
pandoc "Venus-and-Adonis-Complete-Commentary.md" \
  -o "Venus-and-Adonis-Commentary.epub" \
  --epub-metadata=metadata.xml \
  --toc \
  --toc-depth=2 \
  --css=kindle-styles.css

# Then convert EPUB to AZW3 using Calibre
ebook-convert "Venus-and-Adonis-Commentary.epub" \
  "Venus-and-Adonis-Commentary.azw3" \
  --title="Venus and Adonis: Complete Commentary" \
  --authors="Shakespeare Literary Analysis" \
  --language=en \
  --tags="Literature, Shakespeare, Poetry, Analysis"
```

#### Convert to KFX (Newest Kindle Format)
```bash
# Convert to KFX if you have the plugin
ebook-convert "Venus-and-Adonis-Commentary.epub" \
  "Venus-and-Adonis-Commentary.kfx" \
  --title="Venus and Adonis: Complete Commentary" \
  --authors="Shakespeare Literary Analysis"
```

### Step 3: EPUB Conversion (NOT recommended for Kindle)
```bash
# Only use EPUB for other e-readers
pandoc "Venus-and-Adonis-Complete-Commentary.md" \
  -o "Venus-and-Adonis-Commentary.epub" \
  --epub-metadata=metadata.xml \
  --toc \
  --toc-depth=2 \
  --css=kindle-styles.css
```

---

## Method 2: Using Kindle Create (GUI Method)

### Important Note:
Kindle Create outputs **KPF format** which Amazon converts to AZW3 automatically during publishing.

### Step 1: Download Kindle Create
1. Visit: https://kdp.amazon.com/en_US/help/topic/G202131170
2. Download Kindle Create for Mac
3. Install the application

### Step 2: Import Your Document
1. Open Kindle Create
2. Select "New Project from File"
3. Choose your `Venus-and-Adonis-Complete-Commentary.md` file
4. Select "Reflowable" format (recommended for text-heavy books)

### Step 3: Format Your Book
1. **Add Cover**: Create or upload a cover image
2. **Table of Contents**: Kindle Create will auto-generate from your headers
3. **Chapter Breaks**: Adjust where chapters start/end
4. **Styling**: Apply consistent formatting

### Step 4: Preview and Export
1. Use the preview feature to test on different devices
2. Export as .kpf (Kindle Package Format)
3. Upload directly to KDP (Amazon converts to AZW3 automatically)

---

## Method 3: Using Calibre Directly

### Install Calibre
```bash
brew install --cask calibre
```

### Direct Markdown to AZW3 Conversion
```bash
ebook-convert "Venus-and-Adonis-Complete-Commentary.md" \
  "Venus-and-Adonis-Commentary.azw3" \
  --title="Venus and Adonis: Complete Commentary" \
  --authors="Shakespeare Literary Analysis" \
  --language=en \
  --toc-title="Table of Contents" \
  --tags="Literature, Shakespeare, Poetry, Analysis, Renaissance" \
  --comments="Complete stanza-by-stanza analysis of Shakespeare's Venus and Adonis"
```

---

## ⭐ RECOMMENDED Workflow

1. **Use the automated script** `./convert-to-kindle.sh` (creates AZW3 + other formats)
2. **Test the AZW3** on Kindle Previewer
3. **Upload AZW3** to KDP for publishing
4. **Transfer AZW3** directly to Kindle devices

---

## Format Compatibility Guide

### For Modern Kindles (2014+):
- ✅ **AZW3** - Best compatibility and features
- ✅ **KFX** - Enhanced typography (if available)
- ❌ **EPUB** - May have formatting issues
- ❌ **MOBI** - Deprecated, limited features

### For Publishing on Amazon KDP:
- ✅ **AZW3** - Recommended upload format
- ✅ **KPF** - From Kindle Create
- ⚠️ **EPUB** - Converted to AZW3 by Amazon (may lose formatting)

### For Other E-readers:
- ✅ **EPUB** - Universal format
- ❌ **AZW3** - Kindle-specific (won't work)

---

## Tips for Best AZW3 Results

### Formatting Tips
- Use consistent heading levels (# ## ###)
- Keep tables simple for small screens
- Test navigation on actual Kindle devices
- Ensure images are appropriately sized

### Metadata Tips
- Include comprehensive title and author info
- Add relevant tags for discoverability
- Set proper language and publication info
- Include description/comments

### Quality Assurance
- **MUST:** Test on Kindle Previewer
- **MUST:** Check on different screen sizes
- **RECOMMENDED:** Test on actual Kindle device
- **RECOMMENDED:** Verify table of contents works

---

*Next: Run `./convert-to-kindle.sh` to create your AZW3 Kindle book!*
