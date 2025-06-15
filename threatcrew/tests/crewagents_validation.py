#!/usr/bin/env python3
"""
ThreatAgent CrewAgents Validation Script
=======================================

This script displays:
1. The latest LLM fine-tuning data (last entry in training file)
2. The date and time of the latest fine-tuning data
3. A summary of the training data
4. Details from the memory database (IOCs, stats)
5. The latest consolidated threat intelligence report (if available)
"""

import os
import json
from pathlib import Path
from datetime import datetime

TRAINING_FILE = Path(__file__).parent / "src/knowledge/training_data/threat_intelligence_dataset_20250615_124031.jsonl"
MEMORY_DB = Path(__file__).parent / "src/knowledge/threat_memory.db"
REPORT_FILE = Path(__file__).parent / "src/threatcrew/tools/consolidated_report.json"

print("\n=== ThreatAgent CrewAgents Validation ===\n")

# 1. Latest LLM fine-tuning data
if TRAINING_FILE.exists():
    with open(TRAINING_FILE, "r") as f:
        lines = f.readlines()
        if lines:
            last_entry = json.loads(lines[-1])
            print(f"[LLM Training] Last entry: {last_entry}")
            print(f"[LLM Training] Last entry date: {last_entry.get('date', 'N/A')}")
            print(f"[LLM Training] Total entries: {len(lines)}")
        else:
            print("[LLM Training] No entries found.")
else:
    print(f"[LLM Training] Training file not found: {TRAINING_FILE}")

# 2. Memory DB stats (placeholder, implement actual DB read if needed)
if MEMORY_DB.exists():
    print(f"[Memory DB] Found at: {MEMORY_DB}")
    # Add real DB stats extraction here if needed
else:
    print(f"[Memory DB] Not found: {MEMORY_DB}")

# 3. Latest consolidated report
if REPORT_FILE.exists():
    with open(REPORT_FILE, "r") as f:
        report = json.load(f)
        print(f"[Report] Latest consolidated report summary:")
        print(json.dumps(report, indent=2)[:1000])
else:
    print(f"[Report] No consolidated report found at: {REPORT_FILE}")

print("\n=== Validation Complete ===\n")
