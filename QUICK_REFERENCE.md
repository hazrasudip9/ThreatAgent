# 🚀 ThreatAgent Quick Reference Card

## **30-Second Start**
```bash
cd /Users/noobita/Desktop/Github/ThreatAgent
python3 threatcrew/tests/verify_system.py        # Check health
streamlit run ui/threatagent_app.py --server.port 8502  # Start UI
# Open: http://localhost:8502
```

## **Web UI Modes**
| Mode | Purpose | Best For |
|------|---------|----------|
| 📊 **Dashboard** | System scripts & validation | First-time setup |
| 🎯 **Campaign** | Create threat intelligence campaigns | Daily operations |
| 🤖 **Console** | CLI commands in web | Power users |
| 🎓 **Training** | AI model management | Advanced users |
| 🔄 **Monitor** | Live system health | Operations teams |

## **CLI Quick Commands**
```bash
# Interactive mode (recommended)
python3 threatcrew/src/threatcrew/main.py interactive

# Direct workflows
python3 threatcrew/tests/simple_run.py           # Quick analysis
python3 threatcrew/tests/demo_complete_system.py # Full demo
python3 threatcrew/tests/verify_system.py        # Health check
```

## **Console Commands**
```
run      - Execute workflow
status   - System health  
train    - Model training
memory   - Database stats
create   - New campaign
list     - Show campaigns
quit     - Exit/clear
```

## **Campaign Creation (UI)**
1. **Campaign Mode** → **Create Campaign** tab
2. Fill: Company, Industry, Domains, Threat Types
3. Click **"🚀 Create & Execute Full Intelligence Workflow"**
4. Watch 8-step automation complete!

## **System Health Check**
```bash
python3 threatcrew/tests/verify_system.py
# Expected: "🚀 System Status: HEALTHY"
```

## **Test Everything**
```bash
python3 -m pytest test_threatcrew_all.py -v
# Expected: 11/11 tests passing
```

## **Troubleshooting**
- **UI won't start:** Try port 8503 instead of 8502
- **Health check fails:** Run `python3 threatcrew/tests/setup_memory_finetuning.py`
- **Ollama issues:** Ensure `ollama serve` is running
- **Tests fail:** Check `threatcrew/tests/verify_system.py` output

## **Production Ready Checklist**
- ✅ System health: 10/10 checks passing
- ✅ Test suite: 11/11 tests passing  
- ✅ Memory DB: Active with IOCs
- ✅ Custom model: Available
- ✅ UI accessible: http://localhost:8502

**🎯 Ready for immediate threat intelligence automation!**
