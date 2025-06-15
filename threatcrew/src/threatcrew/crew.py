from crewai import Crew, Agent, Task
import os
import uuid
import time
import logging
from datetime import datetime
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import OllamaEmbeddings # Import OllamaEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure LLM
def get_llm():
    raw_model_name = os.getenv('MODEL', 'threat-intelligence') 
    
    # Extract the actual model name for OllamaLLM
    # OllamaLLM expects the model name as known by Ollama server (e.g., "llama3")
    # not the LiteLLM-style prefixed name (e.g., "ollama/llama3").
    if "/" in raw_model_name:
        actual_model_name = raw_model_name.split('/')[-1]
    else:
        actual_model_name = raw_model_name
    
    ollama_base_url = os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')
    logger.info(f"Configuring OllamaLLM with model: '{actual_model_name}', base_url: '{ollama_base_url}', num_predict: 2048")

    return OllamaLLM(
        model=actual_model_name, 
        base_url=ollama_base_url,
        temperature=0.1,
        num_predict=2048, # Increased from 512
        stop=["\\n\\n", "Human:", "Assistant:"],
        request_timeout=120.0 
    )

# Tools imports
from threatcrew.tools.osint_scraper import run as scrape_osint
from threatcrew.tools.llm_classifier import run as classify_iocs
from threatcrew.tools.ttp_mapper import run as map_ttps
from threatcrew.tools.report_writer import run as write_report
from threatcrew.tools.rule_generator import run as generate_rules
from threatcrew.tools.memory_system import get_memory
from threatcrew.tools.finetuning_system import ThreatFineTuner

# Get the LLM instance
llm = get_llm()
memory = get_memory() # This is your custom memory system, not directly ChromaDB for agent memory
finetuner = ThreatFineTuner()

# It seems CrewAI might be trying to use a default OpenAI embedding for its own memory/RAG if not specified.
# Let's try to provide a local embedding function to the Agent's memory configuration.
# This is separate from your custom `memory_system` and pertains to CrewAI's internal memory capabilities.

def get_embedding_function():
    return OllamaEmbeddings(
        model=os.getenv('MODEL', 'threat-intelligence'), # Use the same model for embeddings if suitable, or a dedicated embedding model
        base_url=os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')
    )

embedding_function = get_embedding_function()

# Memory-enhanced agents with performance tracking
from threatcrew.managers import get_crewai_training_manager

training_manager = get_crewai_training_manager()

def create_memory_enhanced_agent(role: str, goal: str, backstory: str, tools: list, 
                                agent_name: str, targeting_config: dict = None) -> Agent:
    """Create an agent with memory-enhanced capabilities and performance tracking."""
    
    # Get historical performance data for context
    performance_analysis = training_manager.analyze_agent_performance(agent_name)
    optimization_prompts = training_manager.generate_agent_optimization_prompts(agent_name)
    
    # Enhance backstory with memory context
    memory_context = memory.get_historical_context(agent_name)
    enhanced_backstory = f"""{backstory}

MEMORY CONTEXT:
You have access to historical threat intelligence data including:
- {len(memory_context.get('iocs', []))} previously analyzed IOCs
- {len(memory_context.get('ttp_mappings', []))} TTP mappings
- {len(memory_context.get('analysis_history', []))} past analyses

Use this historical context to improve your analysis accuracy and consistency.
"""
    
    # Add performance optimization guidance if needed
    if optimization_prompts and agent_name in optimization_prompts:
        for task_type, prompt in optimization_prompts.items():
            enhanced_backstory += f"\n\nOPTIMIZATION GUIDANCE for {task_type}:\n{prompt}"

    # Add targeting guidance if provided
    if targeting_config:
        campaign_name = targeting_config.get('campaign_name', 'Unnamed Campaign')
        num_targets = len(targeting_config.get('targets', []))
        threat_types_summary = ', '.join(targeting_config.get('threat_types', ['any'])[:3])
        if len(targeting_config.get('threat_types', [])) > 3:
            threat_types_summary += "..."
            
        enhanced_backstory += f"""

TARGETING GUIDANCE (Campaign: {campaign_name}):
- Focus your efforts on {num_targets} specific targets.
- Prioritize threat types: {threat_types_summary}.
- Utilize provided search filters and keywords for this campaign.
"""
        if agent_name == "recon_agent" and targeting_config.get('search_filters'):
            filters_summary = str(targeting_config['search_filters'])[:200] # Keep it brief
            enhanced_backstory += f"- Specific OSINT search filters: {filters_summary}...\\n"
        elif agent_name == "analyzer_agent" and targeting_config.get('targets'):
            target_details = str(targeting_config['targets'])[:200] # Keep it brief
            enhanced_backstory += f"- Analyze IOCs relevant to: {target_details}...\\n"
        elif agent_name == "exporter_agent" and targeting_config.get('campaign_name'):
             enhanced_backstory += f"- Tailor reports for campaign '{campaign_name}'.\\n"

    return Agent(
        role=role,
        goal=goal,
        backstory=enhanced_backstory,
        tools=tools,
        llm=llm,
        max_iter=3,
        verbose=True,
        memory=True  # Enable CrewAI memory features
    )

# Define agents with memory enhancement
recon_agent = create_memory_enhanced_agent(
    role='Memory-Enhanced Recon Specialist',
    goal='Scan external threat intelligence feeds and extract suspicious domains. Use targeting parameters if provided.',
    backstory=(
        'An expert in OSINT and threat reconnaissance, equipped with advanced tools and historical knowledge. \n'
        'You meticulously scan various sources for potential threats, focusing on accuracy and relevance. \n'
        'You adapt your search based on ongoing campaign targets and threat landscapes.'
    ),
    tools=[scrape_osint],
    agent_name="recon_agent"
)

analyzer_agent = create_memory_enhanced_agent(
    role='Memory-Enhanced IOC Analyst',
    goal='Classify suspicious domains and map them to MITRE ATT&CK TTPs. Use targeting parameters if provided.',
    backstory=(
        'A seasoned cybersecurity analyst specializing in IOC classification and TTP mapping. \n'
        'You leverage historical data and advanced analytical techniques to determine threat severity and actor tactics. \n'
        'Your analysis is crucial for understanding the nature of identified threats, especially those relevant to active campaigns.'
    ),
    tools=[classify_iocs, map_ttps],
    agent_name="analyzer_agent"
)

exporter_agent = create_memory_enhanced_agent(
    role='Memory-Enhanced Threat Report Exporter',
    goal='Generate comprehensive threat intelligence reports and actionable security rules. Use targeting parameters if provided.',
    backstory=(
        'A skilled technical writer and security strategist, adept at translating complex threat data into clear, actionable insights. \n'
        'You produce detailed reports for stakeholders and generate security rules for automated defense systems. \n'
        'Your reports are tailored to the specific needs and context of the ongoing threat intelligence campaigns.'
    ),
    tools=[write_report, generate_rules],
    agent_name="exporter_agent"
)

# Define tasks with performance tracking and targeting context
def create_tracked_task(description: str, agent: Agent, task_name: str, 
                        expected_output: str, targeting_config: dict = None) -> Task:
    """Create a task with performance tracking and context injection."""
    
    # Enhance description with memory and performance guidance
    enhanced_description = f"""{description}

MEMORY GUIDANCE:
- Use historical patterns from similar past analyses
- Reference previous successful approaches for this task type
- Learn from past errors and avoid known failure patterns
- Maintain consistency with established classification standards

PERFORMANCE EXPECTATIONS:
- Provide confidence scores for all conclusions
- Include reasoning and evidence for decisions
- Process efficiently while maintaining accuracy
- Flag any unusual patterns for review
"""
    # Add targeting context if provided
    if targeting_config:
        campaign_name = targeting_config.get('campaign_name', 'Unnamed Campaign')
        search_filters_summary = str(targeting_config.get('search_filters', {}))[:150]
        threat_types_summary = ', '.join(targeting_config.get('threat_types', ['any'])[:3])
        if len(targeting_config.get('threat_types', [])) > 3:
            threat_types_summary += "..."

        enhanced_description = f"""TARGETING CONTEXT (Campaign: {campaign_name}):
- Focus on intelligence relevant to the current campaign: {campaign_name}.
- Utilize campaign-specific keywords and filters: {search_filters_summary}...
- Prioritize threats matching campaign objectives: {threat_types_summary}.

{enhanced_description}
"""

    return Task(
        description=enhanced_description,
        agent=agent,
        expected_output=expected_output,
        # Ensure the task uses the agent's LLM, which is already configured
    )

# Enhanced memory-aware agents
recon_agent = create_memory_enhanced_agent(
    role="Memory-Enhanced Recon Specialist",
    goal="Scan OSINT sources for suspicious indicators using historical threat patterns and current targeting parameters.",
    backstory="""You are a cyber threat intelligence analyst specializing in gathering phishing and 
    threat domains from open sources. You leverage historical threat data and specific campaign 
    targeting parameters to identify patterns and improve detection accuracy. 
    You learn from previous discoveries to enhance future reconnaissance.""",
    tools=[scrape_osint],
    agent_name="recon_agent"
)

analyzer_agent = create_memory_enhanced_agent(
    role="Memory-Enhanced Threat Analyst",
    goal="Classify IOCs and map them to MITRE TTPs using historical patterns, learned behaviors, and campaign-specific targets.",
    backstory="""You are an experienced cyber analyst who enriches threat data with context and 
    classification. You use historical IOC patterns, past TTP mappings, learned threat behaviors, 
    and current campaign targets to provide accurate analysis. Your classifications improve over time 
    through continuous learning and focused targeting.""",
    tools=[classify_iocs, map_ttps],
    agent_name="analyzer_agent"
)

exporter_agent = create_memory_enhanced_agent(
    role="Memory-Enhanced Intel Exporter",
    goal="Generate comprehensive reports and detection rules using historical analysis patterns and tailored to the current campaign focus.",
    backstory="""You are a SOC analyst who prepares detection content and documentation for security 
    teams. You leverage historical report patterns, successful detection rules, past analysis results, 
    and current campaign objectives to create high-quality, actionable intelligence products.""",
    tools=[write_report, generate_rules],
    agent_name="exporter_agent"
)

# Enhanced memory-aware tasks with performance tracking
def create_tracked_task(description: str, expected_output: str, agent: Agent, 
                       task_type: str, context: list = None, targeting_config: dict = None) -> Task:
    """Create a task with performance tracking capabilities and targeting awareness."""
    
    # Add memory context to task description
    memory_enhanced_description = f"""{description}

MEMORY GUIDANCE:
- Use historical patterns from similar past analyses
- Reference previous successful approaches for this task type
- Learn from past errors and avoid known failure patterns
- Maintain consistency with established classification standards

PERFORMANCE EXPECTATIONS:
- Provide confidence scores for all conclusions
- Include reasoning and evidence for decisions
- Process efficiently while maintaining accuracy
- Flag any unusual patterns for review
"""

    # Add targeting context to task description if provided
    if targeting_config:
        campaign_name = targeting_config.get('campaign_name', 'Default Campaign')
        search_filters = targeting_config.get('search_filters', {})
        
        targeting_guidance = f"""TARGETING CONTEXT (Campaign: {campaign_name}):
- Focus on intelligence relevant to the current campaign: {campaign_name}.
- Utilize campaign-specific keywords and filters: {str(search_filters)[:200]}...
- Prioritize threats matching campaign objectives: {', '.join(targeting_config.get('threat_types', ['any'])[:3])}.
"""
        memory_enhanced_description = f"{targeting_guidance}\n{memory_enhanced_description}"
    
    return Task(
        description=memory_enhanced_description,
        expected_output=expected_output,
        agent=agent,
        context=context or []
    )

recon_task = create_tracked_task(
    description="""
    Please scan external threat intelligence feeds and extract suspicious domains.
    Use the OSINT Scraper tool to collect potential threat indicators.
    Focus on domains that match historical phishing and malware patterns, 
    and align with current campaign targeting parameters if provided.
    Return a list of suspicious domains with confidence scores.
    """,
    expected_output="A list of suspicious domains from OSINT sources with confidence scores and reasoning, aligned with targeting.",
    agent=recon_agent,
    task_type="osint_collection"
)

analyzer_task = create_tracked_task(
    description="""
    Take the list of domains from the previous task and:
    1. Classify each indicator using the IOC Classifier tool with memory-enhanced context and campaign targets.
    2. Map the classified IOCs to MITRE ATT&CK TTPs using historical TTP patterns and campaign relevance.
    3. Use past analysis results and current targeting to improve accuracy and consistency.
    4. Provide confidence scores and detailed reasoning for each classification.
    Return a list with classifications, mappings, and confidence assessments, relevant to the campaign.
    """,
    expected_output="A list of classified and enriched IOCs with risk levels, TTPs, confidence scores, and historical context, focused on campaign targets.",
    agent=analyzer_agent,
    task_type="ioc_analysis",
    context=[recon_task]
)

exporter_task = create_tracked_task(
    description="""
    Take the enriched threat data and:
    1. Generate a comprehensive markdown report using historical report templates, tailored to the current campaign.
    2. Create Sigma detection rules based on successful past patterns and relevant to campaign targets.
    3. Include confidence assessments and source attribution.
    4. Reference similar past incidents and their outcomes, focusing on campaign relevance.
    Return both the enhanced report and optimized detection rules, aligned with the campaign.
    """,
    expected_output="A comprehensive markdown report and optimized Sigma detection rules with historical context, tailored to the campaign.",
    agent=exporter_agent,
    task_type="report_generation",
    context=[analyzer_task]
)

# Enhanced Crew with memory and performance tracking
class MemoryEnhancedCrew:
    """Enhanced Crew with memory capabilities and performance tracking."""
    
    def __init__(self):
        self.agents = {
            "recon_agent": recon_agent,
            "analyzer_agent": analyzer_agent,
            "exporter_agent": exporter_agent
        }
        self.tasks = {
            "recon_task": recon_task,
            "analyzer_task": analyzer_task,
            "exporter_task": exporter_task
        }
        self.session_id_base = f"crew_session_{int(time.time())}"
        self.crew = None # Will be initialized in kickoff
        
    def kickoff(self, inputs: dict = None) -> dict:
        """Execute the crew workflow with performance tracking and targeting."""
        import time
        start_time = time.time()
        self.session_id = f"{self.session_id_base}_{str(uuid.uuid4())[:8]}"
        
        targeting_config = inputs.pop('targeting_config', None) if inputs else None
        
        # Re-create agents and tasks with targeting config if provided
        current_agents = [self.agents["recon_agent"], self.agents["analyzer_agent"], self.agents["exporter_agent"]]
        current_tasks = [self.tasks["recon_task"], self.tasks["analyzer_task"], self.tasks["exporter_task"]]

        if targeting_config:
            logger.info(f"🎯 Applying targeting configuration: {targeting_config.get('campaign_name')}")
            # Create new instances of agents with targeting config
            targeted_recon_agent = create_memory_enhanced_agent(
                role=recon_agent.role, goal=recon_agent.goal, backstory=recon_agent.backstory,
                tools=recon_agent.tools, agent_name="recon_agent", targeting_config=targeting_config
            )
            targeted_analyzer_agent = create_memory_enhanced_agent(
                role=analyzer_agent.role, goal=analyzer_agent.goal, backstory=analyzer_agent.backstory,
                tools=analyzer_agent.tools, agent_name="analyzer_agent", targeting_config=targeting_config
            )
            targeted_exporter_agent = create_memory_enhanced_agent(
                role=exporter_agent.role, goal=exporter_agent.goal, backstory=exporter_agent.backstory,
                tools=exporter_agent.tools, agent_name="exporter_agent", targeting_config=targeting_config
            )
            current_agents = [targeted_recon_agent, targeted_analyzer_agent, targeted_exporter_agent]
            
            # Create new instances of tasks with targeting config and updated agents
            targeted_recon_task = create_tracked_task(
                description=recon_task.description, expected_output=recon_task.expected_output,
                agent=targeted_recon_agent, task_type="osint_collection", targeting_config=targeting_config
            )
            targeted_analyzer_task = create_tracked_task(
                description=analyzer_task.description, expected_output=analyzer_task.expected_output,
                agent=targeted_analyzer_agent, task_type="ioc_analysis", context=[targeted_recon_task], 
                targeting_config=targeting_config
            )
            targeted_exporter_task = create_tracked_task(
                description=exporter_task.description, expected_output=exporter_task.expected_output,
                agent=targeted_exporter_agent, task_type="report_generation", context=[targeted_analyzer_task],
                targeting_config=targeting_config
            )
            current_tasks = [targeted_recon_task, targeted_analyzer_task, targeted_exporter_task]

        self.crew = Crew(
            agents=current_agents,
            tasks=current_tasks,
            memory=True,  # Enable CrewAI memory
            verbose=True,
            process="sequential"  # Can be changed to "hierarchical" for complex workflows
        )
        
        try:
            # Execute the crew workflow
            result = self.crew.kickoff(inputs=inputs or {})
            
            execution_time = time.time() - start_time
            
            # Track successful execution
            training_manager.record_task_execution(
                task_id=self.session_id,
                agent_name="crew_workflow",
                task_type="full_workflow", 
                input_data=inputs or {},
                output_data={"result": str(result)},
                execution_time=execution_time,
                success=True,
                confidence=0.8  # Default confidence for successful workflow
            )
            
            # Store workflow result in memory
            memory.store_analysis(
                session_id=self.session_id,
                analysis_type="crew_workflow",
                input_data=inputs or {},
                output_data=result,
                processing_time=execution_time
            )
            
            logger.info(f"✅ Crew workflow completed successfully in {execution_time:.2f}s")
            
            return {
                "status": "success",
                "result": result,
                "execution_time": execution_time,
                "session_id": self.session_id
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Track failed execution
            training_manager.record_task_execution(
                task_id=self.session_id,
                agent_name="crew_workflow",
                task_type="full_workflow",
                input_data=inputs or {},
                output_data={},
                execution_time=execution_time,
                success=False,
                confidence=0.0,
                error_message=str(e)
            )
            
            logger.error(f"❌ Crew workflow failed: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "execution_time": execution_time,
                "session_id": self.session_id
            }

# Create the enhanced crew instance
crew = MemoryEnhancedCrew()

# Additional utility functions for monitoring and management
def get_crew_performance_summary():
    """Get a summary of crew performance."""
    return training_manager.get_crew_performance_summary()

def get_memory_stats():
    """Get memory system statistics."""
    return memory.get_statistics()

def get_learning_status():
    """Get continuous learning status."""
    from threatcrew.managers import get_continuous_learning_manager
    learning_manager = get_continuous_learning_manager()
    return learning_manager.get_learning_status()

def trigger_manual_training():
    """Manually trigger a training update."""
    try:
        # Generate new training dataset
        dataset_path = finetuner.generate_training_dataset()
        
        # Create training configuration
        training_config = finetuner.create_training_configuration(
            dataset_path=dataset_path,
            model_name=f"threat-intelligence-manual-{int(time.time())}",
            learning_rate=0.0001,
            epochs=3,
            batch_size=4
        )
        
        # Generate Ollama Modelfile
        modelfile_path = finetuner.generate_ollama_modelfile(
            base_model="llama3",
            dataset_path=dataset_path,
            model_name=training_config["model_name"]
        )
        
        return {
            "status": "success",
            "dataset_path": dataset_path,
            "modelfile_path": modelfile_path,
            "training_config": training_config
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Export the main crew and utility functions
__all__ = [
    'crew',
    'get_crew_performance_summary',
    'get_memory_stats', 
    'get_learning_status',
    'trigger_manual_training',
    'MemoryEnhancedCrew'
]
