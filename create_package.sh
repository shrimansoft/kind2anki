#!/bin/bash
# Create Anki addon package for kind2anki

echo "Creating kind2anki.ankiaddon package..."

# Remove any existing package
rm -f kind2anki.ankiaddon

# Create the addon package
zip -r kind2anki.ankiaddon manifest.json __init__.py kind2anki -x "**/__pycache__/*" "**/*.pyc" "**/.*"

if [ $? -eq 0 ]; then
    echo "Package created successfully: kind2anki.ankiaddon"
    ls -la kind2anki.ankiaddon
else
    echo "Error creating package"
    exit 1
fi