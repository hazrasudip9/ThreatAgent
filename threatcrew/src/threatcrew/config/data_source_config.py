"""
ThreatAgent Data Source Configuration
====================================

Configuration settings for controlling the data sources used in threat intelligence training.
"""

# Data source configuration
DATA_SOURCE_CONFIG = {
    # Use only real threat intelligence data from memory database
    "USE_REAL_DATA_ONLY": True,
    
    # Disable synthetic data generation
    "DISABLE_SYNTHETIC_DATA": True,
    
    # Minimum confidence threshold for real data to be included
    "MIN_CONFIDENCE_THRESHOLD": 0.5,
    
    # Maximum number of examples per category
    "MAX_EXAMPLES_PER_CATEGORY": 1000,
    
    # Data sources to include
    "ALLOWED_DATA_SOURCES": [
        "memory_database",
        "historical_analysis",
        "real_iocs",
        "actual_reports"
    ],
    
    # Data sources to exclude
    "EXCLUDED_DATA_SOURCES": [
        "synthetic",
        "generated",
        "example",
        "demo",
        "test"
    ]
}

# Training dataset configuration
TRAINING_CONFIG = {
    # Only use verified real threat intelligence
    "VERIFIED_DATA_ONLY": True,
    
    # Require source attribution for all training data
    "REQUIRE_SOURCE_ATTRIBUTION": True,
    
    # Filter out training examples with suspicious patterns
    "FILTER_SUSPICIOUS_PATTERNS": True
}
