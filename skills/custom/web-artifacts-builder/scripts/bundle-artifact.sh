#!/bin/bash
set -e

echo "📦 Bundling React app to single HTML..."

if [ ! -f "package.json" ]; then
    echo "❌ No package.json found. Run from project root."
    exit 1
fi

if [ ! -f "index.html" ]; then
    echo "❌ No index.html found in project root."
    exit 1
fi

# Check pnpm
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm
fi

echo "📦 Installing bundling dependencies..."
pnpm add -D parcel @parcel/config-default html-inline

# Parcel config
if [ ! -f ".parcelrc" ]; then
    cat > .parcelrc << 'EOF'
{
  "extends": "@parcel/config-default"
}
EOF
fi

echo "🧹 Cleaning previous build..."
rm -rf dist bundle.html

echo "🔨 Building with Parcel..."
pnpm exec parcel build index.html --dist-dir dist --no-source-maps

echo "🎯 Inlining assets into single HTML..."
pnpm exec html-inline dist/index.html > bundle.html

FILE_SIZE=$(du -h bundle.html | cut -f1)
echo ""
echo "✅ Bundle complete! Output: bundle.html ($FILE_SIZE)"
echo "Open bundle.html in any browser to view."
