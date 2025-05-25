# kind2anki - Enhanced Kindle to Anki Importer

An advanced Anki add-on that imports vocabulary from Kindle's Vocabulary Builder with **Oxford Dictionary integration**, enhanced field mapping, and comprehensive example sources. Transform your Kindle reading into powerful Anki flashcards with professional definitions, pronunciation, audio, and contextual examples.

## 🚀 Key Features

### ✨ **Enhanced Field Mapping (9-Field Note Type)**
- **Word**: Target vocabulary from Kindle
- **Word Type**: Enhanced with Oxford Dictionary part-of-speech data
- **Phonetic**: Oxford pronunciation with IPA notation
- **Example**: Dual-source examples (Oxford + Kindle) with clean formatting
- **Sound**: Enhanced audio with Oxford Dictionary sources
- **Image**: Ready for manual addition
- **Definition**: Oxford definitions as primary source + translations
- **Content**: Rich book information and source attribution
- **Copyright**: Generation metadata

### 📖 **Oxford Dictionary Integration**
- **Professional Definitions**: High-quality, authoritative definitions
- **IPA Pronunciation**: Accurate phonetic transcriptions
- **Audio Files**: Native speaker pronunciation
- **Usage Examples**: Professional example sentences
- **Word Types**: Accurate part-of-speech information

### 📚 **Enhanced Example Field**
- **Dual Sources**: Both Oxford Dictionary and Kindle book examples
- **Clean Formatting**: `📖 Oxford:` and `📚 Kindle:` labels
- **Fill-in-the-Blank**: Kindle examples with interactive blanks
- **Source Attribution**: Clear indication of example sources

### 📊 **Intelligent Content Prioritization**
1. **Definitions**: Oxford Dictionary → Translations → Basic lookup
2. **Examples**: Oxford professional examples + Kindle contextual usage
3. **Audio**: Oxford native audio → Generated URLs
4. **Pronunciation**: Oxford IPA → Kindle readings

### 🔧 **Advanced Features**
- **Book Attribution**: Full book titles and authors from Kindle database
- **Multiple Languages**: Support for English, German, Polish, Portuguese, Spanish, Lithuanian
- **Flexible Import**: Configurable time ranges and usage options
- **Rich HTML**: Enhanced formatting for better card readability

## 📦 Installation

### Method 1: Direct Installation
1. Download `kind2anki.ankiaddon` from this repository
2. Open Anki → Tools → Add-ons → Install from file...
3. Select the downloaded `.ankiaddon` file
4. Restart Anki

### Method 2: AnkiWeb (if available)
Go to https://ankiweb.net/shared/info/1621749993 and follow installation instructions.

## ⚙️ Oxford Dictionary Setup (Recommended)

To unlock the full potential of enhanced definitions and examples:

1. **Get Oxford Dictionary API credentials**:
   - Visit [Oxford Dictionaries API](https://developer.oxforddictionaries.com/)
   - Sign up for a free developer account
   - Get your Application ID and Application Key

2. **Configure in Anki**:
   - Tools → Add-ons → Select kind2anki → Config
   - Enter your Oxford API credentials
   - Enable dictionary integration

## 🎯 Usage

### Basic Import Process

1. **Access the Importer**
   - Go to Tools → kind2anki
   
2. **Configure Import Settings**
   - **Deck**: Choose target deck (or create new one)
   - **Import Mode**: Handle duplicates (Update/Ignore/Import all)
   - **✅ Include usage example**: Get Kindle contextual examples
   - **✅ Translate**: Enable translations for definitions
   - **✅ Include dictionary definition**: Enable Oxford integration
   - **Language**: Select target language for translations
   - **Days**: Import words from last N days

3. **Import Vocabulary**
   - Click "Import"
   - Select `vocab.db` from your Kindle device
   - Wait for processing (Oxford lookups may take time)
   - Review import summary

### Kindle Database Location

- **Linux**: `/media/username/Kindle/system/vocabulary/vocab.db`
- **Windows**: `D:\system\vocabulary\vocab.db` (replace D: with Kindle drive)
- **macOS**: `/Volumes/Kindle/system/vocabulary/vocab.db`

*Note: The `system` folder is hidden by default on Windows*

## 📋 Example Card Output

With Oxford integration enabled, your cards will contain:

```
Word: acquire
Word Type: verb
Phonetic: /əˈkwaɪə(r)/
Example: 
📖 Oxford:
The company decided to acquire a smaller competitor.

📚 Business Strategy Book:
The merger will help us _____ new market share.

Sound: [sound:acquire_oxford.mp3]
Definition: 
(verb)
1. Buy or obtain (an asset or object) for oneself
2. Learn or develop (a skill, habit, or quality)
Translation: adquirir, obtener

Content: Book: Business Strategy Fundamentals | Example from: Oxford + Kindle
```

## 🔧 Advanced Configuration

### Field Mapping Customization
The addon uses a 9-field note type optimized for vocabulary learning. You can:
- Customize field order in Anki's note type settings
- Modify card templates for different display styles
- Add custom CSS for enhanced visual presentation

### Language Support
- **Fully Supported**: English (with Oxford integration)
- **Supported with Translation**: German, Polish, Portuguese, Spanish, Lithuanian, Hindi
- **Extensible**: Easy to add new languages in configuration

## 🆚 What's New vs Original

| Feature | Original | Enhanced |
|---------|----------|----------|
| Dictionary | Google Translate only | Oxford Dictionary + Translation |
| Examples | Kindle only (if enabled) | Oxford + Kindle dual sources |
| Pronunciation | Basic/None | Oxford IPA notation |
| Audio | Generic URLs | Oxford native audio files |
| Word Types | Basic heuristics | Oxford part-of-speech data |
| Field Mapping | 3-4 basic fields | 9-field comprehensive system |
| Book Info | Limited | Full title, author, attribution |
| Formatting | Plain text | Rich HTML with clean styling |

## 🛠️ Development & Contribution

### Building from Source
```bash
# Clone repository
git clone https://github.com/yourusername/kind2anki.git
cd kind2anki

# Create package
bash create_package.sh

# Validate package
python validate_package.py
```

### Project Structure
```
kind2anki/
├── kind2anki/
│   ├── kindleimporter.py      # Core import logic with enhancements
│   ├── oxford_dictionary.py   # Oxford API integration
│   ├── translate.py           # Translation services
│   └── kind2anki_ui.py       # User interface
├── manifest.json             # Addon metadata
└── __init__.py              # Anki addon entry point
```

## ⚠️ Important Notes

### Oxford Dictionary API
- **Free Tier**: 3,000 requests/month (sufficient for most users)
- **Rate Limits**: Automatic handling with retries
- **Fallback**: Works without Oxford API (uses translations only)

### Google Translate
- **Anti-abuse**: Google may implement restrictions
- **Backup**: Oxford definitions reduce dependency on translations
- **Quality**: Oxford definitions are generally more accurate

### Performance
- **First Import**: Slower due to Oxford API calls and audio downloads
- **Subsequent Imports**: Faster with cached data
- **Large Vocabularies**: Consider importing in smaller batches

## 🐛 Troubleshooting

### Common Issues
1. **"Oxford API not responding"**: Check internet connection and API credentials
2. **"Import taking too long"**: Normal for large vocabularies with Oxford integration
3. **"Missing audio files"**: Ensure Anki has write permissions to media folder

### Support
- Check existing issues on GitHub
- Provide vocab.db size and error messages
- Include Anki version and operating system

## 📄 Disclaimer

- **Oxford Dictionary**: Requires API registration for full features
- **Google Translate**: Subject to service availability and restrictions
- **Accuracy**: Manual review of translations recommended
- **Usage**: Respect Oxford Dictionary API terms of service

## 🙏 Acknowledgments

- Original kind2anki developers
- Oxford Dictionaries API
- TextBlob translation library
- Anki community for feedback and testing

---

**Transform your Kindle vocabulary into comprehensive Anki flashcards with professional dictionary integration!**
