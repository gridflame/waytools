#!/bin/bash
# Setup GitHub remote for way.tools project

echo "GitHub Account Setup for way.tools"
echo "==================================="
echo ""

read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your GitHub email: " GITHUB_EMAIL
read -p "Enter repository name (default: waytools): " REPO_NAME
REPO_NAME=${REPO_NAME:-waytools}

echo ""
echo "Configuring Git..."
git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_EMAIL"

echo ""
echo "Setting up remote..."
# Remove existing remote if it exists
git remote remove origin 2>/dev/null

# Add new remote
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "✅ Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Create the repository '$REPO_NAME' on GitHub (if it doesn't exist)"
echo "2. Push your code:"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "   git push -u origin main"
echo ""
echo "Note: GitHub may ask for a Personal Access Token instead of password"

