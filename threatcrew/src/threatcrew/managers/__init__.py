"""
ThreatAgent Managers Package
===========================

This package contains management systems for the ThreatAgent threat intelligence platform:

- ThreatFeedManager: Real-time threat feed ingestion and processing
- ContinuousLearningManager: Automated model improvement and retraining
- CrewAITrainingManager: Performance tracking and optimization for CrewAI agents
"""

from .threat_feed_manager import ThreatFeedManager, get_threat_feed_manager
from .continuous_learning_manager import ContinuousLearningManager, get_continuous_learning_manager
from .crewai_training_manager import CrewAITrainingManager, get_crewai_training_manager

__all__ = [
    'ThreatFeedManager',
    'get_threat_feed_manager',
    'ContinuousLearningManager', 
    'get_continuous_learning_manager',
    'CrewAITrainingManager',
    'get_crewai_training_manager'
]
