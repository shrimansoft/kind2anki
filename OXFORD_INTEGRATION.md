# Oxford Learner's Dictionary Integration

## Overview

The Kind2Anki addon now includes enhanced dictionary functionality using Oxford Learner's Dictionary techniques adapted from the AutoDefine repository. This provides significantly better word definitions, pronunciations, examples, and audio compared to the basic dictionary API.

## Key Features

### 1. Enhanced Definition Quality
- **Rich Definitions**: Multiple definitions with proper grammar labels
- **Examples**: Real usage examples from Oxford corpus
- **Word Types**: Accurate part-of-speech detection
- **Labels**: Contextual labels (informal, formal, old-fashioned, etc.)

### 2. Pronunciation Support
- **IPA Notation**: Proper International Phonetic Alphabet pronunciation
- **Multiple Variants**: Both British and American pronunciations when available
- **Audio Integration**: Direct audio file downloads from Oxford

### 3. Audio Enhancement
- **High-Quality Audio**: Direct downloads from Oxford's audio servers
- **Format Support**: MP3 audio files optimized for Anki
- **Automatic Download**: Audio files automatically saved to Anki's media folder
- **Fallback Handling**: Graceful fallback if audio unavailable

### 4. Smart Examples
- **Fill-in-the-Blank**: Automatic creation of cloze-style examples
- **Multiple Sources**: Uses Kindle sentences first, Oxford examples as fallback
- **Context Preservation**: Maintains punctuation and sentence structure

## Technical Implementation

### Oxford Dictionary Module (`oxford_dictionary.py`)

The module implements web scraping techniques from the AutoDefine repository:

#### Key Components:
- **BeautifulSoup Parsing**: HTML parsing with specific CSS selectors
- **Request Handling**: Session management with cookie blocking
- **Error Handling**: Robust error handling for network issues
- **Data Extraction**: Comprehensive extraction of word information

#### CSS Selectors Used:
```python
# Word information
title_selector = '.top-container .headword'
wordform_selector = '.top-container .pos'

# Pronunciation
br_pronounce_selector = '[geo=br] .phon'
am_pronounce_selector = '[geo=n_am] .phon'

# Audio
br_pronounce_audio_mp3_selector = '[geo=br] [data-src-mp3]'
am_pronounce_audio_mp3_selector = '[geo=n_am] [data-src-mp3]'

# Definitions and examples
definitions_selector = '.senses_multiple .sense > .def'
examples_selector = '.senses_multiple .sense > .examples .x'
```

### Enhanced Processing Pipeline

1. **Word Lookup**: Query Oxford Learner's Dictionary
2. **Data Extraction**: Parse HTML to extract comprehensive word data
3. **Audio Download**: Download pronunciation audio files
4. **Field Mapping**: Map data to 9-field note structure
5. **Example Processing**: Create fill-in-the-blank examples

### Field Mapping Enhancements

| Field | Enhancement | Source |
|-------|-------------|---------|
| Word Type | Oxford POS data vs basic heuristics | `oxford_data['word_type']` |
| Phonetic | IPA pronunciation vs empty | `oxford_data['pronunciation']` |
| Example | Oxford examples if Kindle unavailable | `oxford_data['examples']` |
| Sound | Real Oxford audio vs generic URLs | `oxford_data['audio_url']` |
| Definition | Formatted Oxford definitions | `oxford_data['definitions']` |

## Configuration Options

### Maximum Limits
- **Definitions**: Up to 3 definitions per word (configurable)
- **Examples**: Up to 2 examples per definition (configurable)
- **Audio Preference**: American English preferred, British as fallback

### Fallback Behavior
- If Oxford lookup fails, gracefully falls back to basic dictionary API
- If audio download fails, provides generic audio field format
- If examples unavailable, uses Kindle sentence data

## Error Handling

### Network Issues
- **Timeout Handling**: 10-second timeout for HTTP requests
- **Connection Errors**: Graceful handling of network failures
- **Rate Limiting**: Respectful request patterns

### Data Issues
- **Word Not Found**: Clear messaging when word unavailable
- **Malformed Data**: Robust parsing with fallback values
- **Audio Failures**: Non-blocking audio download failures

## Performance Considerations

### Optimization Strategies
- **Session Reuse**: HTTP session reuse for better performance
- **Cookie Blocking**: Prevents tracking, improves speed
- **Selective Downloads**: Only downloads audio if media folder available
- **Caching**: Avoids re-downloading existing audio files

### Resource Management
- **Memory Efficient**: Processes words one at a time
- **Disk Space**: Audio files are reasonably sized (typically 20-50KB)
- **Network Bandwidth**: Respectful request patterns

## Dependencies

### Required Packages
- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing and data extraction
- **http.cookiejar**: Cookie management (built-in)

### Automatic Installation
The addon automatically attempts to install missing dependencies:
```python
def ensure_dependencies_installed():
    dependencies = ['requests', 'beautifulsoup4']
    # Automatic installation logic
```

## Usage Examples

### Basic Word Lookup
```python
result = lookup_oxford_dictionary("example")
# Returns comprehensive word data
```

### Enhanced Definition Formatting
```python
# Input: "example"
# Output: Rich HTML definition with examples
"""
<i>(noun)</i><br>
<b>1.</b> a thing characteristic of its kind or illustrating a general rule<br>
<b>Examples:</b><br>
• it is a good example of how European action can produce results<br>
• some of these constitute rare examples of ancient Egyptian art
"""
```

### Audio Integration
```python
# Downloads and returns filename
filename = download_audio_file(audio_url, "example", media_folder)
# Returns: "example_oxford.mp3"
```

## Testing and Validation

### Test Cases
1. **Common Words**: Verify basic word lookup works
2. **Complex Words**: Test words with multiple definitions
3. **Audio Download**: Verify audio files download correctly
4. **Error Handling**: Test behavior with invalid words
5. **Network Issues**: Test offline behavior

### Validation Checklist
- [ ] Oxford data extraction works correctly
- [ ] Audio files download to media folder
- [ ] Fill-in-the-blank examples created properly
- [ ] Word type detection enhanced vs basic
- [ ] Pronunciation formatting correct
- [ ] Error handling graceful

## Future Enhancements

### Potential Improvements
1. **Caching System**: Local cache for frequently looked up words
2. **Batch Processing**: Process multiple words in single request
3. **Advanced Audio**: Support for multiple pronunciations
4. **Custom Formatting**: User-configurable definition formatting
5. **Language Support**: Extension to other Oxford dictionaries

### Performance Optimizations
1. **Async Processing**: Asynchronous HTTP requests
2. **Connection Pooling**: Reuse HTTP connections
3. **Selective Field Updates**: Only update changed fields
4. **Smart Fallbacks**: Intelligent fallback strategies

## Troubleshooting

### Common Issues

#### 1. No Definitions Retrieved
**Cause**: Network connectivity or Oxford server issues
**Solution**: Check internet connection, try again later

#### 2. Audio Files Not Downloading
**Cause**: Media folder not accessible or audio URL invalid
**Solution**: Verify Anki is running and media folder permissions

#### 3. Import Errors
**Cause**: Missing dependencies
**Solution**: Dependencies auto-install on first run

#### 4. Slow Performance
**Cause**: Network latency or server response time
**Solution**: Normal for web scraping, consider caching

### Debug Information
Enable debug output by checking Anki's debug console for detailed error messages and processing information.

## Compliance and Ethics

### Web Scraping Considerations
- **Respectful Usage**: Reasonable request rates
- **Terms of Service**: Educational use within reasonable bounds
- **Attribution**: Credit to Oxford Learner's Dictionary
- **No Commercial Use**: For personal learning only

### Data Privacy
- **No User Data Storage**: No personal information stored
- **Local Processing**: All processing done locally
- **No Tracking**: Cookie blocking prevents tracking
