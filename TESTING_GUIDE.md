# Kind2Anki PyQt6 Testing Guide

## Overview
This guide provides comprehensive testing procedures for the PyQt6-compatible version of the Kind2Anki addon for Anki 25.x.

## Prerequisites
- Anki 25.x installed
- Kindle vocabulary database file (vocab.db)
- Sample vocabulary data in your Kindle database

## Installation Testing

### 1. Initial Installation
1. Close Anki completely
2. Install the addon package: `kind2anki.ankiaddon`
3. Start Anki
4. Check the addon loads without errors

**Expected Behavior**: 
- No error dialogs on startup
- "kind2anki" appears in Tools menu

**Debug Steps if Failed**:
```
1. Open Anki Debug Console (Tools > Debugging > Debug Console)
2. Check for error messages
3. Run: `print([addon for addon in mw.addonManager.addons() if 'kind2anki' in addon])`
4. If addon not listed, check installation
```

### 2. Menu Item Testing
1. Go to Tools menu
2. Look for "kind2anki" option
3. Click on it

**Expected Behavior**: 
- Dialog opens without errors
- All UI elements are visible and properly aligned

## Core Functionality Testing

### 3. Database Selection
1. Click "kind2anki" from Tools menu
2. Test database file selection

**Test Cases**:
- **Valid Kindle DB**: Select actual vocab.db file
- **Invalid File**: Select non-database file
- **Cancel Selection**: Click cancel in file dialog

**Expected Behaviors**:
- Valid DB: Dialog continues, no error
- Invalid File: Error message "Selected file is not a DB"
- Cancel: Dialog closes with "DB file not selected, exiting"

### 4. UI Component Testing

#### Language Selection
- Test dropdown has multiple language options
- Default selection is reasonable
- Selection changes properly

#### Import Options
Test all checkboxes:
- ✅ Include Usage Sentences
- ✅ Translate Words  
- ✅ Include Dictionary Definitions

#### Days Input
- Default value based on last run
- Can be modified
- Accepts reasonable range (1-365)

#### Deck Selection
- Deck chooser appears
- Can select existing decks
- Can create new deck

## Advanced Feature Testing

### 5. Dictionary Integration
1. Enable "Include Dictionary Definitions"
2. Select words that should have dictionary entries
3. Import and verify cards contain definitions

**Debug Commands**:
```python
# In Debug Console, after import
cards = mw.col.find_cards("deck:YourDeckName")
for card_id in cards[:5]:  # Check first 5 cards
    card = mw.col.get_card(card_id)
    note = card.note()
    print(f"Definition field: {note['Definition']}")
```

### 6. Audio URL Generation
1. Import words with audio URLs enabled
2. Check that audio URLs are properly formatted

**Debug Commands**:
```python
# Check audio field content
cards = mw.col.find_cards("deck:YourDeckName")
for card_id in cards[:3]:
    card = mw.col.get_card(card_id)
    note = card.note()
    print(f"Audio field: {note['Audio']}")
```

### 7. Threading and Progress
1. Start import with large dataset
2. Verify progress bar appears
3. Check UI remains responsive
4. Verify import completes successfully

## Error Testing

### 8. Network Connectivity
1. Disconnect internet
2. Try importing with translation enabled
3. Should handle gracefully

**Expected**: "Cannot connect" error message

### 9. File System Errors
1. Try selecting non-existent file
2. Try accessing read-only locations
3. Test with corrupted database

### 10. Memory and Performance
1. Import large vocabulary sets (>1000 words)
2. Monitor memory usage
3. Check for memory leaks after multiple imports

## Debug Console Testing

### Essential Debug Commands

```python
# Check addon status
print(mw.addonManager.isEnabled("kind2anki"))

# Inspect loaded modules
import sys
kind2anki_modules = [mod for mod in sys.modules if 'kind2anki' in mod]
print(kind2anki_modules)

# Test dialog creation manually
from kind2anki import Kind2AnkiDialog
dialog = Kind2AnkiDialog()

# Check PyQt6 compatibility
from aqt.qt import *
print(f"Qt version: {QT_VERSION_STR}")
print(f"PyQt version: {PYQT_VERSION_STR}")

# Test thread functionality
from kind2anki import ThreadTranslate
thread = ThreadTranslate()
print(f"Thread created: {thread}")

# Check UI components
from kind2anki.kind2anki import kind2anki_ui
ui = kind2anki_ui.Ui_kind2ankiDialog()
print(f"UI class loaded: {ui}")
```

## Regression Testing

### 11. Card Field Verification
After successful import, verify all fields are populated:

```python
# Get latest imported cards
cards = mw.col.find_cards("added:1")  # Cards added today
if cards:
    card = mw.col.get_card(cards[0])
    note = card.note()
    
    # Check all expected fields
    fields = ['Word', 'Reading', 'Definition', 'Sentence', 'Audio', 'Frequency', 'BookName']
    for field in fields:
        if field in note:
            print(f"{field}: {note[field][:50]}...")  # First 50 chars
        else:
            print(f"MISSING: {field}")
```

### 12. Import Mode Testing
Test all import modes:
1. Update existing notes
2. Create new notes only
3. Skip duplicates

## Performance Benchmarks

### 13. Timing Tests
```python
import time

# Time the import process
start_time = time.time()
# Perform import...
end_time = time.time()
print(f"Import time: {end_time - start_time:.2f} seconds")

# Memory usage (requires psutil)
import psutil
import os
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

## Troubleshooting

### Common Issues and Solutions

1. **Import Error on Startup**
   - Check PyQt6 compatibility
   - Verify all files are present
   - Check file permissions

2. **Database Connection Issues**
   - Verify database file exists
   - Check file permissions
   - Ensure database is valid SQLite format

3. **Translation Service Failures**
   - Check internet connection
   - Verify API endpoints are accessible
   - Test with smaller batches

4. **UI Layout Problems**
   - Check Qt version compatibility
   - Verify all UI files are PyQt6 compatible
   - Test on different screen resolutions

## Success Criteria

✅ **Installation**: Addon loads without errors
✅ **UI Display**: All dialogs render correctly
✅ **Database Access**: Can read Kindle vocabulary files
✅ **Import Process**: Successfully creates Anki cards
✅ **Field Population**: All 7 fields contain appropriate data
✅ **Error Handling**: Graceful handling of edge cases
✅ **Performance**: Reasonable speed for typical datasets
✅ **Memory Management**: No memory leaks during extended use

## Test Results Template

```
Date: ___________
Anki Version: ___________
Operating System: ___________
Test Database Size: ___________ words

[ ] Installation successful
[ ] Menu item appears
[ ] Dialog opens correctly
[ ] Database selection works
[ ] Import process completes
[ ] Cards created with all fields
[ ] No memory leaks detected
[ ] Error handling appropriate

Issues Found:
_________________________________
_________________________________

Performance Notes:
_________________________________
_________________________________
```

## Contact and Support

If issues are found during testing:
1. Document the exact error message
2. Note the testing environment details
3. Save debug console output
4. Record steps to reproduce

This comprehensive testing ensures the PyQt6 compatibility fixes work correctly across all features of the enhanced Kind2Anki addon.
