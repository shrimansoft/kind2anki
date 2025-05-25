# 🔧 PyQt6 Compatibility Fix Applied

## ✅ Issues Resolved
**Problem 1**: `ModuleNotFoundError: No module named 'PyQt5'` in Anki 25.x
**Problem 2**: `AttributeError: type object 'Qt' has no attribute 'Window'`
**Root Cause**: Anki 25.x uses PyQt6 with different enum structures than PyQt5
**Solution**: Updated all Qt imports and enum references to use Anki's `aqt.qt` module

## 🔄 Changes Made

### 1. Updated Main Module (`__init__.py`)
- Removed: `from PyQt5.QtCore import QThread, pyqtSignal`
- Added: All Qt classes now imported via `from aqt.qt import *`
- Added: Simple translation function `_ = lambda text: text` for compatibility
- Fixed: `Qt.Window` → `Qt.WindowType.Window` for PyQt6 enum structure

### 2. Recreated UI Module (`kind2anki_ui.py`)
**Before (PyQt5):**
```python
from PyQt5 import QtCore, QtGui, QtWidgets
```

**After (Anki's PyQt6):**
```python
from aqt.qt import *
```

### 3. Updated Qt Enum References
**PyQt5 → PyQt6 Enum Changes:**
- `Qt.Window` → `Qt.WindowType.Window`
- `QtCore.Qt.Horizontal` → `Qt.Orientation.Horizontal`  
- `QtWidgets.QSizePolicy.Preferred` → `QSizePolicy.Policy.Preferred`
- `QtWidgets.QDialogButtonBox.Close` → `QDialogButtonBox.StandardButton.Close`

### 4. Updated Qt Class References
- `QtWidgets.QDialog` → `QDialog`
- `QtCore.Qt.Horizontal` → `Qt.Orientation.Horizontal`
- `QtWidgets.QSizePolicy.Preferred` → `QSizePolicy.Policy.Preferred`
- All other Qt classes now use direct imports

## 📦 Updated Package Details
- **File**: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
- **Size**: 13,291 bytes (includes PyQt6 fixes)
- **Validation**: ✅ All files present and valid
- **Compatibility**: Anki 25.x (PyQt6) - Both import and enum issues fixed

## 🧪 Ready for Testing
The addon should now load properly in Anki 25.x without the PyQt5 import error. 

### Installation Steps:
1. **Remove old version** (if installed): Tools → Add-ons → Select old kind2anki → Remove
2. **Install new version**: Tools → Add-ons → Install from file...
3. **Select**: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
4. **Restart Anki**
5. **Test**: Tools → kind2anki (should open without errors)

## 🔍 What to Test Next
1. **Basic Loading**: Addon appears in Tools menu without errors
2. **UI Display**: Dialog opens with all controls visible including "Include dictionary definition" checkbox
3. **File Selection**: Can browse and select Kindle vocab.db file
4. **Import Process**: Import completes without Python errors
5. **Enhanced Features**: Dictionary definitions and rich card fields work

## 🚨 If Issues Persist
If you encounter other errors, check:
1. **Anki Version**: Ensure you're running Anki 25.x or later
2. **Python Console**: Tools → Add-ons → [addon] → "View Files" → Check console for errors
3. **Dependencies**: The addon will attempt to install `requests` module automatically

## 📋 Enhanced Features Available
✅ **Dictionary Integration** - Free API lookups  
✅ **Audio URLs** - Language-specific pronunciation links  
✅ **Rich Cards** - 7-field format (Word, Reading, Definition, Sentence, Audio, Frequency, BookName)  
✅ **Multi-language Support** - Automatic language detection  
✅ **Enhanced UI** - New dictionary option checkbox
