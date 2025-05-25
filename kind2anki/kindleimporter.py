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
    Lookup word in Oxford Advanced Learner's Dictionary API
    Returns dictionary definition if available
    """
    try:
        # Using a free dictionary API as an example
        # In a real implementation, you would use Oxford or Webster API with proper authentication
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data or not isinstance(data, list):
                return ""
                
            result = "<div class='dictionary-definition'>"
            # Extract definitions
            for entry in data:
                if "meanings" in entry:
                    for meaning in entry["meanings"]:
                        if "partOfSpeech" in meaning:
                            result += f"<p><i>{meaning['partOfSpeech']}</i></p>"
                        if "definitions" in meaning:
                            result += "<ul>"
                            for definition in meaning["definitions"]:
                                result += f"<li>{definition['definition']}</li>"
                                if "example" in definition:
                                    result += f"<p><i>Example: {definition['example']}</i></p>"
                            result += "</ul>"
            result += "</div>"
            return result
        return ""
    except Exception:
        return ""


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
                "sentence": self.sentences.get(word_key, ""),
                "frequency": self.frequencies.get(word_key, ""),
                "book_name": self.book_names.get(word_key, "Unknown Book"),
                "audio_url": self.audio_urls.get(word_key, "")
            }
            
            # Add sentence/usage if enabled
            if self.includeUsage and card_data["sentence"]:
                # Replace the target word with underscores for fill-in-the-blank style
                # Handle case-insensitive replacement and word variations
                sentence = card_data["sentence"]
                word_lower = word.lower()
                
                # Split sentence into words to find exact matches
                words_in_sentence = sentence.split()
                for i, sentence_word in enumerate(words_in_sentence):
                    # Remove punctuation for comparison
                    clean_word = sentence_word.strip('.,!?;:"()[]').lower()
                    if clean_word == word_lower or clean_word.startswith(word_lower):
                        # Preserve original punctuation but replace the word part
                        punctuation = ''.join(c for c in sentence_word if not c.isalnum())
                        words_in_sentence[i] = "_____" + punctuation
                        break
                
                card_data["sentence"] = " ".join(words_in_sentence).replace(";", ",")
            else:
                card_data["sentence"] = ""
            
            # Add translation if enabled
            if self.doTranslate:
                try:
                    card_data["translated_definition"] = translate_func(word)
                except Exception as e:
                    card_data["translated_definition"] = "cannot translate"
            
            # Add dictionary lookup if enabled
            if self.includeDictionary:
                try:
                    # For languages other than English, we'd need a different API
                    # Here we assume English for the dictionary API
                    if self.langs.get(word_key, "en") == "en":
                        card_data["dictionary_definition"] = lookupDictionary(word)
                    else:
                        # For non-English words, try to get a translation first then lookup
                        try:
                            eng_word = translate(word, from_lang=self.langs.get(word_key, "en"), to_lang="en")
                            card_data["dictionary_definition"] = lookupDictionary(eng_word)
                        except:
                            card_data["dictionary_definition"] = ""
                except Exception:
                    card_data["dictionary_definition"] = ""
            
            translated_data.append(card_data)
            
        return translated_data

    def createTemporaryFile(self):
        if len(self.words) == 0:
            return None
            
        path = os.path.join(tempfile.gettempdir(), "kind2anki_temp.txt")
        
        with codecs.open(path, "w", encoding="utf-8") as f:
            # Write all card fields into the file
            for card_data in self.translated:
                # Combine definitions for the Def field
                definition = card_data["translated_definition"]
                if card_data["dictionary_definition"]:
                    definition += "<hr>" + card_data["dictionary_definition"]
                
                # Detect word type (very basic implementation)
                word_type = self.detect_word_type(card_data["word"])
                
                # Map to user's 9-field note type:
                # 1:Word, 2:Word Type, 3:Phonetic, 4:Example, 5:Sound, 6:Image, 7:Def, 8:Content, 9:Copyright
                fields = [
                    card_data["word"],                          # 1: Word
                    word_type,                                  # 2: Word Type
                    card_data["reading"],                       # 3: Phonetic
                    card_data["sentence"],                      # 4: Example (with _____ replacing word)
                    f"[sound:{card_data['word']}.mp3]",        # 5: Sound
                    "",                                         # 6: Image (intentionally empty)
                    definition,                                 # 7: Def
                    f"Source: {card_data['book_name']}",       # 8: Content
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

def ensure_dependencies_installed():
    try:
        import requests
    except ImportError:
        import subprocess
        import sys
        # Install requests if not available
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        
        try:
            import requests
        except ImportError:
            print("Could not install requests module automatically. Please install it manually.")
            return False
    return True

# Ensure dependencies are installed
ensure_dependencies_installed()
