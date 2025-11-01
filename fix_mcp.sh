#!/bin/bash
# Fix MCP npm permission issues

echo "🔧 Fixing npm permissions..."
sudo chown -R 501:20 "/Users/keegandewitt/.npm"

echo "🧹 Cleaning npm cache..."
sudo rm -rf /Users/keegandewitt/.npm/_cacache
sudo rm -rf /Users/keegandewitt/.npm/_logs

echo "📦 Creating fresh cache..."
/Users/keegandewitt/.nvm/versions/node/v22.20.0/bin/npm cache clean --force

echo "✅ Done! Now:"
echo "   1. Quit Cursor (Cmd+Q)"
echo "   2. Reopen Cursor"
echo "   3. MCPs should connect reliably"



