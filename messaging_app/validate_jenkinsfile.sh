#!/bin/bash

# Jenkinsfile Validation Script
# This script validates that the Jenkinsfile meets all requirements

echo "=== Jenkinsfile Validation Report ==="
echo ""

# Check if Jenkinsfile exists
echo "1. Checking Jenkinsfile existence..."
if [ -f "messaging_app/Jenkinsfile" ]; then
    echo "   ✅ messaging_app/Jenkinsfile exists"
else
    echo "   ❌ messaging_app/Jenkinsfile does not exist"
    exit 1
fi

# Check if Jenkinsfile is not empty
echo "2. Checking Jenkinsfile content..."
if [ -s "messaging_app/Jenkinsfile" ]; then
    echo "   ✅ messaging_app/Jenkinsfile is not empty"
else
    echo "   ❌ messaging_app/Jenkinsfile is empty"
    exit 1
fi

# Check for GitHub credentials usage
echo "3. Checking GitHub credentials configuration..."
if grep -q "github-credentials" messaging_app/Jenkinsfile; then
    echo "   ✅ GitHub credentials ID 'github-credentials' found"
else
    echo "   ❌ GitHub credentials ID not found"
fi

# Check for pytest usage
echo "4. Checking pytest configuration..."
if grep -q "pytest" messaging_app/Jenkinsfile; then
    echo "   ✅ pytest usage found in pipeline"
else
    echo "   ❌ pytest not found in pipeline"
fi

# Check for GitHub repository pull
echo "5. Checking GitHub repository pull..."
if grep -q "github.com" messaging_app/Jenkinsfile; then
    echo "   ✅ GitHub repository URL found"
else
    echo "   ❌ GitHub repository URL not found"
fi

# Check for dependency installation
echo "6. Checking dependency installation..."
if grep -q "requirements.txt" messaging_app/Jenkinsfile; then
    echo "   ✅ Dependency installation found"
else
    echo "   ❌ Dependency installation not found"
fi

# Check for report generation
echo "7. Checking report generation..."
if grep -q "test-results.xml" messaging_app/Jenkinsfile; then
    echo "   ✅ Test report generation found"
else
    echo "   ❌ Test report generation not found"
fi

# Check for coverage reporting
echo "8. Checking coverage reporting..."
if grep -q "cov-report" messaging_app/Jenkinsfile; then
    echo "   ✅ Coverage reporting found"
else
    echo "   ❌ Coverage reporting not found"
fi

echo ""
echo "=== Validation Complete ==="
echo "All checks have been performed. Review any ❌ items above."
