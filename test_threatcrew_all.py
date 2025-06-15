import pytest
import os
import json
from pathlib import Path

# Test memory DB exists and is valid
@pytest.mark.memory
def test_memory_db_exists():
    db_path = Path("threatcrew/src/knowledge/threat_memory.db")
    assert db_path.exists(), f"Memory DB not found at {db_path}"

# Test training data exists and is valid JSONL
@pytest.mark.training
def test_training_data_exists_and_valid():
    training_file = Path("threatcrew/src/knowledge/training_data/threat_intelligence_dataset_20250615_124031.jsonl")
    assert training_file.exists(), f"Training data not found at {training_file}"
    with open(training_file) as f:
        for line in f:
            json.loads(line)  # Should not raise

# Test consolidated report (if exists) is valid JSON
@pytest.mark.report
def test_consolidated_report_valid():
    report_file = Path("threatcrew/src/threatcrew/tools/consolidated_report.json")
    if report_file.exists():
        with open(report_file) as f:
            json.load(f)  # Should not raise

# Test that verify_system.py runs without error
@pytest.mark.system
def test_verify_system_runs():
    result = os.system("python3 threatcrew/tests/verify_system.py")
    assert result == 0

# Test that simple_memory_test.py runs without error
@pytest.mark.memory
def test_simple_memory_test_runs():
    result = os.system("python3 threatcrew/tests/simple_memory_test.py")
    assert result == 0

# Test that demo_complete_system.py runs without error
@pytest.mark.demo
def test_demo_complete_system_runs():
    result = os.system("python3 threatcrew/tests/demo_complete_system.py")
    assert result == 0

# Test that demo_targeting_system.py runs without error
@pytest.mark.demo
def test_demo_targeting_system_runs():
    result = os.system("python3 threatcrew/tests/demo_targeting_system.py")
    assert result == 0

# Test that ge_vernova_end_to_end_demo.py runs without error
@pytest.mark.demo
def test_ge_vernova_end_to_end_demo_runs():
    result = os.system("python3 threatcrew/tests/ge_vernova_end_to_end_demo.py")
    assert result == 0

# Test that setup_memory_finetuning.py runs without error
@pytest.mark.setup
def test_setup_memory_finetuning_runs():
    # Use echo n | python3 ... for portable input
    result = os.system("echo n | python3 threatcrew/tests/setup_memory_finetuning.py")
    assert result == 0

# Test that simple_run.py runs without error
@pytest.mark.demo
def test_simple_run_runs():
    result = os.system("python3 threatcrew/tests/simple_run.py")
    assert result == 0

# Test that crewagents_validation.py runs without error
@pytest.mark.validation
def test_crewagents_validation_runs():
    result = os.system("python3 threatcrew/tests/crewagents_validation.py")
    assert result == 0

