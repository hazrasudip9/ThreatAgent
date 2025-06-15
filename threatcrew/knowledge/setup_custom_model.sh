#!/bin/bash

echo "🤖 Setting up ThreatAgent Custom Model"
echo "======================================"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start it first:"
    echo "   ollama serve"
    exit 1
fi

# Create custom model
echo "📦 Creating threat-intelligence model..."
ollama create threat-intelligence -f knowledge/ThreatAgent.Modelfile

if [ $? -eq 0 ]; then
    echo "✅ Custom model created successfully!"
    echo ""
    echo "🎯 Test the model:"
    echo "   ollama run threat-intelligence"
    echo ""
    echo "🔧 To use in ThreatAgent, update crew.py:"
    echo "   model='threat-intelligence'"
    echo ""
else
    echo "❌ Model creation failed"
    exit 1
fi
