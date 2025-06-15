#!/usr/bin/env bash
# refresh_threatagent_data.sh
# This script will clear all ThreatAgent data: memory DB, training data, enhanced datasets, and user preferences.
# USE WITH CAUTION: This action is irreversible!

set -e

# Paths (relative to project root)
MEMORY_DB="src/knowledge/threat_memory.db"
TRAINING_DATA="threatcrew/knowledge/threat_intelligence_training.jsonl"
ENHANCED_DATA="threatcrew/knowledge/enhanced_training_dataset.jsonl"
USER_PREFS="threatcrew/knowledge/user_preference.txt"

# Track what was deleted/cleared
DELETED_ITEMS=()

# Remove memory database
if [ -f "$MEMORY_DB" ]; then
  echo "Removing memory database: $MEMORY_DB"
  rm "$MEMORY_DB"
  DELETED_ITEMS+=("Memory database: $MEMORY_DB")
else
  echo "Memory database not found: $MEMORY_DB"
fi

# Clear training data
if [ -f "$TRAINING_DATA" ]; then
  echo "Clearing LLM training data: $TRAINING_DATA"
  > "$TRAINING_DATA"
  DELETED_ITEMS+=("LLM training data: $TRAINING_DATA (cleared)")
else
  echo "Training data file not found: $TRAINING_DATA"
fi

# Clear enhanced training dataset
if [ -f "$ENHANCED_DATA" ]; then
  echo "Clearing enhanced training dataset: $ENHANCED_DATA"
  > "$ENHANCED_DATA"
  DELETED_ITEMS+=("Enhanced training dataset: $ENHANCED_DATA (cleared)")
else
  echo "Enhanced training dataset not found: $ENHANCED_DATA"
fi

# Clear user preferences
if [ -f "$USER_PREFS" ]; then
  echo "Clearing user preferences: $USER_PREFS"
  > "$USER_PREFS"
  DELETED_ITEMS+=("User preferences: $USER_PREFS (cleared)")
else
  echo "User preferences file not found: $USER_PREFS"
fi

# Optionally delete a fine-tuned LLM model from Ollama
read -p "Do you want to delete a fine-tuned LLM model from Ollama? (y/n): " DELETE_MODEL
if [ "$DELETE_MODEL" = "y" ] || [ "$DELETE_MODEL" = "Y" ]; then
  echo "Listing available Ollama models:"
  ollama list
  read -p "Enter the name of the model you want to delete: " MODEL_NAME
  if [ -n "$MODEL_NAME" ]; then
    echo "Deleting model: $MODEL_NAME"
    ollama rm "$MODEL_NAME"
    DELETED_ITEMS+=("Ollama model: $MODEL_NAME (deleted)")
    echo "Model $MODEL_NAME deleted from Ollama."
  else
    echo "No model name entered. Skipping model deletion."
  fi
else
  echo "Skipping Ollama model deletion."
fi

# Output summary of deleted/cleared items

echo "\n===== ThreatAgent Data Refresh Summary ====="
if [ ${#DELETED_ITEMS[@]} -eq 0 ]; then
  echo "No files or models were deleted or cleared."
else
  for item in "${DELETED_ITEMS[@]}"; do
    echo "- $item"
  done
fi
echo "All ThreatAgent data refresh operations are complete."
