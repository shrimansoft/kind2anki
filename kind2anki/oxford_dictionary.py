# Oxford Learner's Dictionary integration for Kind2Anki
# Adapted from AutoDefine Oxford Learner's Dictionary repository
# https://github.com/artyompetrov/AutoDefine_oxfordlearnersdictionaries

import os
import pathlib
import requests
from bs4 import BeautifulSoup as soup
from http import cookiejar


class WordNotFound(Exception):
    """Word not found in dictionary (404 status code)"""
    pass


class BlockAll(cookiejar.CookiePolicy):
    """Policy to block cookies"""
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args: False
    netscape = True
    rfc2965 = hide_cookie2 = False


class OxfordDictionary:
    """Oxford Learner's Dictionary API for retrieving word information"""
    
    # CSS Selectors for extracting data from Oxford pages
    entry_selector = '#entryContent > .entry'
    header_selector = '.top-container'
    title_selector = header_selector + ' .headword'
    wordform_selector = header_selector + ' .pos'
    property_global_selector = header_selector + ' .grammar'
    
    # Pronunciation selectors
    br_pronounce_selector = '[geo=br] .phon'
    am_pronounce_selector = '[geo=n_am] .phon'
    br_pronounce_audio_mp3_selector = '[geo=br] [data-src-mp3]'
    am_pronounce_audio_mp3_selector = '[geo=n_am] [data-src-mp3]'
    
    # Definition and example selectors
    definition_body_selector = '.senses_multiple'
    definition_body_selector_single = '.sense_single'
    definitions_selector = '.senses_multiple .sense > .def'
    examples_selector = '.senses_multiple .sense > .examples .x'
    
    soup_data = None
    
    @classmethod
    def get_url(cls, word, is_search=True):
        """Get URL for word definition"""
        if is_search:
            baseurl = 'https://www.oxfordlearnersdictionaries.com/search/english/?q='
        else:
            baseurl = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
        return baseurl + word.replace(" ", "-").lower()
    
    @classmethod
    def get_word_info(cls, word):
        """
        Get comprehensive word information from Oxford Learner's Dictionary
        
        Args:
            word: The word to look up
            
        Returns:
            Dictionary containing word information or None if not found
        """
        try:
            # Set up request session with cookie blocking
            req = requests.Session()
            req.cookies.set_policy(BlockAll())
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # First try direct search
            word_to_search = word.replace(" ", "-").lower()
            page_html = req.get(cls.get_url(word_to_search), headers=headers, timeout=10)
            
            if page_html.status_code == 404:
                raise WordNotFound(f"Word '{word}' not found")
            
            cls.soup_data = soup(page_html.content, 'html.parser')
            
            # Check if "No exact match found" message exists
            no_exact = cls.soup_data.select_one('#search-results > h1')
            if no_exact is not None and no_exact.string and no_exact.string.startswith('No exact match found'):
                raise WordNotFound(f"No exact match found for '{word}'")
            
            # Clean up unwanted content
            cls._clean_soup_data()
            
            # Extract word information
            word_info = {
                'name': cls._get_name(),
                'wordform': cls._get_wordform(),
                'pronunciations': cls._get_pronunciations(),
                'definitions': cls._get_definitions_full(),
                'examples': cls._get_examples(),
                'audio_urls': cls._get_audio_urls()
            }
            
            return word_info
            
        except requests.RequestException as e:
            print(f"Network error looking up '{word}': {e}")
            return None
        except Exception as e:
            print(f"Error looking up '{word}': {e}")
            return None
    
    @classmethod
    def _clean_soup_data(cls):
        """Remove unnecessary tags to prevent false positive results"""
        selectors_to_remove = [
            '[title="Oxford Collocations Dictionary"]',
            '[title="British/American"]',
            '[title="Express Yourself"]',
            '[title="Collocations"]',
            '[title="Word Origin"]'
        ]
        
        for selector in selectors_to_remove:
            try:
                for tag in cls.soup_data.select(selector):
                    tag.decompose()
            except:
                pass
    
    @classmethod
    def _get_name(cls):
        """Get the word name"""
        if cls.soup_data is None:
            return None
        
        try:
            name = cls.soup_data.select(cls.title_selector)[0]
            # Remove span tags but keep text
            for span_tag in name.select('span'):
                span_tag.replace_with('')
            return name.text.strip()
        except (IndexError, AttributeError):
            return None
    
    @classmethod
    def _get_wordform(cls):
        """Get word form (noun, verb, adjective, etc.)"""
        if cls.soup_data is None:
            return None
        
        try:
            return cls.soup_data.select(cls.wordform_selector)[0].text.strip()
        except (IndexError, AttributeError):
            return None
    
    @classmethod
    def _get_pronunciations(cls):
        """Get pronunciation information"""
        if cls.soup_data is None:
            return None
        
        pronunciations = {}
        
        try:
            # British pronunciation
            br_phon = cls.soup_data.select(cls.br_pronounce_selector)
            if br_phon:
                pronunciations['british'] = br_phon[0].text.strip()
        except (IndexError, AttributeError):
            pass
        
        try:
            # American pronunciation
            am_phon = cls.soup_data.select(cls.am_pronounce_selector)
            if am_phon:
                pronunciations['american'] = am_phon[0].text.strip()
        except (IndexError, AttributeError):
            pass
        
        return pronunciations if pronunciations else None
    
    @classmethod
    def _get_audio_urls(cls):
        """Get audio URLs for pronunciation"""
        if cls.soup_data is None:
            return None
        
        audio_urls = {}
        
        try:
            # British audio
            br_audio = cls.soup_data.select(cls.br_pronounce_audio_mp3_selector)
            if br_audio and 'data-src-mp3' in br_audio[0].attrs:
                audio_urls['british'] = br_audio[0].attrs['data-src-mp3']
        except (IndexError, AttributeError):
            pass
        
        try:
            # American audio
            am_audio = cls.soup_data.select(cls.am_pronounce_audio_mp3_selector)
            if am_audio and 'data-src-mp3' in am_audio[0].attrs:
                audio_urls['american'] = am_audio[0].attrs['data-src-mp3']
        except (IndexError, AttributeError):
            pass
        
        return audio_urls if audio_urls else None
    
    @classmethod
    def _get_definitions_full(cls):
        """Get comprehensive definitions with examples"""
        if cls.soup_data is None:
            return None
        
        definitions = []
        
        try:
            # Try multiple definition selectors
            definition_tags = cls.soup_data.select('.sense')
            
            for def_tag in definition_tags:
                definition_info = {}
                
                # Get definition text
                try:
                    def_text = def_tag.select('.def')[0].text.strip()
                    definition_info['definition'] = def_text
                except (IndexError, AttributeError):
                    continue
                
                # Get grammar/property information
                try:
                    grammar = def_tag.select('.grammar')[0].text.strip()
                    definition_info['grammar'] = grammar
                except (IndexError, AttributeError):
                    pass
                
                # Get labels (informal, formal, etc.)
                try:
                    labels = def_tag.select('.labels')[0].text.strip()
                    definition_info['labels'] = labels
                except (IndexError, AttributeError):
                    pass
                
                # Get examples
                examples = []
                try:
                    example_tags = def_tag.select('.examples .x')
                    for ex_tag in example_tags:
                        examples.append(ex_tag.text.strip())
                    if examples:
                        definition_info['examples'] = examples
                except (IndexError, AttributeError):
                    pass
                
                definitions.append(definition_info)
        
        except Exception as e:
            print(f"Error extracting definitions: {e}")
        
        return definitions if definitions else None
    
    @classmethod
    def _get_examples(cls):
        """Get all examples (simple list)"""
        if cls.soup_data is None:
            return None
        
        examples = []
        try:
            example_tags = cls.soup_data.select(cls.examples_selector)
            for tag in example_tags:
                examples.append(tag.text.strip())
        except (IndexError, AttributeError):
            pass
        
        return examples if examples else None


def lookup_oxford_dictionary(word, max_definitions=3, max_examples_per_def=2):
    """
    Main function to lookup a word in Oxford Learner's Dictionary
    
    Args:
        word: Word to look up
        max_definitions: Maximum number of definitions to return
        max_examples_per_def: Maximum examples per definition
        
    Returns:
        Dictionary with formatted word information
    """
    try:
        word_info = OxfordDictionary.get_word_info(word)
        
        if not word_info:
            return None
        
        # Format the response for Kind2Anki
        result = {
            'word': word_info.get('name', word),
            'word_type': word_info.get('wordform', ''),
            'pronunciation': '',
            'definitions': [],
            'examples': [],
            'audio_url': ''
        }
        
        # Format pronunciation (prefer American, fallback to British)
        pronunciations = word_info.get('pronunciations', {})
        if pronunciations:
            if 'american' in pronunciations:
                result['pronunciation'] = f"/{pronunciations['american']}/"
            elif 'british' in pronunciations:
                result['pronunciation'] = f"/{pronunciations['british']}/"
        
        # Format definitions with examples
        definitions_data = word_info.get('definitions', [])
        if definitions_data:
            for i, def_info in enumerate(definitions_data[:max_definitions]):
                def_text = def_info.get('definition', '')
                
                # Add grammar/labels if available
                if 'grammar' in def_info:
                    def_text = f"({def_info['grammar']}) {def_text}"
                if 'labels' in def_info:
                    def_text = f"{def_info['labels']} {def_text}"
                
                result['definitions'].append(def_text)
                
                # Add examples for this definition
                def_examples = def_info.get('examples', [])
                for example in def_examples[:max_examples_per_def]:
                    result['examples'].append(example)
        
        # Get audio URL (prefer American)
        audio_urls = word_info.get('audio_urls', {})
        if audio_urls:
            if 'american' in audio_urls:
                result['audio_url'] = audio_urls['american']
            elif 'british' in audio_urls:
                result['audio_url'] = audio_urls['british']
        
        return result
        
    except Exception as e:
        print(f"Error in lookup_oxford_dictionary for '{word}': {e}")
        return None


def download_audio_file(audio_url, word, media_folder):
    """
    Download audio file to Anki's media folder
    
    Args:
        audio_url: URL of the audio file
        word: Word for naming the file
        media_folder: Path to Anki's media folder
        
    Returns:
        Filename of the downloaded audio file or None if failed
    """
    if not audio_url:
        return None
    
    try:
        # Create safe filename
        safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_word}_oxford.mp3"
        filepath = os.path.join(media_folder, filename)
        
        # Don't download if file already exists
        if os.path.exists(filepath):
            return filename
        
        # Download the audio file
        req = requests.Session()
        req.cookies.set_policy(BlockAll())
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = req.get(audio_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Save to media folder
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filename
        
    except Exception as e:
        print(f"Error downloading audio for '{word}': {e}")
        return None
