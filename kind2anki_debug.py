# Kind2Anki Debug Version - Enhanced Error Logging
# This file contains additional debugging code for testing the PyQt6 compatibility

# Import testing function
def test_imports():
    """Test all critical imports and report any issues"""
    import_results = {}
    
    try:
        from aqt.qt import *
        import_results['aqt.qt'] = "✅ Success"
    except Exception as e:
        import_results['aqt.qt'] = f"❌ Failed: {str(e)}"
    
    try:
        from aqt import mw
        import_results['aqt.mw'] = "✅ Success"
    except Exception as e:
        import_results['aqt.mw'] = f"❌ Failed: {str(e)}"
    
    try:
        from aqt.deckchooser import DeckChooser
        import_results['DeckChooser'] = "✅ Success"
    except Exception as e:
        import_results['DeckChooser'] = f"❌ Failed: {str(e)}"
    
    try:
        from anki.importing import TextImporter
        import_results['TextImporter'] = "✅ Success"
    except Exception as e:
        import_results['TextImporter'] = f"❌ Failed: {str(e)}"
    
    return import_results

# Qt Version checking function
def check_qt_versions():
    """Check Qt and PyQt versions for compatibility"""
    version_info = {}
    
    try:
        from aqt.qt import QT_VERSION_STR, PYQT_VERSION_STR
        version_info['Qt Version'] = QT_VERSION_STR
        version_info['PyQt Version'] = PYQT_VERSION_STR
    except Exception as e:
        version_info['Version Check'] = f"❌ Failed: {str(e)}"
    
    try:
        from aqt.qt import Qt
        # Test enum access
        window_type = Qt.WindowType.Window
        version_info['Enum Test'] = "✅ Qt.WindowType.Window accessible"
    except Exception as e:
        version_info['Enum Test'] = f"❌ Failed: {str(e)}"
    
    return version_info

# UI Component testing
def test_ui_components():
    """Test critical UI components for PyQt6 compatibility"""
    ui_results = {}
    
    try:
        from aqt.qt import QDialog, QPushButton, QDialogButtonBox
        ui_results['Basic Widgets'] = "✅ Success"
    except Exception as e:
        ui_results['Basic Widgets'] = f"❌ Failed: {str(e)}"
    
    try:
        from aqt.qt import QThread, pyqtSignal
        ui_results['Threading'] = "✅ Success"
    except Exception as e:
        ui_results['Threading'] = f"❌ Failed: {str(e)}"
    
    try:
        from kind2anki.kind2anki import kind2anki_ui
        ui_results['Custom UI'] = "✅ Success"
    except Exception as e:
        ui_results['Custom UI'] = f"❌ Failed: {str(e)}"
    
    return ui_results

# Enhanced error logging for the main dialog
class DebugKind2AnkiDialog:
    """Debug version of Kind2AnkiDialog with extensive logging"""
    
    def __init__(self):
        self.debug_log = []
        self.log("🔍 Starting Kind2Anki Debug Session")
        
        # Test imports
        self.log("📦 Testing imports...")
        import_results = test_imports()
        for module, result in import_results.items():
            self.log(f"  {module}: {result}")
        
        # Test Qt versions
        self.log("🔧 Checking Qt versions...")
        version_info = check_qt_versions()
        for component, info in version_info.items():
            self.log(f"  {component}: {info}")
        
        # Test UI components
        self.log("🎨 Testing UI components...")
        ui_results = test_ui_components()
        for component, result in ui_results.items():
            self.log(f"  {component}: {result}")
    
    def log(self, message):
        """Add message to debug log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.debug_log.append(log_entry)
        print(log_entry)  # Also print to console
    
    def get_debug_report(self):
        """Return complete debug report"""
        return "\n".join(self.debug_log)

# Function to run comprehensive debug test
def run_debug_test():
    """Run complete debug test and return results"""
    try:
        debug_dialog = DebugKind2AnkiDialog()
        return debug_dialog.get_debug_report()
    except Exception as e:
        return f"❌ Debug test failed: {str(e)}"

# Debug console commands for manual testing
DEBUG_COMMANDS = """
# Run these commands in Anki's Debug Console to test the addon:

# 1. Test imports
from kind2anki_debug import test_imports
print("Import Test Results:")
for module, result in test_imports().items():
    print(f"  {module}: {result}")

# 2. Check Qt versions
from kind2anki_debug import check_qt_versions
print("\\nQt Version Info:")
for component, info in check_qt_versions().items():
    print(f"  {component}: {info}")

# 3. Test UI components
from kind2anki_debug import test_ui_components
print("\\nUI Component Test:")
for component, result in test_ui_components().items():
    print(f"  {component}: {result}")

# 4. Run complete debug test
from kind2anki_debug import run_debug_test
print("\\nComplete Debug Report:")
print(run_debug_test())

# 5. Test dialog creation
try:
    from kind2anki import Kind2AnkiDialog
    print("\\n✅ Dialog class import successful")
    # Note: Don't create dialog in debug console as it will block
except Exception as e:
    print(f"\\n❌ Dialog class import failed: {e}")

# 6. Test individual Qt components
try:
    from aqt.qt import Qt, QDialog, QPushButton, QDialogButtonBox
    print("\\n✅ Qt components accessible")
    print(f"Window type enum: {Qt.WindowType.Window}")
    print(f"Button role enum: {QDialogButtonBox.ButtonRole.AcceptRole}")
except Exception as e:
    print(f"\\n❌ Qt component test failed: {e}")
"""

if __name__ == "__main__":
    print("Kind2Anki Debug Module Loaded")
    print("Use the DEBUG_COMMANDS for manual testing")
    print(DEBUG_COMMANDS)
