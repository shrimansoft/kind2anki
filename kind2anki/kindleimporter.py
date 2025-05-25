# coding=utf-8
import sqlite3
import sys
import os
import tempfile
import codecs
import json
import urllib
import datetime
import time
from urllib.parse import quote, urlencode

try:
    import requests
except ImportError:
    pass  # We've already tried to install it above

from aqt import mw
from functools import partial

from .translate import translate
from .oxford_dictionary import lookup_oxford_dictionary, download_audio_file


def get_audio_url(word, reading=""):
    """
    Generate audio URL for a word. For Japanese words, we can use JapanesePod101 API.
    For other languages, we try to use forvo.com URL format.
    
    Args:
        word: The word to get audio for
        reading: Optional reading (especially for Japanese words)
    
    Returns:
        URL string to the audio file
    """
    # Try to detect if it's Japanese (simple heuristic - contains Japanese characters)
    if any(ord(c) > 0x3000 for c in word):  # Japanese characters range
        # JapanesePod101 style URL
        if reading:
            return f"https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji={urllib.parse.quote(word)}&kana={urllib.parse.quote(reading)}"
        else:
            return f"https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji={urllib.parse.quote(word)}"
    else:
        # Generic Forvo-style URL (may not work without an API key in real implementation)
        return f"https://audio.forvo.com/audios/mp3/{urllib.parse.quote(word)}.mp3"


def get_frequency_data(word):
    """
    Get frequency data for a word. In a real implementation, this would look up a frequency list.
    For demonstration purposes, this returns a dummy value.
    
    Args:
        word: The word to look up frequency for
    
    Returns:
        String representing the frequency data
    """
    # This is a placeholder. In a real implementation, you would
    # load frequency data from a file or database
    return ""


def translateWord(word, target_language):
    return str(translate(word, to_lang=target_language))
    
def lookupDictionary(word):
    """
    Enhanced dictionary lookup using Oxford Learner's Dictionary
    
    Args:
        word: The word to look up
        
    Returns:
        Formatted definition string
    """
    try:
        # Use Oxford Dictionary for better definitions (request more examples)
        oxford_result = lookup_oxford_dictionary(word, max_definitions=3, max_examples_per_def=5)
        
        if oxford_result:
            # Format the Oxford result
            formatted_def = []
            
            # Add word type if available
            if oxford_result['word_type']:
                formatted_def.append(f"<i>({oxford_result['word_type']})</i>")
            
            # Add definitions
            if oxford_result['definitions']:
                for i, definition in enumerate(oxford_result['definitions'][:3], 1):
                    formatted_def.append(f"<b>{i}.</b> {definition}")
            
            # Add examples if available
            if oxford_result['examples']:
                formatted_def.append("<br><b>Examples:</b>")
                for example in oxford_result['examples'][:3]:
                    formatted_def.append(f"• {example}")
            
            return "<br>".join(formatted_def)
        else:
            # Fallback to basic definition
            return f"<i>Definition not available for '{word}'</i>"
            
    except Exception as e:
        print(f"Dictionary lookup error for '{word}': {e}")
        return f"<i>Dictionary lookup failed for '{word}'</i>"


class KindleImporter():
    def __init__(self, db_path, target_language, includeUsage=False,
                 doTranslate=True, importDays=5, includeDictionary=True):
        self.db_path = db_path
        self.target_language = target_language
        self.includeUsage = includeUsage
        self.doTranslate = doTranslate
        self.includeDictionary = includeDictionary
        self.timestamp = self.createTimestamp(importDays) * 1000

    def createTimestamp(self, days):
        d = (datetime.date.today() - datetime.timedelta(days=days))
        return int(time.mktime(d.timetuple()))

    def translateWordsFromDB(self):
        self.getWordsFromDB()
        self.translated = self.translateWords()

    def fetchWordsFromDBWithoutTranslation(self):
        self.getWordsFromDB()
        self.translated = len(self.words) * ['']

    def getWordsFromDB(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get words and their IDs with timestamp filter
        c.execute("SELECT word, id, lang FROM words WHERE timestamp > ?",
                  (str(self.timestamp),))
        words_and_ids = c.fetchall()
        self.words = []
        self.word_keys = []
        self.langs = {}
        
        # Filter out words that aren't in the target language 
        # (assuming Kindle stores language info, if not, we'll store all words)
        for word, word_id, lang in words_and_ids:
            self.words.append(word)
            self.word_keys.append(word_id)
            self.langs[word_id] = lang if lang else "en"  # Default to English if no language
        
        # Get additional information from the database
        self.readings = {}
        self.sentences = {}
        self.book_names = {}
        self.frequencies = {}
        self.audio_urls = {}
        
        # Get usage sentences and book information
        for i, word_key in enumerate(self.word_keys):
            word = self.words[i]
            
            # Getting sentences/usages
            c.execute("SELECT usage, book_key FROM LOOKUPS WHERE word_key = ?", [word_key])
            usages_and_books = c.fetchall()
            
            if usages_and_books:
                self.sentences[word_key] = usages_and_books[0][0]  # Get the first usage example
                
                # Get book name if available
                book_key = usages_and_books[0][1]
                if book_key:
                    c.execute("SELECT title FROM BOOK_INFO WHERE id = ?", [book_key])
                    book_result = c.fetchone()
                    if book_result:
                        self.book_names[word_key] = book_result[0]
                    else:
                        self.book_names[word_key] = "Unknown Book"
                else:
                    self.book_names[word_key] = "Unknown Book"
            else:
                self.sentences[word_key] = ""
                self.book_names[word_key] = "Unknown Book"
            
            # Try to detect Japanese words and extract readings
            # This is very basic - in a real implementation you'd use a Japanese dictionary
            if self.langs[word_key] == "ja" or any(ord(c) > 0x3000 for c in word):
                # For Japanese, we could try to get the reading from a dictionary
                # For now, we'll just leave it empty as Kindle doesn't store this
                self.readings[word_key] = ""
            else:
                # For non-Japanese words, reading is not applicable
                self.readings[word_key] = ""
            
            # Get frequency data
            self.frequencies[word_key] = get_frequency_data(word)
            
            # Generate audio URL
            self.audio_urls[word_key] = get_audio_url(word, self.readings[word_key])
            
        conn.close()

    def translateWords(self):
        translated_data = []
        translate_func = partial(
            translateWord, target_language=self.target_language)
            
        for word, word_key in zip(self.words, self.word_keys):
            # Initialize card components
            card_data = {
                "word": word,
                "reading": self.readings.get(word_key, ""),
                "translated_definition": "",
                "dictionary_definition": "",
                "oxford_data": None,  # Store Oxford data for enhanced processing
                "sentence": self.sentences.get(word_key, ""),
                "frequency": self.frequencies.get(word_key, ""),
                "book_name": self.book_names.get(word_key, "Unknown Book"),
                "audio_url": self.audio_urls.get(word_key, "")
            }
            
            # Add dictionary lookup if enabled (do this first to get Oxford data)
            if self.includeDictionary:
                try:
                    # For languages other than English, we'd need a different API
                    # Here we assume English for the dictionary API
                    if self.langs.get(word_key, "en") == "en":
                        # Get Oxford data for enhanced processing (request more examples)
                        oxford_result = lookup_oxford_dictionary(word, max_definitions=3, max_examples_per_def=5)
                        if oxford_result:
                            card_data["oxford_data"] = oxford_result
                            card_data["dictionary_definition"] = lookupDictionary(word)
                        else:
                            card_data["dictionary_definition"] = ""
                    else:
                        # For non-English words, try to get a translation first then lookup
                        try:
                            eng_word = translate(word, from_lang=self.langs.get(word_key, "en"), to_lang="en")
                            card_data["dictionary_definition"] = lookupDictionary(eng_word)
                        except:
                            card_data["dictionary_definition"] = ""
                except Exception:
                    card_data["dictionary_definition"] = ""
            
            # Enhanced example handling - include BOTH Oxford and Kindle examples
            oxford_result = card_data.get("oxford_data")
            combined_examples = []
            
            # Helper function to create fill-in-the-blank
            def create_fill_in_blank(sentence, target_word):
                """Create fill-in-the-blank by replacing target word with _____"""
                if not sentence:
                    return sentence
                    
                word_lower = target_word.lower()
                words_in_sentence = sentence.split()
                
                for i, sentence_word in enumerate(words_in_sentence):
                    clean_word = sentence_word.strip('.,!?;:"()[]').lower()
                    if clean_word == word_lower or clean_word.startswith(word_lower):
                        punctuation = ''.join(c for c in sentence_word if not c.isalnum())
                        words_in_sentence[i] = "<b><i>_____</i></b>" + punctuation
                        break
                        
                return " ".join(words_in_sentence)
            
            # Collect Oxford examples if available (4-5 examples with fill-in-the-blank)
            oxford_examples = []
            if oxford_result and oxford_result.get('examples'):
                # Take up to 5 Oxford examples and create fill-in-the-blank
                oxford_examples = oxford_result['examples'][:5]
                if oxford_examples:
                    oxford_section = ["📖 <b>Oxford:</b>"]
                    for i, example in enumerate(oxford_examples, 1):
                        fill_blank_example = create_fill_in_blank(example, word)
                        oxford_section.append(f"{i}. {fill_blank_example}")
                    combined_examples.append("<br>".join(oxford_section))
            
            # Collect Kindle example if available and usage is enabled
            kindle_example = ""
            if self.includeUsage and card_data["sentence"]:
                kindle_example = card_data["sentence"]
                # Create fill-in-the-blank for Kindle example using the same helper function
                kindle_fill_blank = create_fill_in_blank(kindle_example, word).replace(";", ",")
                combined_examples.append(f"📚 <b>Kindle:</b><br>{kindle_fill_blank}")
            
            # Set the example field with combined examples
            if combined_examples:
                card_data["sentence"] = "<br><br>".join(combined_examples)
                if oxford_examples and kindle_example:
                    card_data["example_source"] = "Oxford + Kindle"
                elif oxford_examples:
                    card_data["example_source"] = "Oxford"
                elif kindle_example:
                    card_data["example_source"] = "Kindle"
                else:
                    card_data["example_source"] = "None"
            else:
                card_data["sentence"] = ""
                card_data["example_source"] = "None"
            
            # Add translation if enabled
            if self.doTranslate:
                try:
                    card_data["translated_definition"] = translate_func(word)
                except Exception as e:
                    card_data["translated_definition"] = "cannot translate"
            
            translated_data.append(card_data)
            
        return translated_data

    def createTemporaryFile(self):
        if len(self.words) == 0:
            return None
            
        path = os.path.join(tempfile.gettempdir(), "kind2anki_temp.txt")
        
        # Try to get Anki's media folder for audio downloads
        try:
            from aqt import mw
            if mw and mw.col:
                media_folder = mw.col.media.dir()
            else:
                media_folder = None
        except:
            media_folder = None
        
        with codecs.open(path, "w", encoding="utf-8") as f:
            # Write all card fields into the file
            for card_data in self.translated:
                # Enhanced definition field - prioritize Oxford definitions over translations
                oxford_result = card_data.get("oxford_data")
                definition = ""
                
                # First priority: Oxford dictionary definition
                if oxford_result and oxford_result.get('definitions'):
                    oxford_definitions = oxford_result['definitions'][:2]  # Take first 2 definitions
                    definition_parts = []
                    
                    # Add word type if available
                    if oxford_result.get('word_type'):
                        definition_parts.append(f"<i>({oxford_result['word_type']})</i>")
                    
                    # Add definitions
                    for i, def_text in enumerate(oxford_definitions, 1):
                        definition_parts.append(f"<b>{i}.</b> {def_text}")
                    
                    definition = "<br>".join(definition_parts)
                    
                    # Add translation as supplementary information if available
                    if card_data["translated_definition"]:
                        definition += f"<hr><b>Translation:</b> {card_data['translated_definition']}"
                
                # Fallback: Use translation as primary definition
                elif card_data["translated_definition"]:
                    definition = card_data["translated_definition"]
                    
                # Last resort: Basic dictionary definition
                elif card_data["dictionary_definition"]:
                    definition = card_data["dictionary_definition"]
                
                # Enhanced word type detection using Oxford data
                word_type = self.detect_word_type_enhanced(card_data["word"], card_data.get("oxford_data"))
                
                # Enhanced pronunciation using Oxford data
                pronunciation = self.get_pronunciation_enhanced(card_data["word"], card_data.get("oxford_data"))
                
                # Enhanced audio handling using Oxford data
                audio_field = self.get_audio_field_enhanced(card_data["word"], card_data.get("oxford_data"), media_folder)
                
                # Enhanced Content field with detailed book information
                book_info = f"Book: {card_data['book_name']}"
                if card_data.get("example_source") and card_data.get("example_source") != "None":
                    book_info += f" | Example from: {card_data['example_source']}"
                
                # Map to user's 9-field note type:
                # 1:Word, 2:Word Type, 3:Phonetic, 4:Example, 5:Sound, 6:Image, 7:Def, 8:Content, 9:Copyright
                fields = [
                    card_data["word"],                          # 1: Word
                    word_type,                                  # 2: Word Type (enhanced with Oxford data)
                    pronunciation or card_data["reading"],      # 3: Phonetic (enhanced with Oxford pronunciation)
                    card_data["sentence"],                      # 4: Example (with _____ replacing word)
                    audio_field,                               # 5: Sound (enhanced with Oxford audio)
                    "",                                         # 6: Image (intentionally empty)
                    definition,                                 # 7: Def (enhanced with Oxford definitions)
                    book_info,                                 # 8: Content (enhanced book information)
                    "Generated by Kind2Anki from Kindle Vocabulary Builder" # 9: Copyright
                ]
                
                # Write as semicolon-delimited line
                f.write(u"{}\n".format(";".join(field.replace(";", ",") for field in fields)))
                
        return path

    def detect_word_type(self, word):
        """
        Basic word type detection. This is a simple implementation.
        In a more advanced version, you could use NLP libraries like spaCy or NLTK.
        
        Args:
            word: The word to analyze
            
        Returns:
            String indicating the word type (noun, verb, adjective, etc.)
        """
        word = word.lower().strip()
        
        # Very basic heuristics - this could be improved with proper POS tagging
        if word.endswith(('ing', 'ed', 'en')):
            return "verb"
        elif word.endswith(('ly')):
            return "adverb"
        elif word.endswith(('ful', 'less', 'ous', 'ive', 'able', 'ible')):
            return "adjective"
        elif word.endswith(('tion', 'sion', 'ness', 'ment', 'ity', 'ty')):
            return "noun"
        elif len(word.split()) > 1:
            return "phrase"
        else:
            return "word"  # Default fallback
    
    def detect_word_type_enhanced(self, word, oxford_data):
        """
        Enhanced word type detection using Oxford Dictionary data
        
        Args:
            word: The word to analyze
            oxford_data: Oxford dictionary data if available
            
        Returns:
            String indicating the word type
        """
        # First try to get word type from Oxford data
        if oxford_data and oxford_data.get('word_type'):
            return oxford_data['word_type']
        
        # Fallback to basic detection
        return self.detect_word_type(word)
    
    def get_pronunciation_enhanced(self, word, oxford_data):
        """
        Get enhanced pronunciation using Oxford Dictionary data
        
        Args:
            word: The word
            oxford_data: Oxford dictionary data if available
            
        Returns:
            Pronunciation string or None
        """
        if oxford_data and oxford_data.get('pronunciation'):
            return oxford_data['pronunciation']
        return None
    
    def get_audio_field_enhanced(self, word, oxford_data, media_folder):
        """
        Get enhanced audio field using Oxford Dictionary data
        
        Args:
            word: The word
            oxford_data: Oxford dictionary data if available
            media_folder: Anki's media folder path
            
        Returns:
            Audio field string for Anki
        """
        # Try to use Oxford audio if available
        if oxford_data and oxford_data.get('audio_url') and media_folder:
            try:
                filename = download_audio_file(oxford_data['audio_url'], word, media_folder)
                if filename:
                    return f"[sound:{filename}]"
            except Exception as e:
                print(f"Failed to download Oxford audio for '{word}': {e}")
        
        # Fallback to generic audio format
        safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return f"[sound:{safe_word}.mp3]"

def ensure_dependencies_installed():
    """
    Ensure required dependencies are installed for enhanced functionality
    """
    dependencies = ['requests', 'beautifulsoup4']
    
    for package in dependencies:
        try:
            if package == 'beautifulsoup4':
                import bs4
            else:
                __import__(package)
        except ImportError:
            import subprocess
            import sys
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"Could not install {package} automatically. Please install it manually.")
                return False
    return True

# Ensure dependencies are installed
ensure_dependencies_installed()
