"""
CrewAITrainingManager
====================

Manages training and optimization of CrewAI agents based on performance data.
Provides feedback-driven improvement for multi-agent coordination and task execution.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

from ..tools.memory_system import get_memory

logger = logging.getLogger(__name__)

@dataclass
class AgentPerformance:
    agent_name: str
    task_type: str
    success_rate: float
    avg_processing_time: float
    avg_confidence: float
    error_count: int
    last_evaluation: datetime

@dataclass
class TaskExecution:
    task_id: str
    agent_name: str
    task_type: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    execution_time: float
    success: bool
    confidence: float
    error_message: Optional[str]
    timestamp: datetime

class CrewAITrainingManager:
    """
    Manages performance tracking and optimization for CrewAI agents.
    """
    
    def __init__(self):
        self.memory = get_memory()
        self.agent_performances: Dict[str, AgentPerformance] = {}
        self.task_executions: List[TaskExecution] = []
        self.optimization_rules = self._initialize_optimization_rules()
    
    def _initialize_optimization_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize optimization rules for different agent types."""
        return {
            "recon_agent": {
                "min_success_rate": 0.8,
                "max_avg_time": 30.0,  # seconds
                "optimization_prompts": {
                    "low_success": "Focus on verified threat intelligence sources and validate indicators before reporting.",
                    "slow_processing": "Prioritize high-confidence indicators and limit the number of sources queried simultaneously.",
                    "low_confidence": "Include source reliability scores and cross-reference multiple feeds for validation."
                }
            },
            "analyzer_agent": {
                "min_success_rate": 0.85,
                "max_avg_time": 45.0,
                "optimization_prompts": {
                    "low_success": "Use historical IOC patterns and TTP mappings to improve classification accuracy.",
                    "slow_processing": "Leverage cached classifications for known IOC patterns to reduce processing time.",
                    "low_confidence": "Reference MITRE ATT&CK framework more systematically and provide detailed reasoning."
                }
            },
            "exporter_agent": {
                "min_success_rate": 0.9,
                "max_avg_time": 20.0,
                "optimization_prompts": {
                    "low_success": "Follow standardized report templates and ensure all required sections are included.",
                    "slow_processing": "Use predefined Sigma rule templates and focus on high-priority IOCs first.",
                    "low_confidence": "Include confidence scores and evidence links in all generated reports."
                }
            }
        }
    
    def record_task_execution(self, task_id: str, agent_name: str, task_type: str,
                            input_data: Dict[str, Any], output_data: Dict[str, Any],
                            execution_time: float, success: bool, confidence: float = 0.0,
                            error_message: Optional[str] = None):
        """Record the execution of a task by an agent."""
        execution = TaskExecution(
            task_id=task_id,
            agent_name=agent_name,
            task_type=task_type,
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time,
            success=success,
            confidence=confidence,
            error_message=error_message,
            timestamp=datetime.now()
        )
        
        self.task_executions.append(execution)
        
        # Store in memory for persistence
        self.memory.store_analysis(
            session_id=f"crewai_{task_id}",
            analysis_type=f"agent_execution_{agent_name}",
            input_data=input_data,
            output_data={
                "success": success,
                "confidence": confidence,
                "execution_time": execution_time,
                "error_message": error_message,
                "output_data": output_data
            },
            confidence=confidence,
            processing_time=execution_time
        )
        
        # Update agent performance
        self._update_agent_performance(agent_name, task_type, execution)
        
        logger.info(f"📊 Recorded task execution: {agent_name} - {task_type} - {'✅' if success else '❌'}")
    
    def _update_agent_performance(self, agent_name: str, task_type: str, execution: TaskExecution):
        """Update performance metrics for an agent."""
        key = f"{agent_name}_{task_type}"
        
        # Get recent executions for this agent/task combination
        recent_executions = [
            e for e in self.task_executions[-100:]  # Last 100 executions
            if e.agent_name == agent_name and e.task_type == task_type
        ]
        
        if not recent_executions:
            return
        
        # Calculate performance metrics
        success_count = sum(1 for e in recent_executions if e.success)
        success_rate = success_count / len(recent_executions)
        
        avg_processing_time = sum(e.execution_time for e in recent_executions) / len(recent_executions)
        avg_confidence = sum(e.confidence for e in recent_executions) / len(recent_executions)
        error_count = sum(1 for e in recent_executions if not e.success)
        
        # Update or create performance record
        self.agent_performances[key] = AgentPerformance(
            agent_name=agent_name,
            task_type=task_type,
            success_rate=success_rate,
            avg_processing_time=avg_processing_time,
            avg_confidence=avg_confidence,
            error_count=error_count,
            last_evaluation=datetime.now()
        )
    
    def analyze_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Analyze the performance of a specific agent."""
        agent_performances = {
            k: v for k, v in self.agent_performances.items() 
            if v.agent_name == agent_name
        }
        
        if not agent_performances:
            return {"status": "no_data", "agent": agent_name}
        
        analysis = {
            "agent": agent_name,
            "overall_status": "good",
            "task_performances": {},
            "recommendations": [],
            "optimization_needed": False
        }
        
        for key, performance in agent_performances.items():
            task_type = performance.task_type
            
            # Get optimization rules for this agent
            rules = self.optimization_rules.get(agent_name, {})
            min_success_rate = rules.get("min_success_rate", 0.8)
            max_avg_time = rules.get("max_avg_time", 30.0)
            
            # Analyze performance against rules
            task_status = "good"
            issues = []
            
            if performance.success_rate < min_success_rate:
                task_status = "poor"
                issues.append("low_success_rate")
                analysis["optimization_needed"] = True
            
            if performance.avg_processing_time > max_avg_time:
                task_status = "slow"
                issues.append("slow_processing")
                analysis["optimization_needed"] = True
            
            if performance.avg_confidence < 0.7:
                if task_status == "good":
                    task_status = "low_confidence"
                issues.append("low_confidence")
                analysis["optimization_needed"] = True
            
            # Generate recommendations
            recommendations = self._generate_recommendations(agent_name, issues)
            
            analysis["task_performances"][task_type] = {
                "status": task_status,
                "success_rate": performance.success_rate,
                "avg_processing_time": performance.avg_processing_time,
                "avg_confidence": performance.avg_confidence,
                "error_count": performance.error_count,
                "issues": issues,
                "recommendations": recommendations
            }
            
            # Update overall status
            if task_status in ["poor", "slow"] and analysis["overall_status"] == "good":
                analysis["overall_status"] = task_status
            elif task_status == "poor":
                analysis["overall_status"] = "poor"
        
        return analysis
    
    def _generate_recommendations(self, agent_name: str, issues: List[str]) -> List[str]:
        """Generate specific recommendations for agent improvement."""
        recommendations = []
        rules = self.optimization_rules.get(agent_name, {})
        optimization_prompts = rules.get("optimization_prompts", {})
        
        for issue in issues:
            if issue in optimization_prompts:
                recommendations.append(optimization_prompts[issue])
        
        return recommendations
    
    def get_crew_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of the entire crew's performance."""
        if not self.agent_performances:
            return {"status": "no_data"}
        
        # Analyze each agent
        agent_analyses = {}
        overall_optimization_needed = False
        
        for agent_name in set(p.agent_name for p in self.agent_performances.values()):
            analysis = self.analyze_agent_performance(agent_name)
            agent_analyses[agent_name] = analysis
            
            if analysis.get("optimization_needed", False):
                overall_optimization_needed = True
        
        # Calculate crew-wide metrics
        all_performances = list(self.agent_performances.values())
        crew_success_rate = sum(p.success_rate for p in all_performances) / len(all_performances)
        crew_avg_time = sum(p.avg_processing_time for p in all_performances) / len(all_performances)
        crew_avg_confidence = sum(p.avg_confidence for p in all_performances) / len(all_performances)
        
        return {
            "overall_status": "needs_optimization" if overall_optimization_needed else "good",
            "crew_metrics": {
                "success_rate": crew_success_rate,
                "avg_processing_time": crew_avg_time,
                "avg_confidence": crew_avg_confidence
            },
            "agent_analyses": agent_analyses,
            "optimization_needed": overall_optimization_needed,
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_agent_optimization_prompts(self, agent_name: str) -> Dict[str, str]:
        """Generate optimization prompts for a specific agent."""
        analysis = self.analyze_agent_performance(agent_name)
        
        if not analysis.get("optimization_needed", False):
            return {"status": "no_optimization_needed"}
        
        optimization_prompts = {}
        
        for task_type, task_performance in analysis.get("task_performances", {}).items():
            if task_performance.get("recommendations"):
                # Create enhanced system prompt
                base_prompt = self._get_base_agent_prompt(agent_name)
                performance_context = self._get_performance_context(agent_name, task_type)
                optimization_guidance = "\n".join(task_performance["recommendations"])
                
                enhanced_prompt = f"""
{base_prompt}

PERFORMANCE OPTIMIZATION GUIDANCE:
{optimization_guidance}

RECENT PERFORMANCE CONTEXT:
{performance_context}

Focus on implementing the above guidance to improve your performance in this task type.
"""
                
                optimization_prompts[task_type] = enhanced_prompt.strip()
        
        return optimization_prompts
    
    def _get_base_agent_prompt(self, agent_name: str) -> str:
        """Get the base system prompt for an agent."""
        base_prompts = {
            "recon_agent": """You are a cyber threat intelligence specialist focused on gathering and validating threat indicators from open sources. Your primary responsibility is to identify suspicious domains, IPs, and other indicators of compromise (IOCs) from threat intelligence feeds.""",
            
            "analyzer_agent": """You are an experienced cyber threat analyst responsible for classifying IOCs and mapping them to MITRE ATT&CK tactics, techniques, and procedures (TTPs). You provide detailed analysis and context for security teams.""",
            
            "exporter_agent": """You are a SOC analyst specializing in creating actionable threat intelligence reports and detection rules. You transform raw threat data into readable reports and Sigma detection rules for security operations."""
        }
        
        return base_prompts.get(agent_name, "You are a specialized threat intelligence agent.")
    
    def _get_performance_context(self, agent_name: str, task_type: str) -> str:
        """Get performance context for an agent/task combination."""
        key = f"{agent_name}_{task_type}"
        performance = self.agent_performances.get(key)
        
        if not performance:
            return "No recent performance data available."
        
        context = f"""
Current Performance Metrics:
- Success Rate: {performance.success_rate:.1%}
- Average Processing Time: {performance.avg_processing_time:.1f} seconds
- Average Confidence: {performance.avg_confidence:.1%}
- Recent Errors: {performance.error_count}

Focus on improving areas where performance is below optimal thresholds.
"""
        return context.strip()
    
    def get_training_feedback(self, days: int = 7) -> Dict[str, Any]:
        """Get feedback data for training improvements."""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Get recent executions
        recent_executions = [
            e for e in self.task_executions 
            if e.timestamp >= cutoff_time
        ]
        
        if not recent_executions:
            return {"status": "no_recent_data"}
        
        # Analyze patterns in failures
        failures = [e for e in recent_executions if not e.success]
        success_patterns = [e for e in recent_executions if e.success and e.confidence > 0.8]
        
        feedback = {
            "period_days": days,
            "total_executions": len(recent_executions),
            "failure_count": len(failures),
            "high_confidence_successes": len(success_patterns),
            "common_failure_patterns": self._analyze_failure_patterns(failures),
            "success_patterns": self._analyze_success_patterns(success_patterns),
            "agent_specific_feedback": {}
        }
        
        # Generate agent-specific feedback
        for agent_name in set(e.agent_name for e in recent_executions):
            agent_executions = [e for e in recent_executions if e.agent_name == agent_name]
            feedback["agent_specific_feedback"][agent_name] = {
                "executions": len(agent_executions),
                "success_rate": sum(1 for e in agent_executions if e.success) / len(agent_executions),
                "improvement_areas": self._identify_improvement_areas(agent_executions)
            }
        
        return feedback
    
    def _analyze_failure_patterns(self, failures: List[TaskExecution]) -> List[Dict[str, Any]]:
        """Analyze common patterns in task failures."""
        if not failures:
            return []
        
        patterns = []
        
        # Group by error type
        error_groups = {}
        for failure in failures:
            error_key = failure.error_message or "unknown_error"
            if error_key not in error_groups:
                error_groups[error_key] = []
            error_groups[error_key].append(failure)
        
        # Analyze each error group
        for error_type, error_failures in error_groups.items():
            if len(error_failures) >= 2:  # Pattern requires at least 2 occurrences
                patterns.append({
                    "error_type": error_type,
                    "occurrences": len(error_failures),
                    "affected_agents": list(set(f.agent_name for f in error_failures)),
                    "avg_execution_time": sum(f.execution_time for f in error_failures) / len(error_failures)
                })
        
        return patterns
    
    def _analyze_success_patterns(self, successes: List[TaskExecution]) -> List[Dict[str, Any]]:
        """Analyze patterns in successful high-confidence executions."""
        if not successes:
            return []
        
        patterns = []
        
        # Group by agent and task type
        groups = {}
        for success in successes:
            key = f"{success.agent_name}_{success.task_type}"
            if key not in groups:
                groups[key] = []
            groups[key].append(success)
        
        # Analyze each group
        for group_key, group_successes in groups.items():
            if len(group_successes) >= 3:
                agent_name, task_type = group_key.split('_', 1)
                patterns.append({
                    "agent": agent_name,
                    "task_type": task_type,
                    "success_count": len(group_successes),
                    "avg_confidence": sum(s.confidence for s in group_successes) / len(group_successes),
                    "avg_execution_time": sum(s.execution_time for s in group_successes) / len(group_successes)
                })
        
        return patterns
    
    def _identify_improvement_areas(self, executions: List[TaskExecution]) -> List[str]:
        """Identify specific improvement areas for an agent."""
        areas = []
        
        if not executions:
            return areas
        
        success_rate = sum(1 for e in executions if e.success) / len(executions)
        avg_time = sum(e.execution_time for e in executions) / len(executions)
        avg_confidence = sum(e.confidence for e in executions) / len(executions)
        
        if success_rate < 0.8:
            areas.append("improve_success_rate")
        
        if avg_time > 30:
            areas.append("reduce_processing_time")
        
        if avg_confidence < 0.7:
            areas.append("increase_confidence")
        
        # Check for consistency issues
        confidence_values = [e.confidence for e in executions if e.success]
        if confidence_values and (max(confidence_values) - min(confidence_values)) > 0.4:
            areas.append("improve_consistency")
        
        return areas

# Global CrewAI training manager instance
_crewai_training_manager = None

def get_crewai_training_manager() -> CrewAITrainingManager:
    """Get the global CrewAI training manager instance."""
    global _crewai_training_manager
    if _crewai_training_manager is None:
        _crewai_training_manager = CrewAITrainingManager()
    return _crewai_training_manager
