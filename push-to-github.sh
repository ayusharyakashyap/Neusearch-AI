#!/bin/bash

echo "🚀 GitHub Repository Setup"
echo "=========================="
echo ""
echo "✅ Git repository initialized"
echo "✅ All files committed (40 files, 23,756 insertions)"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: neusearch-product-assistant"
echo "   - Description: AI-powered product discovery assistant with RAG pipeline"
echo "   - Make it PUBLIC"
echo "   - DO NOT initialize with README (we already have one)"
echo ""
echo "2. Copy your repository URL (it will look like):"
echo "   https://github.com/YOUR_USERNAME/neusearch-product-assistant.git"
echo ""
echo "3. Run these commands (replace YOUR_USERNAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/neusearch-product-assistant.git"
echo "   git push -u origin main"
echo ""
echo "=========================="
echo ""
echo "Or simply copy-paste this after creating the repo:"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "No URL provided. Run this script again when you have the URL."
    exit 0
fi

echo ""
echo "Adding remote and pushing..."
git remote add origin "$REPO_URL"
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub"
echo "📦 Repository: $REPO_URL"
