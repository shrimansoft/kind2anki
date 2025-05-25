# Enhanced Kindle2Anki Features

This version of Kindle2Anki includes additional features that provide richer information for your Anki cards.

## New Fields and Features

The enhanced version now includes the following fields:

1. **Word** - The target word from your Kindle vocabulary
2. **Reading** - Reading/pronunciation (especially useful for Japanese words)
3. **Definition** - Now includes both:
   - Translation to your target language
   - Dictionary definition from a free dictionary API
4. **Sentence** - Usage example from your Kindle with highlighted word
5. **Audio** - Automatically generates URL links to audio pronunciations
6. **Frequency** - Frequency information (framework is in place, but requires loading a frequency database)
7. **BookName** - The book title where you encountered the word

## How to Use

1. Run the plugin as before via Tools > kind2anki
2. The new option "Include dictionary definition" allows you to add dictionary definitions to your cards
3. Once imported, make sure your Anki note type has fields corresponding to these data types

## Setting Up Note Types

For the best experience, create a note type in Anki with the following fields:

1. Word
2. Reading
3. Definition
4. Sentence
5. Audio
6. Frequency
7. BookName

## Technical Details

- Dictionary definitions are fetched from a free API (dictionaryapi.dev) for English words
- For non-English words, they are first translated to English and then looked up
- Audio URLs are generated using JapanesePod101 format for Japanese words and Forvo format for other languages
- The frequency framework is prepared but requires connecting to a frequency database

## Future Improvements

- Add direct frequency list integration
- Add support for offline dictionaries
- Improve Japanese reading detection
- Add support for custom audio sources

## Credits

Based on the original kind2anki addon with enhancements inspired by Kindle2Anki Python script by Kartoffel0.
