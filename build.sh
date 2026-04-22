#!/bin/bash
set -e

echo "🏗  Building data includes from _data/..."
python scripts/build.py

echo "📄 Building CV PDFs..."
python scripts/build_cv.py

echo "🇰🇷 Building Korean site..."
quarto render .

echo "🇺🇸 Building English site..."
cd en && quarto render . && cd ..

echo "✅ Done. Output structure:"
echo "   _site/ (Korean site)"
echo "   _site/en/ (English site)"
echo "   assets/cv_en.pdf · assets/cv_ko.pdf (CV PDFs)"
echo ""
echo "📁 Files generated:"
find _site -name "*.html" -type f | head -10
