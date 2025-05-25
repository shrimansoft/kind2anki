# kind2anki Enhanced Addon - Testing Checklist

## ✅ Package Status
- **Package Created**: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon` (13,288 bytes)
- **Validation**: All required files present and valid
- **Manifest**: Properly formatted JSON with all required fields
- **PyQt6 Compatibility**: ✅ Fixed for Anki 25.x (see PYQT6_COMPATIBILITY_FIX.md)

## 🔧 Installation Instructions

### Step 1: Install the Addon
1. **Remove old version** (if previously installed): Tools → Add-ons → Select old kind2anki → Remove
2. Open Anki
3. Go to **Tools → Add-ons**
4. Click **"Install from file..."**
5. Select: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
6. Click **"Open"**
7. **Restart Anki** when prompted

### Step 2: Verify Installation
- After restart, check **Tools** menu
- You should see **"kind2anki"** option

## 🧪 Testing Scenarios

### Test 1: Basic Functionality
- [ ] Click **Tools → kind2anki**
- [ ] Dialog opens with enhanced UI
- [ ] "Include dictionary definition" checkbox is visible
- [ ] File browser works for selecting vocab.db
- [ ] Deck chooser functions properly

### Test 2: Enhanced Features
- [ ] Check "Include dictionary definition" box
- [ ] Import with internet connection (for dictionary API)
- [ ] Verify cards have multiple fields (Word, Reading, Definition, Sentence, Audio, Frequency, BookName)
- [ ] Check that dictionary definitions are fetched and added
- [ ] Verify audio URLs are generated based on language

### Test 3: Error Handling
- [ ] Test without internet connection
- [ ] Test with invalid vocab.db file
- [ ] Test with missing dependencies (requests module)

## 📋 Expected Output Format

After import, cards should have semicolon-separated fields:
```
Word;Reading;Definition;Sentence;Audio;Frequency;BookName
```

### Example Japanese Card:
```
桜;さくら;cherry blossom; Traditional Japanese flower...;春になると桜が咲きます;https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kana=さくら;High;日本語の本
```

### Example English Card:
```
serendipity;;the occurrence of events by chance; A pleasant surprise...;It was pure serendipity that led to the discovery;https://forvo.com/word/serendipity;Medium;Novel Title
```

## 🐛 Troubleshooting Guide

### If addon doesn't appear in Tools menu:
1. Check **Tools → Add-ons** to see if it's listed
2. If listed but disabled, enable it
3. If not listed, reinstallation may be needed

### If dictionary lookups fail:
- Check internet connection
- Fallback: Only translated definition will be used
- Dictionary API: [dictionaryapi.dev](https://dictionaryapi.dev)

### If requests module is missing:
1. Go to **Tools → Add-ons**
2. Select **kind2anki**
3. Click **"Config"** or **"View Files"**
4. The addon will attempt auto-installation on first use

### If import fails:
- Verify vocab.db file is valid Kindle database
- Check file permissions
- Ensure destination deck exists

## 🎯 Enhanced Features to Verify

### ✅ Dictionary Integration
- Uses free dictionaryapi.dev API
- Fetches English definitions
- Combines with translation
- Graceful fallback on failure

### ✅ Audio URL Generation
- **Japanese**: JapanesePod101 format
- **Other languages**: Forvo format  
- Language auto-detection
- No downloads, just URLs for Anki to fetch

### ✅ Rich Card Data
- **Word**: Original vocabulary term
- **Reading**: Pronunciation (mainly for Japanese)
- **Definition**: Combined translation + dictionary
- **Sentence**: Usage example from original book
- **Audio**: Generated pronunciation URL
- **Frequency**: Framework ready (placeholder for now)
- **BookName**: Source book identification

### ✅ Language Support
- Auto-detection of vocabulary language
- Appropriate audio service selection
- Unicode text handling

## 📊 Success Criteria

- [ ] Addon installs without errors
- [ ] UI loads with enhanced features
- [ ] Database import completes successfully
- [ ] Cards contain all expected fields
- [ ] Dictionary definitions are fetched when enabled
- [ ] Audio URLs are properly formatted
- [ ] No Python errors in Anki console

## 🔄 Next Steps After Testing

1. **If successful**: Document any usage notes or tips
2. **If issues found**: Create bug reports with specific error messages
3. **Performance**: Note any slowdowns with large vocabularies
4. **Enhancement opportunities**: Identify additional features

## 📁 Files Reference

- **Main Package**: `kind2anki.ankiaddon`
- **Installation Guide**: `INSTALLATION_GUIDE.md`
- **Enhanced Features**: `ENHANCED_FEATURES.md`
- **This Checklist**: `TESTING_CHECKLIST.md`
- **Validation Script**: `validate_package.py`
