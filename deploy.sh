#!/bin/bash

# Deploy script for Alter Ego project
# Usage: ./deploy.sh "commit message"

# Check if commit message is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a commit message"
    echo "Usage: ./deploy.sh \"commit message\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "🚀 Starting deployment process..."
echo "Commit message: $COMMIT_MESSAGE"
echo ""

# Function to check if command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 completed successfully"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Step 1: Switch to develop branch
echo "📝 Step 1: Switching to develop branch..."
git checkout develop
check_status "Switch to develop"

# Step 2: Add all changes
echo "📝 Step 2: Adding all changes..."
git add .
check_status "Add changes"

# Step 3: Commit with provided message
echo "📝 Step 3: Committing changes..."
git commit -m "$COMMIT_MESSAGE"
check_status "Commit changes"

# Step 4: Push to develop
echo "📝 Step 4: Pushing to develop..."
git push origin develop
check_status "Push to develop"

# Step 5: Switch to master
echo "📝 Step 5: Switching to master branch..."
git switch master
check_status "Switch to master"

# Step 6: Merge develop into master
echo "📝 Step 6: Merging develop into master..."
git merge develop
check_status "Merge develop into master"

# Step 7: Push master
echo "📝 Step 7: Pushing master..."
git push origin master
check_status "Push master"

# Step 8: Activate virtual environment and deploy
echo "📝 Step 8: Activating virtual environment..."
source .venv/Scripts/activate
check_status "Activate virtual environment"

# Step 9: Deploy with Gradio
echo "📝 Step 9: Deploying with Gradio..."
gradio deploy
check_status "Gradio deployment"

echo ""
echo "🎉 Deployment completed successfully!"
echo "Your changes have been committed, pushed, and deployed." 