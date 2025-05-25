# Installation and Testing Guide for Enhanced kind2anki Addon

## Installation Steps

1. **Locate the Package**: The addon package is at:
   `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`

2. **Install in Anki**:
   - Open Anki
   - Go to Tools → Add-ons
   - Click "Install from file..."
   - Select the `kind2anki.ankiaddon` file
   - Restart Anki when prompted

3. **Verify Installation**:
   - After restart, go to Tools menu
   - You should see "kind2anki" option

## Testing the Enhanced Features

### Basic Import Test
1. Click Tools → kind2anki
2. Select your Kindle database file (vocab.db)
3. Check "Include dictionary definition" checkbox
4. Choose destination deck
5. Click Import

### Expected Output Format
The addon now creates cards with these fields (semicolon-separated):
- Word
- Reading (for languages like Japanese)
- Definition (translated + dictionary if enabled)
- Sentence (usage example from book)
- Audio (URL for pronunciation)
- Frequency (usage frequency data)
- BookName (source book title)

### Troubleshooting

#### If requests module is missing:
The addon will attempt to install it automatically. If that fails:
1. Open Anki's Python console (Tools → Add-ons → [select kind2anki] → "View Files")
2. Run: `pip install requests`

#### If dictionary lookups fail:
- Check internet connection
- The addon uses free API (dictionaryapi.dev)
- Fallback: Only translated definition will be used

#### If audio URLs don't work:
- Audio URLs are generated based on language detection
- Japanese: Uses JapanesePod101 format
- Others: Uses Forvo format
- URLs need internet access to work in Anki

## Expected Enhancements

✅ **Dictionary Integration**: Fetches English definitions from free API
✅ **Audio URLs**: Generates pronunciation links based on language
✅ **Usage Sentences**: Extracts sentences from original books
✅ **Book Names**: Identifies source material
✅ **Multi-field Cards**: Rich card format with 7 fields
✅ **Language Detection**: Automatic language identification
✅ **Frequency Framework**: Structure ready for frequency data

## Next Steps After Testing

1. Test import with sample Kindle database
2. Verify card creation in Anki
3. Check dictionary definition fetching
4. Validate audio URL generation
5. Confirm all fields are populated correctly

## File Locations

- Main addon: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
- Source code: `/Users/shrimankeshri/Documents/GitHub/kind2anki/`
- Documentation: `ENHANCED_FEATURES.md`
