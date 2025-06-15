"""
ContinuousLearningManager
========================

Manages continuous learning and model improvement for the ThreatAgent system.
Automatically generates training data and triggers fine-tuning based on performance metrics.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..tools.memory_system import get_memory
from ..tools.finetuning_system import ThreatFineTuner

logger = logging.getLogger(__name__)

@dataclass
class LearningMetrics:
    accuracy: float
    confidence: float
    processing_time: float
    false_positive_rate: float
    false_negative_rate: float
    timestamp: datetime

@dataclass
class ModelPerformance:
    model_version: str
    metrics: LearningMetrics
    training_data_size: int
    improvements: Dict[str, float]

class ContinuousLearningManager:
    """
    Manages continuous learning for the threat intelligence system.
    Monitors performance, generates training data, and triggers model updates.
    """
    
    def __init__(self, learning_threshold: float = 0.1, min_training_samples: int = 100):
        self.memory = get_memory()
        self.finetuner = ThreatFineTuner()
        self.learning_threshold = learning_threshold  # Minimum improvement needed to retrain
        self.min_training_samples = min_training_samples
        self.running = False
        self.current_model_version = "1.0"
        self.performance_history: List[ModelPerformance] = []
        self.last_training_time = None
        
    async def start_continuous_learning(self):
        """Start the continuous learning process."""
        self.running = True
        logger.info("🧠 Starting continuous learning manager...")
        
        while self.running:
            try:
                # Evaluate current performance
                current_metrics = await self._evaluate_current_performance()
                
                # Check if retraining is needed
                if self._should_retrain(current_metrics):
                    logger.info("📈 Performance decline detected. Initiating retraining...")
                    await self._trigger_retraining()
                
                # Update knowledge patterns
                await self._update_knowledge_patterns()
                
                # Sleep for evaluation interval (e.g., every 6 hours)
                await asyncio.sleep(6 * 3600)
                
            except Exception as e:
                logger.error(f"❌ Error in continuous learning: {e}")
                await asyncio.sleep(3600)  # Retry in 1 hour
    
    async def _evaluate_current_performance(self) -> LearningMetrics:
        """Evaluate the current model performance."""
        try:
            # Get recent analysis results
            recent_analyses = self._get_recent_analyses(hours=24)
            
            if not recent_analyses:
                logger.warning("⚠️  No recent analyses found for performance evaluation")
                return LearningMetrics(
                    accuracy=0.0,
                    confidence=0.0,
                    processing_time=0.0,
                    false_positive_rate=0.0,
                    false_negative_rate=0.0,
                    timestamp=datetime.now()
                )
            
            # Calculate metrics
            total_analyses = len(recent_analyses)
            total_confidence = sum(analysis.get('confidence', 0) for analysis in recent_analyses)
            total_processing_time = sum(analysis.get('processing_time', 0) for analysis in recent_analyses)
            
            # Estimate accuracy based on confidence and feedback
            high_confidence_analyses = [a for a in recent_analyses if a.get('confidence', 0) > 0.8]
            estimated_accuracy = len(high_confidence_analyses) / total_analyses if total_analyses > 0 else 0
            
            # Calculate false positive/negative rates (simplified estimation)
            fp_rate = self._estimate_false_positive_rate(recent_analyses)
            fn_rate = self._estimate_false_negative_rate(recent_analyses)
            
            metrics = LearningMetrics(
                accuracy=estimated_accuracy,
                confidence=total_confidence / total_analyses if total_analyses > 0 else 0,
                processing_time=total_processing_time / total_analyses if total_analyses > 0 else 0,
                false_positive_rate=fp_rate,
                false_negative_rate=fn_rate,
                timestamp=datetime.now()
            )
            
            logger.info(f"📊 Current performance - Accuracy: {metrics.accuracy:.2f}, "
                       f"Confidence: {metrics.confidence:.2f}, FP Rate: {metrics.false_positive_rate:.2f}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error evaluating performance: {e}")
            return LearningMetrics(0, 0, 0, 0, 0, datetime.now())
    
    def _get_recent_analyses(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent analysis results from memory."""
        import sqlite3
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.memory.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT analysis_type, input_data, output_data, confidence, processing_time, created_at
                FROM analysis_history 
                WHERE created_at >= ? 
                ORDER BY created_at DESC
            ''', (cutoff_time.isoformat(),))
            
            analyses = []
            for row in cursor.fetchall():
                analysis_type, input_data, output_data, confidence, processing_time, created_at = row
                analyses.append({
                    'analysis_type': analysis_type,
                    'input_data': json.loads(input_data) if input_data else {},
                    'output_data': json.loads(output_data) if output_data else {},
                    'confidence': confidence or 0,
                    'processing_time': processing_time or 0,
                    'created_at': created_at
                })
            
            return analyses
    
    def _estimate_false_positive_rate(self, analyses: List[Dict[str, Any]]) -> float:
        """Estimate false positive rate based on analysis patterns."""
        # Simplified estimation - in production, this would use feedback data
        classification_analyses = [a for a in analyses if a['analysis_type'] == 'ioc_classification']
        if not classification_analyses:
            return 0.0
        
        # Look for patterns that might indicate false positives
        # E.g., low confidence classifications that were marked as high risk
        potential_fps = 0
        for analysis in classification_analyses:
            output = analysis.get('output_data', {})
            if isinstance(output, str):
                try:
                    output = json.loads(output)
                except:
                    continue
            
            confidence = analysis.get('confidence', 0)
            risk_level = output.get('risk_level', 'UNKNOWN')
            
            # If low confidence but high risk, might be false positive
            if confidence < 0.6 and risk_level in ['HIGH', 'CRITICAL']:
                potential_fps += 1
        
        return potential_fps / len(classification_analyses) if classification_analyses else 0.0
    
    def _estimate_false_negative_rate(self, analyses: List[Dict[str, Any]]) -> float:
        """Estimate false negative rate based on analysis patterns."""
        # Simplified estimation - in production, this would use feedback data
        classification_analyses = [a for a in analyses if a['analysis_type'] == 'ioc_classification']
        if not classification_analyses:
            return 0.0
        
        # Look for patterns that might indicate false negatives
        # E.g., high confidence classifications marked as low risk but showing suspicious patterns
        potential_fns = 0
        for analysis in classification_analyses:
            output = analysis.get('output_data', {})
            if isinstance(output, str):
                try:
                    output = json.loads(output)
                except:
                    continue
            
            confidence = analysis.get('confidence', 0)
            risk_level = output.get('risk_level', 'UNKNOWN')
            
            # If high confidence but low risk, but input shows suspicious patterns
            if confidence > 0.8 and risk_level in ['LOW', 'UNKNOWN']:
                input_data = analysis.get('input_data', {})
                if self._has_suspicious_patterns(input_data):
                    potential_fns += 1
        
        return potential_fns / len(classification_analyses) if classification_analyses else 0.0
    
    def _has_suspicious_patterns(self, input_data: Dict[str, Any]) -> bool:
        """Check if input data has suspicious patterns that might indicate false negative."""
        # Simplified pattern detection
        if isinstance(input_data, str):
            text = input_data.lower()
            suspicious_keywords = ['phish', 'malware', 'exploit', 'attack', 'threat', 'suspicious']
            return any(keyword in text for keyword in suspicious_keywords)
        return False
    
    def _should_retrain(self, current_metrics: LearningMetrics) -> bool:
        """Determine if the model should be retrained based on performance."""
        if not self.performance_history:
            return False
        
        # Check if we have enough new training data
        new_analyses_count = len(self._get_recent_analyses(hours=24))
        if new_analyses_count < self.min_training_samples:
            return False
        
        # Check if enough time has passed since last training (minimum 1 week)
        if self.last_training_time:
            time_since_training = datetime.now() - self.last_training_time
            if time_since_training < timedelta(days=7):
                return False
        
        # Compare with baseline performance
        baseline_metrics = self.performance_history[-1].metrics
        
        # Retrain if accuracy dropped significantly
        accuracy_drop = baseline_metrics.accuracy - current_metrics.accuracy
        if accuracy_drop > self.learning_threshold:
            logger.info(f"📉 Accuracy dropped by {accuracy_drop:.3f} (threshold: {self.learning_threshold})")
            return True
        
        # Retrain if false positive rate increased significantly
        fp_increase = current_metrics.false_positive_rate - baseline_metrics.false_positive_rate
        if fp_increase > self.learning_threshold:
            logger.info(f"📈 False positive rate increased by {fp_increase:.3f}")
            return True
        
        # Retrain if false negative rate increased significantly
        fn_increase = current_metrics.false_negative_rate - baseline_metrics.false_negative_rate
        if fn_increase > self.learning_threshold:
            logger.info(f"📈 False negative rate increased by {fn_increase:.3f}")
            return True
        
        return False
    
    async def _trigger_retraining(self):
        """Trigger the retraining process."""
        try:
            logger.info("🔄 Starting model retraining process...")
            
            # Generate new training dataset
            dataset_path = self.finetuner.generate_training_dataset()
            
            # Create enhanced training configuration
            training_config = self.finetuner.create_training_configuration(
                dataset_path=dataset_path,
                model_name=f"threat-intelligence-v{self._get_next_version()}",
                learning_rate=0.0001,
                epochs=3,
                batch_size=4
            )
            
            # Generate Ollama Modelfile for the new version
            modelfile_path = self.finetuner.generate_ollama_modelfile(
                base_model="llama3",
                dataset_path=dataset_path,
                model_name=training_config["model_name"]
            )
            
            logger.info(f"📝 Generated training configuration and Modelfile")
            logger.info(f"💾 Dataset: {dataset_path}")
            logger.info(f"🔧 Modelfile: {modelfile_path}")
            
            # Update model version
            self.current_model_version = training_config["model_name"]
            self.last_training_time = datetime.now()
            
            # Store performance improvement
            self._record_training_event(dataset_path, training_config)
            
            logger.info("✅ Retraining completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error during retraining: {e}")
    
    def _get_next_version(self) -> str:
        """Get the next model version number."""
        if not self.performance_history:
            return "2.0"
        
        # Extract version number and increment
        last_version = self.performance_history[-1].model_version
        try:
            major, minor = last_version.split('.')
            return f"{major}.{int(minor) + 1}"
        except:
            return "2.0"
    
    def _record_training_event(self, dataset_path: str, training_config: Dict[str, Any]):
        """Record a training event in the performance history."""
        # Calculate training data size
        training_data_size = 0
        try:
            with open(dataset_path, 'r') as f:
                training_data_size = sum(1 for line in f)
        except:
            pass
        
        # Create dummy metrics for new model (will be updated after evaluation)
        metrics = LearningMetrics(
            accuracy=0.0,
            confidence=0.0,
            processing_time=0.0,
            false_positive_rate=0.0,
            false_negative_rate=0.0,
            timestamp=datetime.now()
        )
        
        performance = ModelPerformance(
            model_version=training_config["model_name"],
            metrics=metrics,
            training_data_size=training_data_size,
            improvements={}
        )
        
        self.performance_history.append(performance)
    
    async def _update_knowledge_patterns(self):
        """Update knowledge patterns based on recent successful analyses."""
        try:
            # Get high-confidence analyses from the last week
            successful_analyses = self._get_successful_analyses(days=7)
            
            if not successful_analyses:
                return
            
            # Extract patterns from successful analyses
            patterns = self._extract_knowledge_patterns(successful_analyses)
            
            # Store patterns in memory
            for pattern in patterns:
                self.memory.store_knowledge_pattern(
                    pattern_type=pattern['type'],
                    pattern_text=pattern['text'],
                    pattern_rules=json.dumps(pattern['rules']),
                    effectiveness_score=pattern['score']
                )
            
            logger.info(f"📚 Updated {len(patterns)} knowledge patterns")
            
        except Exception as e:
            logger.error(f"❌ Error updating knowledge patterns: {e}")
    
    def _get_successful_analyses(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get successful analyses from the specified time period."""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        analyses = self._get_recent_analyses(hours=days * 24)
        
        # Filter for high-confidence analyses
        successful = [
            analysis for analysis in analyses 
            if analysis.get('confidence', 0) > 0.8
        ]
        
        return successful
    
    def _extract_knowledge_patterns(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract reusable knowledge patterns from successful analyses."""
        patterns = []
        
        # Group analyses by type
        by_type = {}
        for analysis in analyses:
            analysis_type = analysis['analysis_type']
            if analysis_type not in by_type:
                by_type[analysis_type] = []
            by_type[analysis_type].append(analysis)
        
        # Extract patterns for each type
        for analysis_type, type_analyses in by_type.items():
            if analysis_type == 'ioc_classification':
                patterns.extend(self._extract_classification_patterns(type_analyses))
            elif analysis_type == 'ttp_mapping':
                patterns.extend(self._extract_ttp_patterns(type_analyses))
        
        return patterns
    
    def _extract_classification_patterns(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract classification patterns from successful analyses."""
        patterns = []
        
        # Group by risk level and category
        risk_groups = {}
        for analysis in analyses:
            output = analysis.get('output_data', {})
            if isinstance(output, str):
                try:
                    output = json.loads(output)
                except:
                    continue
            
            risk_level = output.get('risk_level', 'UNKNOWN')
            category = output.get('category', 'unknown')
            
            key = f"{risk_level}_{category}"
            if key not in risk_groups:
                risk_groups[key] = []
            risk_groups[key].append(analysis)
        
        # Extract patterns for each group
        for group_key, group_analyses in risk_groups.items():
            if len(group_analyses) >= 5:  # Minimum occurrences for pattern
                pattern = self._create_classification_pattern(group_key, group_analyses)
                if pattern:
                    patterns.append(pattern)
        
        return patterns
    
    def _create_classification_pattern(self, group_key: str, analyses: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create a classification pattern from grouped analyses."""
        try:
            risk_level, category = group_key.split('_', 1)
            
            # Extract common input characteristics
            common_features = []
            for analysis in analyses:
                input_data = analysis.get('input_data', {})
                if isinstance(input_data, str):
                    # Extract features from text input
                    if any(keyword in input_data.lower() for keyword in ['phish', 'banking']):
                        common_features.append('financial_keywords')
                    if any(tld in input_data for tld in ['.tk', '.ml', '.ga']):
                        common_features.append('suspicious_tld')
            
            # Calculate effectiveness score
            avg_confidence = sum(a.get('confidence', 0) for a in analyses) / len(analyses)
            
            return {
                'type': 'classification',
                'text': f"Pattern for {risk_level} {category}",
                'rules': {
                    'risk_level': risk_level,
                    'category': category,
                    'common_features': list(set(common_features)),
                    'sample_count': len(analyses)
                },
                'score': avg_confidence
            }
        
        except Exception as e:
            logger.error(f"❌ Error creating classification pattern: {e}")
            return None
    
    def _extract_ttp_patterns(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract TTP mapping patterns from successful analyses."""
        # Similar implementation for TTP patterns
        return []
    
    def get_learning_status(self) -> Dict[str, Any]:
        """Get the current status of the continuous learning system."""
        return {
            "running": self.running,
            "current_model_version": self.current_model_version,
            "last_training_time": self.last_training_time.isoformat() if self.last_training_time else None,
            "performance_history_count": len(self.performance_history),
            "learning_threshold": self.learning_threshold,
            "min_training_samples": self.min_training_samples
        }
    
    def stop(self):
        """Stop the continuous learning process."""
        self.running = False
        logger.info("⏹️  Continuous learning manager stopped")

# Global continuous learning manager instance
_continuous_learning_manager = None

def get_continuous_learning_manager() -> ContinuousLearningManager:
    """Get the global continuous learning manager instance."""
    global _continuous_learning_manager
    if _continuous_learning_manager is None:
        _continuous_learning_manager = ContinuousLearningManager()
    return _continuous_learning_manager
