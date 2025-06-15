"""
ThreatAgent Fine-tuning System
=============================

This module provides fine-tuning capabilities for the LLM using historical threat data.
It generates training datasets and adapts the model for improved threat intelligence analysis.
"""

import json
import os
import uuid
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple
from pathlib import Path

from .memory_system import get_memory
from ..config.data_source_config import DATA_SOURCE_CONFIG, TRAINING_CONFIG


class ThreatFineTuner:
    """
    Fine-tuning system for adapting LLM to threat intelligence domain.
    """
    
    def __init__(self, training_data_dir: str = None):
        if training_data_dir is None:
            training_data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge", "training_data")
        
        self.training_data_dir = training_data_dir
        Path(self.training_data_dir).mkdir(parents=True, exist_ok=True)
        
        self.memory = get_memory()
    
    def generate_training_dataset(self) -> str:
        """
        Generate a training dataset from stored threat intelligence data.
        Returns the path to the generated dataset file.
        """
        # Log configuration settings
        use_real_data_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        disable_synthetic = DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False)
        
        print(f"🔧 Dataset Generation Configuration:")
        print(f"   ✅ Use Real Data Only: {use_real_data_only}")
        print(f"   ❌ Disable Synthetic Data: {disable_synthetic}")
        print(f"   📊 Min Confidence Threshold: {DATA_SOURCE_CONFIG.get('MIN_CONFIDENCE_THRESHOLD', 0.5)}")
        print(f"   🚫 Excluded Sources: {DATA_SOURCE_CONFIG.get('EXCLUDED_DATA_SOURCES', [])}")
        
        training_data = []
        
        # Generate IOC classification examples
        ioc_examples = self._generate_ioc_classification_examples()
        training_data.extend(ioc_examples)
        
        # Generate TTP mapping examples
        ttp_examples = self._generate_ttp_mapping_examples()
        training_data.extend(ttp_examples)
        
        # Generate report writing examples
        report_examples = self._generate_report_examples()
        training_data.extend(report_examples)
        
        # Generate threat analysis examples
        analysis_examples = self._generate_analysis_examples()
        training_data.extend(analysis_examples)
        
        # Save training dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_suffix = "real_data" if use_real_data_only else "mixed_data"
        dataset_path = os.path.join(self.training_data_dir, f"threat_intelligence_dataset_{dataset_suffix}_{timestamp}.jsonl")
        
        with open(dataset_path, 'w') as f:
            for example in training_data:
                f.write(json.dumps(example) + '\n')
        
        print(f"📊 Generated training dataset: {len(training_data)} examples")
        print(f"💾 Saved to: {dataset_path}")
        print(f"🔍 Data Source: {'Real threat intelligence only' if use_real_data_only else 'Mixed real and synthetic data'}")
        
        return dataset_path
    
    def _generate_ioc_classification_examples(self) -> List[Dict]:
        """Generate training examples for IOC classification."""
        examples = []
        
        # Configuration check for real data only
        use_real_data_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        min_confidence = DATA_SOURCE_CONFIG.get("MIN_CONFIDENCE_THRESHOLD", 0.5)
        excluded_sources = DATA_SOURCE_CONFIG.get("EXCLUDED_DATA_SOURCES", [])
        
        # Get IOCs from memory database (real data)
        db_path = self.memory.db_path if hasattr(self.memory, 'db_path') else self.memory
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check table schema first
            try:
                cursor.execute("PRAGMA table_info(iocs)")
                columns = [column[1] for column in cursor.fetchall()]
                
                # Build query based on available columns
                base_columns = "ioc, ioc_type, risk_level, category, confidence"
                if "metadata" in columns:
                    base_columns += ", metadata"
                if "source" in columns:
                    base_columns += ", source"
                
                # Build WHERE clause based on available columns
                where_conditions = ["confidence >= ?"]
                params = [min_confidence]
                
                if "source" in columns and excluded_sources:
                    placeholders = ','.join(['?'] * len(excluded_sources))
                    where_conditions.append(f"source NOT IN ({placeholders})")
                    params.extend(excluded_sources)
                
                query = f'''
                    SELECT {base_columns}
                    FROM iocs 
                    WHERE {' AND '.join(where_conditions)}
                    ORDER BY confidence DESC LIMIT 100
                '''
                
                cursor.execute(query, params)
                
                for row in cursor.fetchall():
                    ioc, ioc_type, risk_level, category, confidence = row[:5]
                    metadata_str = row[5] if len(row) > 5 and "metadata" in columns else '{}'
                    source = row[6] if len(row) > 6 and "source" in columns else 'unknown'
                    
                    metadata = json.loads(metadata_str or '{}')
                    
                    # Skip if source is in excluded list or marked as synthetic
                    if source != 'unknown' and any(excluded in source.lower() for excluded in excluded_sources):
                        continue
                    
                    # Create instruction-following example from real data
                    instruction = f"Classify the following indicator of compromise (IOC): {ioc}"
                    
                    response = {
                        "ioc": ioc,
                        "type": ioc_type,
                        "risk_level": risk_level,
                        "category": category,
                        "confidence": confidence,
                        "reasoning": metadata.get('reasoning', f"Real threat intelligence data shows this {ioc_type} exhibits {category} characteristics with {risk_level} risk level."),
                        "source": "real_threat_intelligence"
                    }
                    
                    examples.append({
                        "instruction": instruction,
                        "input": ioc,
                        "output": json.dumps(response, indent=2)
                    })
                    
            except sqlite3.OperationalError as e:
                print(f"⚠️  Database schema issue: {e}")
                # Continue with empty examples if database has issues
        
        # Only add synthetic examples if real data only mode is disabled
        if not use_real_data_only and not DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False):
            synthetic_examples = [
                {
                    "instruction": "Classify the following indicator of compromise (IOC): login-secure-banking.ru",
                    "input": "login-secure-banking.ru",
                    "output": json.dumps({
                        "ioc": "login-secure-banking.ru",
                        "type": "domain",
                        "risk_level": "high",
                        "category": "phishing",
                        "confidence": 0.9,
                        "reasoning": "Domain mimics legitimate banking services with suspicious TLD and login keyword typically used in phishing campaigns.",
                        "source": "synthetic_example"
                    }, indent=2)
                },
                {
                    "instruction": "Classify the following indicator of compromise (IOC): 192.168.1.100",
                    "input": "192.168.1.100",
                    "output": json.dumps({
                        "ioc": "192.168.1.100",
                        "type": "ip_address",
                        "risk_level": "low",
                        "category": "internal",
                        "confidence": 0.1,
                        "reasoning": "Private IP address range, likely internal network traffic with minimal threat potential.",
                        "source": "synthetic_example"
                    }, indent=2)
                }
            ]
            examples.extend(synthetic_examples)
        
        print(f"📊 Generated {len(examples)} IOC classification examples (Real data only: {use_real_data_only})")
        return examples
    
    def _generate_ttp_mapping_examples(self) -> List[Dict]:
        """Generate training examples for TTP mapping."""
        examples = []
        
        # Configuration check for real data only
        use_real_data_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        excluded_sources = DATA_SOURCE_CONFIG.get("EXCLUDED_DATA_SOURCES", [])
        
        # Get real TTP mappings from memory database
        db_path = self.memory.db_path if hasattr(self.memory, 'db_path') else self.memory
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if analysis_history table exists and get its schema
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_history'")
                table_exists = cursor.fetchone() is not None
                
                if table_exists:
                    # Get actual TTP mappings from analysis history
                    cursor.execute('''
                        SELECT DISTINCT input_data, output_data, analysis_type
                        FROM analysis_history 
                        WHERE analysis_type = 'ttp_mapping' 
                        AND input_data IS NOT NULL 
                        AND output_data IS NOT NULL
                        LIMIT 50
                    ''')
                    
                    for row in cursor.fetchall():
                        input_data, output_data, analysis_type = row
                        
                        try:
                            # Parse the real analysis data
                            if input_data and output_data:
                                examples.append({
                                    "instruction": "Map the threat category to appropriate MITRE ATT&CK TTPs based on real analysis.",
                                    "input": input_data,
                                    "output": output_data
                                })
                        except (json.JSONDecodeError, KeyError):
                            continue  # Skip malformed data
            except sqlite3.OperationalError:
                # Table doesn't exist or has different schema
                pass
        
        # Only add predefined mappings if real data only mode is disabled
        if not use_real_data_only and not DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False):
            # TTP mapping knowledge (kept as fallback only)
            ttp_mappings = {
                "phishing": ["T1566.001", "T1566.002", "T1566.003"],
                "malware": ["T1204.001", "T1204.002", "T1055"],
                "c2": ["T1071.001", "T1071.004", "T1090"],
                "exfiltration": ["T1041", "T1048", "T1567"],
                "persistence": ["T1053", "T1547", "T1574"]
            }
            
            for category, ttps in ttp_mappings.items():
                for ttp in ttps:
                    instruction = f"Map the threat category '{category}' to appropriate MITRE ATT&CK TTPs."
                    
                    response = {
                        "category": category,
                        "primary_ttp": ttp,
                        "confidence": 0.8,
                        "reasoning": f"The {category} category commonly aligns with {ttp} based on MITRE ATT&CK framework.",
                        "source": "framework_mapping"
                    }
                    
                    examples.append({
                        "instruction": instruction,
                        "input": category,
                        "output": json.dumps(response, indent=2)
                    })
        
        print(f"📊 Generated {len(examples)} TTP mapping examples (Real data only: {use_real_data_only})")
        return examples
    
    def _generate_report_examples(self) -> List[Dict]:
        """Generate training examples for report writing."""
        examples = []
        
        # Configuration check for real data only
        use_real_data_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        excluded_sources = DATA_SOURCE_CONFIG.get("EXCLUDED_DATA_SOURCES", [])
        
        # Get real analysis history for report examples
        history = self.memory.get_analysis_history(analysis_type="report_generation", limit=50)
        
        for record in history:
            if record['input_data'] and record['output_data']:
                # Filter out synthetic/demo data
                source = record.get('metadata', {}).get('source', '')
                if any(excluded in source.lower() for excluded in excluded_sources):
                    continue
                
                instruction = "Generate a professional threat intelligence report from the provided real IOC analysis data."
                
                examples.append({
                    "instruction": instruction,
                    "input": record['input_data'],
                    "output": record['output_data']
                })
        
        # Only add template example if real data only mode is disabled
        if not use_real_data_only and not DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False):
            template_example = {
                "instruction": "Generate a professional threat intelligence report from the provided IOC data.",
                "input": json.dumps([
                    {"ioc": "malicious-site.com", "risk": "high", "category": "phishing", "ttp": "T1566.002"},
                    {"ioc": "evil-domain.net", "risk": "medium", "category": "malware", "ttp": "T1204.002"}
                ]),
                "output": """# Threat Intelligence Report

## Executive Summary
Identified 2 suspicious indicators associated with phishing and malware distribution campaigns.

## Indicators of Compromise (IOCs)
- malicious-site.com (HIGH RISK) - Phishing domain
- evil-domain.net (MEDIUM RISK) - Malware distribution

## MITRE ATT&CK TTPs
- T1566.002 - Phishing: Spearphishing Link
- T1204.002 - User Execution: Malicious File

## Recommendations
1. Block these domains at network perimeter
2. Update email security filters
3. Monitor for similar domain patterns
4. User awareness training for phishing recognition
"""
            }
            
            examples.append(template_example)
        
        print(f"📊 Generated {len(examples)} report generation examples (Real data only: {use_real_data_only})")
        return examples
    
    def _generate_analysis_examples(self) -> List[Dict]:
        """Generate training examples for general threat analysis."""
        examples = []
        
        # Configuration check for real data only
        use_real_data_only = DATA_SOURCE_CONFIG.get("USE_REAL_DATA_ONLY", False)
        excluded_sources = DATA_SOURCE_CONFIG.get("EXCLUDED_DATA_SOURCES", [])
        
        # Get real analysis examples from memory database
        db_path = self.memory.db_path if hasattr(self.memory, 'db_path') else self.memory
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check if analysis_history table exists and get available columns
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_history'")
                table_exists = cursor.fetchone() is not None
                
                if table_exists:
                    # Get actual threat analysis from history
                    cursor.execute('''
                        SELECT DISTINCT input_data, output_data, analysis_type
                        FROM analysis_history 
                        WHERE analysis_type IN ('threat_analysis', 'domain_analysis', 'ip_analysis')
                        AND input_data IS NOT NULL 
                        AND output_data IS NOT NULL
                        LIMIT 100
                    ''')
                    
                    for row in cursor.fetchall():
                        input_data, output_data, analysis_type = row
                        
                        # For now, skip metadata filtering since the table structure may vary
                        try:
                            examples.append({
                                "instruction": f"Analyze this indicator for potential security threats based on real intelligence: {input_data}",
                                "input": input_data,
                                "output": output_data
                            })
                        except (json.JSONDecodeError, KeyError):
                            continue  # Skip malformed data
            except sqlite3.OperationalError:
                # Table doesn't exist or has different schema
                pass
        
        # Only add synthetic examples if real data only mode is disabled
        if not use_real_data_only and not DATA_SOURCE_CONFIG.get("DISABLE_SYNTHETIC_DATA", False):
            domain_patterns = [
                {
                    "instruction": "Analyze this domain for potential security threats: secure-login-bank.tk",
                    "input": "secure-login-bank.tk",
                    "output": """Analysis of secure-login-bank.tk:

THREAT INDICATORS:
- Suspicious TLD (.tk) commonly used in malicious campaigns
- Banking-related keywords (secure, login, bank) typical of phishing
- Domain structure mimics legitimate banking services

RISK ASSESSMENT: HIGH
CATEGORY: Banking phishing
RECOMMENDED ACTIONS:
1. Block domain immediately
2. Alert security team
3. Check for similar domain registrations
4. Monitor network traffic for this indicator"""
                },
                {
                    "instruction": "Analyze this IP address for potential security threats: 198.51.100.42",
                    "input": "198.51.100.42",
                    "output": """Analysis of 198.51.100.42:

THREAT INDICATORS:
- Public IP address in documentation range
- No known malicious associations
- Standard IPv4 format

RISK ASSESSMENT: LOW
CATEGORY: Documentation/Test IP
RECOMMENDED ACTIONS:
1. Monitor for unusual traffic patterns
2. No immediate blocking required
3. Standard network monitoring sufficient"""
                }
            ]
            examples.extend(domain_patterns)
        
        print(f"📊 Generated {len(examples)} analysis examples (Real data only: {use_real_data_only})")
        return examples
    
    def create_context_prompt(self, query: str, max_examples: int = 5) -> str:
        """
        Create a context-enriched prompt using similar historical data.
        """
        # Search for similar IOCs/analyses
        similar_iocs = self.memory.search_similar_iocs(query, limit=max_examples)
        
        if not similar_iocs:
            return query
        
        # Build context prompt
        context = "HISTORICAL CONTEXT (similar threats analyzed):\n\n"
        
        for i, ioc_data in enumerate(similar_iocs, 1):
            context += f"{i}. IOC: {ioc_data['ioc']}\n"
            context += f"   Risk: {ioc_data['risk_level']} | Category: {ioc_data['category']}\n"
            context += f"   Confidence: {ioc_data['confidence']:.2f} | Seen {ioc_data['times_seen']} times\n"
            context += f"   Similarity: {ioc_data['similarity']:.3f}\n\n"
        
        # Add analysis history context
        recent_analyses = self.memory.get_analysis_history(limit=3)
        if recent_analyses:
            context += "RECENT ANALYSIS PATTERNS:\n\n"
            for analysis in recent_analyses:
                context += f"- {analysis['analysis_type']}: {analysis['confidence']:.2f} confidence\n"
        
        # Combine context with query
        enhanced_prompt = f"{context}\nCURRENT ANALYSIS REQUEST:\n{query}\n\nBased on the historical context above, provide a detailed analysis:"
        
        return enhanced_prompt
    
    def export_training_config(self) -> Dict:
        """
        Export configuration for fine-tuning frameworks like Ollama or Unsloth.
        """
        stats = self.memory.get_statistics()
        
        config = {
            "model_name": "threat-intelligence-llama3",
            "base_model": "llama3",
            "training_data": {
                "total_examples": stats['total_analyses'],
                "ioc_examples": stats['total_iocs'],
                "categories": list(stats['category_distribution'].keys()),
                "risk_levels": list(stats['risk_distribution'].keys())
            },
            "training_parameters": {
                "learning_rate": 5e-5,
                "batch_size": 4,
                "epochs": 3,
                "max_seq_length": 2048,
                "warmup_steps": 100
            },
            "ollama_modelfile": self._generate_ollama_modelfile(),
            "created_at": datetime.now().isoformat()
        }
        
        return config
    
    def _generate_ollama_modelfile(self) -> str:
        """Generate Ollama Modelfile for custom fine-tuned model."""
        stats = self.memory.get_statistics()
        
        # Build system prompt with learned patterns
        system_prompt = """You are a cybersecurity threat intelligence analyst specialized in analyzing indicators of compromise (IOCs), mapping threats to MITRE ATT&CK framework, and generating professional security reports.

Your expertise includes:
- IOC classification and risk assessment
- MITRE ATT&CK TTP mapping
- Threat intelligence report generation
- Sigma rule creation for SOC teams

"""
        
        # Add learned patterns to system prompt
        if stats['category_distribution']:
            common_categories = sorted(stats['category_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]
            system_prompt += f"Common threat categories you've analyzed: {', '.join([cat for cat, _ in common_categories])}\n"
        
        if stats['risk_distribution']:
            system_prompt += f"Risk levels you assess: {', '.join(stats['risk_distribution'].keys())}\n"
        
        system_prompt += "\nAlways provide detailed analysis with confidence scores and actionable recommendations."
        
        modelfile = f'''FROM llama3

SYSTEM """{system_prompt}"""

# Fine-tuning parameters
PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_predict 512
PARAMETER stop "Human:"
PARAMETER stop "Assistant:"
PARAMETER stop "\\n\\n"

# Custom prompt template for threat intelligence
TEMPLATE """{{{{ if .System }}}}<|start_header_id|>system<|end_header_id|>

{{{{ .System }}}}<|eot_id|>{{{{ end }}}}{{{{ if .Prompt }}}}<|start_header_id|>user<|end_header_id|>

{{{{ .Prompt }}}}<|eot_id|>{{{{ end }}}}<|start_header_id|>assistant<|end_header_id|>

"""
'''
        
        return modelfile


# Global fine-tuner instance
_finetuner_instance = None

def get_finetuner() -> ThreatFineTuner:
    """Get the global fine-tuner instance."""
    global _finetuner_instance
    if _finetuner_instance is None:
        _finetuner_instance = ThreatFineTuner()
    return _finetuner_instance
