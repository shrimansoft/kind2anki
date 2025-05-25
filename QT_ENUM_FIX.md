# 🔧 Qt.Window Enum Fix Applied

## ✅ **FIXED**: Qt Enum Attribute Error
**Error**: `AttributeError: type object 'Qt' has no attribute 'Window'`  
**Location**: `__init__.py` line 81 in `QDialog.__init__(self, mw, Qt.Window)`  
**Root Cause**: PyQt6 changed enum structure from PyQt5  

## 🛠️ **Fix Applied**
```python
# Before (PyQt5):
QDialog.__init__(self, mw, Qt.Window)

# After (PyQt6):
QDialog.__init__(self, mw, Qt.WindowType.Window)
```

## 📦 **Updated Package Ready**
- **Location**: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
- **Size**: 13,291 bytes
- **Status**: ✅ Both PyQt import and enum issues fixed

## 🚀 **Installation Instructions**
1. **Remove previous version**: Tools → Add-ons → Select kind2anki → Remove
2. **Install updated version**: Tools → Add-ons → Install from file...
3. **Select**: `/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon`
4. **Restart Anki**
5. **Test**: Tools → kind2anki (should now open without errors)

## 🎯 **Should Now Work**
The addon should now:
- ✅ Load without PyQt5 import errors
- ✅ Initialize dialog without Qt enum errors  
- ✅ Display enhanced UI with dictionary checkbox
- ✅ Function with all enhanced features

**Ready for full testing!** 🎉
