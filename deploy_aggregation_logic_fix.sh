#!/bin/bash

# Deploy Aggregation Logic Fix for Overall Status
# Fixes the logic issue where TransformerML saying "malicious" but overall status showing "CLEAN"

echo "🚀 Deploying Aggregation Logic Fix for Overall Status..."

# Navigate to the main Java application directory
cd /Users/bootnext-55/Downloads/malicious-url-detector\ 2

echo "📁 Current directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "src/main/java/com/example/malwaredetector/service/ComprehensiveMalwareDetectionService.java" ]; then
    echo "❌ Error: ComprehensiveMalwareDetectionService.java not found in current directory"
    exit 1
fi

# Check git status
echo "📊 Git status:"
git status --porcelain

# Add all changes
echo "➕ Adding changes..."
git add .

# Commit with descriptive message
echo "💾 Committing changes..."
git commit -m "Fix aggregation logic: Implement robust overall status determination

- Fixed logic where TransformerML 'malicious' was ignored in overall status
- Implemented intelligent aggregation strategy with 3 strategies:
  1. Check for any 'malicious' label with >30% confidence
  2. Check for high confidence content analysis issues (>50%)
  3. Count multiple suspicious indicators
- Added proper status escalation: CLEAN -> LOW-MEDIUM RISK -> SUSPICIOUS -> MALICIOUS
- Improved recommendation generation with specific risk levels
- Now properly handles cases where ML says 'malicious' but content analysis flags issues
- Resolves contradiction between individual module results and overall status"

# Push to remote repository
echo "🚀 Pushing to remote repository..."
git push origin main

echo "✅ Aggregation logic fix deployed successfully!"
echo ""
echo "📋 Summary of changes:"
echo "   - Fixed overall status determination logic"
echo "   - Added intelligent aggregation strategies"
echo "   - Implemented proper status escalation"
echo "   - Now properly handles TransformerML 'malicious' results"
echo "   - Added specific risk level recommendations"
echo ""
echo "🔍 Expected results:"
echo "   - URLs flagged as 'malicious' by any module with >30% confidence will show as MALICIOUS"
echo "   - Content analysis issues with >50% confidence will escalate status"
echo "   - Multiple suspicious indicators will trigger appropriate risk levels"
echo "   - No more contradiction between individual results and overall status" 