#!/usr/bin/env python3
"""
Quick validation script for kind2anki addon package
"""

import zipfile
import json
import os

def validate_addon_package():
    package_path = "/Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon"
    
    if not os.path.exists(package_path):
        print("❌ Package file not found!")
        return False
    
    print(f"📦 Package found: {package_path}")
    print(f"📊 Size: {os.path.getsize(package_path):,} bytes")
    
    try:
        with zipfile.ZipFile(package_path, 'r') as zip_file:
            files = zip_file.namelist()
            
            # Check required files
            required_files = [
                'manifest.json',
                '__init__.py',
                'kind2anki/kindleimporter.py',
                'kind2anki/kind2anki_ui.py',
                'kind2anki/kind2anki_ui.ui'
            ]
            
            print("\n📋 File validation:")
            for file in required_files:
                if file in files:
                    print(f"✅ {file}")
                else:
                    print(f"❌ {file} - MISSING!")
                    return False
            
            # Validate manifest
            try:
                manifest_content = zip_file.read('manifest.json')
                manifest = json.loads(manifest_content)
                print(f"\n📄 Manifest validation:")
                print(f"✅ Package: {manifest.get('package', 'N/A')}")
                print(f"✅ Name: {manifest.get('name', 'N/A')}")
                print(f"✅ Description length: {len(manifest.get('description', ''))}")
            except Exception as e:
                print(f"❌ Manifest validation failed: {e}")
                return False
            
            print(f"\n📁 Total files: {len(files)}")
            print("✅ Package validation successful!")
            return True
            
    except Exception as e:
        print(f"❌ Package validation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Validating kind2anki addon package...\n")
    
    if validate_addon_package():
        print("\n🎉 Ready for installation in Anki!")
        print("\nNext steps:")
        print("1. Open Anki")
        print("2. Go to Tools → Add-ons")
        print("3. Click 'Install from file...'")
        print("4. Select: /Users/shrimankeshri/Documents/GitHub/kind2anki/kind2anki.ankiaddon")
        print("5. Restart Anki")
        print("6. Look for 'kind2anki' in Tools menu")
    else:
        print("\n❌ Package validation failed - check errors above")
