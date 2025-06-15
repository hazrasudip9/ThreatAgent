#!/bin/bash

# ThreatAgent - Test Runner Script

echo "🧪 ThreatAgent - System Testing"
echo "================================"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Error: Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    exit 1
fi

# Check if llama3 model is available
if ! curl -s http://localhost:11434/api/tags | grep -q "llama3"; then
    echo "❌ Error: llama3 model not found. Please install it first:"
    echo "   ollama pull llama3"
    exit 1
fi

echo "✅ Prerequisites met - running tests..."
echo ""

# Set Python path and run tests
export PYTHONPATH="$(pwd)/src"
python3 test_simple.py

echo ""
echo "🧪 Testing completed!"
