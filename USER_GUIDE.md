# 🕵️ ThreatAgent Complete User Guide
**AI-Powered Threat Intelligence Automation System**

---

## 🚀 **Quick Start (5 Minutes)**

### **1. System Health Check**
```bash
cd /Users/noobita/Desktop/Github/ThreatAgent
python3 threatcrew/tests/verify_system.py
```
**Expected Output:** `🚀 System Status: HEALTHY - Ready for production use!`

### **2. Start the Web Interface**
```bash
streamlit run ui/threatagent_app.py --server.port 8502
```
**Access:** Open browser to `http://localhost:8502`

### **3. Run Your First Threat Analysis**
- Go to **Campaign Mode** → **Create Campaign** tab
- Fill in: Company Name: `ACME Corp`, Industry: `technology`
- Click **"🚀 Create & Execute Full Intelligence Workflow"**
- Watch the 8-step automated process complete!

---

## 🎯 **Complete Usage Guide**

### **A. Web Interface (Recommended for Beginners)**

#### **🌐 Access the UI**
```bash
cd /Users/noobita/Desktop/Github/ThreatAgent
streamlit run ui/threatagent_app.py --server.port 8502
# Open: http://localhost:8502
```

#### **📊 Dashboard Mode - System Automation**
**Purpose:** Run all system validation and scripts

1. **Select Scripts:** Choose from 8 available system scripts
2. **Run Automation:** Click "Run Selected Scripts"
3. **Monitor Progress:** Each script shows purpose, output, and next steps

**Recommended First Run:**
- ✅ System Verification
- ✅ Memory & Fine-tuning Setup  
- ✅ Simple Memory Test

#### **🎯 Campaign Mode - Threat Intelligence Campaigns**

##### **Basic Campaign Creation:**
1. **Fill Form:**
   - Company Name: `Target Company Inc.`
   - Industry: Select from dropdown (financial_services, technology, etc.)
   - Domains: `targetcompany.com, target-corp.net`
   - Threat Types: Select multiple (phishing, malware, ransomware)
   - Geographic Focus: Select regions (US, EU, global)

2. **Execute Campaign:** Click "🚀 Create & Execute Full Intelligence Workflow"

3. **Watch Progress:** 8-step automated process:
   - Step 1: Campaign file creation
   - Step 2: Intelligence target enrichment
   - Step 3: Memory database setup
   - Step 4: System verification
   - Step 5: OSINT reconnaissance
   - Step 6: Complete threat analysis
   - Step 7: Intelligence report generation
   - Step 8: Results display

##### **Advanced Targeting:**
1. **Company Targets:** Add multiple companies with domains and priorities
2. **Industry Targets:** Target entire industry sectors with regional focus
3. **Advanced Settings:** Configure memory enhancement, confidence thresholds
4. **Custom Configuration:** Set timeout, max results, continuous monitoring

##### **Interactive Campaign Mode:**
1. **Step-by-Step Creation:** 6-step guided process
2. **Progressive Input:** Company → Domains → Industry → Geographic → Review → Execute
3. **Visual Progress:** Progress bar and step-by-step guidance

#### **🤖 Interactive Console - CLI in Web**
**Purpose:** Command-line interface within the web browser

**Available Commands:**
```
run        - Execute threat intelligence workflow
status     - Show system health
train      - Trigger model training
summary    - Show system statistics
memory     - Memory database stats
list       - List available campaigns
target <name> - Set active campaign
create <name> - Create new campaign
enhanced   - Switch to enhanced mode
simple     - Switch to simple mode
crew       - Switch to crew mode
quit       - Clear console
```

**Example Session:**
```
ThreatAgent> status
📊 System status: Healthy
   Checks: 10/10 passed (100.0%)

ThreatAgent> create my_campaign
📝 Campaign created: threat_campaign_my_campaign_20250615_154530.yaml

ThreatAgent> run
🚀 Executing threat intelligence workflow...
✅ Workflow completed successfully
```

#### **🎓 Training Center - AI Model Management**
**Purpose:** Train and optimize the threat intelligence AI model

##### **Quick Training:**
- **Full System Setup:** Complete memory and model initialization
- **Memory Database Only:** Update threat intelligence database
- **Model Training Only:** Fine-tune the AI model
- **Validate Training:** Test model quality

##### **Advanced Training:**
- **Custom Parameters:** Learning rate, batch size, epochs
- **Data Upload:** Add your own threat intelligence data (JSONL format)
- **Performance Metrics:** View training accuracy, loss, F1 score
- **Model Comparison:** Compare different model versions

#### **🔄 Real-time Monitor - System Health**
**Purpose:** Live monitoring and system status

**Features:**
- **System Overview:** Memory DB, Custom Model, CrewAI Agents status
- **Health Checks:** Quick system verification
- **Memory Statistics:** Database performance metrics
- **Recent Activity:** Latest campaigns and modifications

---

### **B. Command Line Interface (Advanced Users)**

#### **🖥️ CLI Access**
```bash
cd /Users/noobita/Desktop/Github/ThreatAgent/threatcrew
```

#### **Interactive Mode (Recommended)**
```bash
python3 src/threatcrew/main.py interactive
```

**Available Commands:**
- `run` - Execute threat intelligence workflow
- `status` - Show system status
- `train` - Trigger manual training
- `summary` - Show system summary
- `quit` - Exit system

#### **Direct Execution Modes**
```bash
# Simple workflow
python3 src/threatcrew/main.py simple

# Full CrewAI workflow
python3 src/threatcrew/main.py crew

# Targeted workflow (interactive setup)
python3 src/threatcrew/main.py targeted
```

#### **Individual Script Execution**
```bash
# System verification
python3 verify_system.py

# Memory system test
python3 simple_memory_test.py

# Complete system demo
python3 demo_complete_system.py

# Targeting system demo
python3 demo_targeting_system.py

# Setup and training
python3 setup_memory_finetuning.py

# Direct workflow execution
python3 simple_run.py

# System validation
python3 crewagents_validation.py
```

---

## 🎯 **Use Case Examples**

### **Use Case 1: Financial Services Threat Analysis**
**Scenario:** Analyze threats targeting a bank

1. **Via UI:**
   - Campaign Mode → Create Campaign
   - Company: "First National Bank"
   - Industry: "financial_services" 
   - Domains: "firstnational.com, fnb.net"
   - Threat Types: ["phishing", "business_email_compromise", "credential_theft"]
   - Execute workflow

2. **Via CLI:**
   ```bash
   python3 src/threatcrew/main.py targeted
   # Enter: First National Bank
   # Enter: firstnational.com
   # Enter: financial_services
   # Enter: phishing,business_email_compromise
   ```

**Expected Results:**
- Banking-specific phishing domains identified
- Financial sector threat patterns analyzed
- Regulatory compliance report generated
- MITRE ATT&CK mappings for financial threats

### **Use Case 2: Critical Infrastructure Analysis**
**Scenario:** Monitor threats against energy sector

1. **Via UI Advanced Targeting:**
   - Add Industry Target: "energy"
   - Geographic Focus: ["US", "EU"]
   - Threat Types: ["apt", "supply_chain", "insider_threat"]
   - Priority: 5 (highest)
   - Enable continuous monitoring

**Expected Results:**
- APT group activity targeting energy sector
- Supply chain vulnerability analysis
- Critical infrastructure specific IOCs
- Geopolitical threat landscape

### **Use Case 3: Technology Company Monitoring**
**Scenario:** Ongoing threat monitoring for a tech startup

1. **Via UI Interactive Mode:**
   - Step 1: Company: "TechStart Inc."
   - Step 2: Domains: "techstart.io, techstart-app.com"
   - Step 3: Industry: "technology", Threats: ["malware", "ransomware"]
   - Step 4: Geographic: ["global"]
   - Step 5: Review and approve
   - Step 6: Execute with continuous monitoring

**Expected Results:**
- Technology sector threat trends
- Startup-specific threat vectors
- Cloud security threat analysis
- Developer-focused phishing campaigns

---

## 📋 **Workflow Outputs**

### **Campaign Files**
**Location:** Root directory  
**Format:** `threat_campaign_<company>_<timestamp>.yaml`  
**Contents:**
- Campaign configuration
- Targeting parameters
- Threat types and priorities
- Execution metadata

### **Intelligence Reports**
**Format:** Markdown reports  
**Contents:**
- Executive summary
- IOC analysis with risk levels
- MITRE ATT&CK TTP mappings
- Actionable recommendations
- Sigma detection rules

### **Memory Database**
**Location:** `threatcrew/src/knowledge/threat_memory.db`  
**Contents:**
- Historical IOC analysis
- Threat pattern learning
- Similarity relationships
- Risk assessments

### **Training Data**
**Location:** `threatcrew/src/knowledge/training_data/`  
**Format:** JSONL files  
**Contents:**
- Threat intelligence examples
- IOC classifications
- Model training datasets

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **System Health Check Fails**
```bash
python3 threatcrew/verify_system.py
```
**Solutions:**
- Missing components: Run `python3 threatcrew/setup_memory_finetuning.py`
- Ollama not running: Start with `ollama serve`
- Missing model: Run `ollama pull llama3`

#### **Memory Database Issues**
```bash
python3 threatcrew/simple_memory_test.py
```
**Solutions:**
- Database missing: Run setup scripts first
- Permission issues: Check file permissions
- SQLite errors: Recreate database

#### **UI Not Loading**
```bash
streamlit run ui/threatagent_app.py --server.port 8502
```
**Solutions:**
- Port conflict: Try different port (`--server.port 8503`)
- Python path: Ensure you're in the ThreatAgent directory
- Dependencies: Check Streamlit installation

#### **Campaign Execution Fails**
**Check:**
1. System health: `python3 threatcrew/verify_system.py`
2. Memory system: `python3 threatcrew/simple_memory_test.py`
3. Basic workflow: `python3 threatcrew/simple_run.py`

### **Performance Optimization**

#### **Speed Up Analysis**
- Use specific threat types (avoid "all")
- Limit geographic scope
- Set reasonable confidence thresholds
- Use targeted company lists

#### **Improve Accuracy**
- Train with custom data
- Update memory database regularly
- Use industry-specific configurations
- Validate and refine threat types

---

## 📊 **System Monitoring**

### **Health Checks**
```bash
# Complete system verification
python3 threatcrew/verify_system.py

# Memory system status
python3 threatcrew/simple_memory_test.py

# Agent validation
python3 threatcrew/crewagents_validation.py
```

### **Performance Metrics**
- **System Health:** 10/10 checks passing (100%)
- **Memory Database:** 126,976 bytes with 11 IOCs
- **Test Coverage:** 11/11 tests passing (100%)
- **Response Time:** 5-15 minutes per campaign

---

## 🎓 **Best Practices**

### **For Beginners**
1. **Start with UI Dashboard Mode** - Run system verification first
2. **Use Basic Campaign Mode** - Simple company + industry targeting
3. **Monitor Real-time tab** - Check system health regularly
4. **Review outputs carefully** - Understand report structure

### **For Advanced Users**
1. **Use CLI Interactive Mode** - More precise control
2. **Configure Advanced Targeting** - Multi-company, industry focus
3. **Train Custom Models** - Add your threat intelligence data
4. **Automate with Scripts** - Integrate into your security workflow

### **For Security Teams**
1. **Set up Continuous Monitoring** - Enable ongoing threat tracking
2. **Customize Threat Types** - Focus on your specific risks
3. **Integrate with SIEM** - Use generated Sigma rules
4. **Regular Training Updates** - Keep model current with new threats

---

## 🚀 **Production Deployment**

### **Requirements**
- Python 3.12+
- Ollama with llama3 model
- 4GB+ RAM for model operations
- SQLite for memory database

### **Setup Steps**
1. **System Initialization:**
   ```bash
   python3 threatcrew/setup_memory_finetuning.py
   ```

2. **Health Verification:**
   ```bash
   python3 threatcrew/verify_system.py
   ```

3. **Test Execution:**
   ```bash
   python3 -m pytest test_threatcrew_all.py
   ```

4. **Production Launch:**
   ```bash
   streamlit run ui/threatagent_app.py --server.port 8502
   ```

### **Maintenance**
- **Weekly:** Run system health checks
- **Monthly:** Update training data
- **Quarterly:** Retrain models with new threat intelligence
- **As needed:** Add new threat types and targeting

---

## 📞 **Support & Resources**

### **Documentation**
- `SYSTEM_COMPLETION_SUMMARY.md` - Complete system overview
- `SCRIPT_COVERAGE_ANALYSIS.md` - Detailed test coverage
- `threatcrew/README.md` - Technical documentation

### **Validation**
- All 11 tests passing (100% success rate)
- 10/10 system health checks passing
- Complete script coverage analysis
- Production-ready validation

**🎉 ThreatAgent is ready for immediate use with comprehensive threat intelligence automation capabilities!**
