# DeepCode Quick Start Guide

## 🚀 Essential Commands

### 1. Launch Web Interface (Main)
```bash
python deepcode.py
# Opens at http://localhost:8503
```

### 2. Launch CLI Interface
```bash
python cli/main_cli.py
```

### 3. View Logs (NEW!)
```bash
python view_logs.py
# Opens log viewer at http://localhost:8501
```

## 📁 Project Folder Structure (NEW Format!)

All new projects now use **human-readable timestamps** for easy identification:

```
deepcode_lab/papers/
├── paper_20260208_210000/          # Research paper project
│   ├── paper_20260208_210000.md    # Paper content
│   ├── initial_plan.txt            # Implementation plan
│   ├── generate_code/              # Generated code
│   └── code_implementation_report.txt
├── chat_project_20260208_214743/   # Chat-based project
│   ├── chat_project_20260208_214743.md
│   ├── initial_plan.txt
│   └── generate_code/
└── ...
```

**Format**: `YYYYMMDD_HHMMSS`
- Example: `20260208_214743` = February 8, 2026 at 21:47:43

## 📋 Log Files

Logs are saved in matching format for easy correlation:

```
logs/
├── mcp-agent-20260208_214743.jsonl
├── mcp-agent-20260208_215530.jsonl
└── ...
```

**Pro Tip**: The timestamps match!
- Project: `chat_project_20260208_214743/`
- Log file: `mcp-agent-20260208_214743.jsonl`

## 🔍 Using the Log Viewer

### Launch
```bash
python view_logs.py
```

### Key Features
1. **Select Log File** - Choose from dropdown (newest first)
2. **Filter by Level** - INFO, ERROR, WARNING, DEBUG
3. **Search** - Find text in messages and data
4. **Display Modes**:
   - Formatted View (pretty, color-coded)
   - Table View (spreadsheet-like)
   - Raw JSON (complete details)
5. **Export** - Download as JSON or CSV

### Useful Searches

**Find planning phase**:
```
Search: "ChatPlanningAgent"
```

**Find file creation**:
```
Search: "StructureGeneratorAgent"
```

**Find errors**:
```
Filter Level: ERROR
```

**Track code generation**:
```
Search: "CodeImplementationAgent"
```

## 📊 Understanding Project Flow

### For Chat Input (e.g., "Generate fibonacci sequence")

1. **Chat Planning** → Generates YAML plan
2. **Creates Project Folder** → `chat_project_20260208_HHMMSS/`
3. **Generates Code** → In `generate_code/` subfolder
4. **Saves Report** → `code_implementation_report.txt`

### For Research Paper Input

1. **Paper Analysis** → Downloads and converts to markdown
2. **Creates Project Folder** → `paper_20260208_HHMMSS/`
3. **Reference Discovery** → Finds related GitHub repos (optional)
4. **Code Planning** → Generates implementation plan
5. **Generates Code** → Full implementation with tests

## 🎯 Example: Your Fibonacci Project

**Location**: `deepcode_lab/papers/chat_project_20260208_214743/generate_code/fibonacci-cli/`

```bash
cd deepcode_lab/papers/chat_project_20260208_214743/generate_code/fibonacci-cli

# Run the CLI
python fibonacci_cli.py --max-number 100

# Different formats
python fibonacci_cli.py --max-number 50 --format inline
python fibonacci_cli.py --max-number 20 --format json --count

# Run tests
pytest tests/test_fibonacci.py -v
```

## 📖 Documentation

- **README_view_logs.md** - Complete log viewer guide
- **CLAUDE.md** - Project overview and architecture
- **CHANGELOG_timestamp_fix.md** - Details on timestamp changes
- **README.md** - Main project documentation

## 🔧 Configuration

**Main Config**: `mcp_agent.config.yaml`
```yaml
llm_provider: anthropic          # or "google", "openai", "openrouter"
anthropic:
  default_model: claude-sonnet-4-5-20250929  # ✅ Fixed model name

logger:
  path_settings:
    path_pattern: logs/mcp-agent-{unique_id}.jsonl
    timestamp_format: '%Y%m%d_%H%M%S'
```

**Secrets**: `mcp_agent.secrets.yaml` (not in git)
```yaml
anthropic:
  api_key: "your-key-here"
google:
  api_key: "your-key-here"
```

## ⚡ Quick Troubleshooting

### Issue: "Model not found" error
**Fix**: Check `mcp_agent.config.yaml` - use correct model name
```yaml
anthropic:
  default_model: claude-sonnet-4-5-20250929  # Not claude-sonnet-4.5
```

### Issue: Can't find generated code
**Check**: Look for newest timestamp folder
```bash
ls -lt deepcode_lab/papers/
# Or search by pattern
find deepcode_lab/papers -name "*20260208*"
```

### Issue: Want to see what happened
**Use**: Log viewer
```bash
python view_logs.py
# Select the matching log file
```

## 🎨 Tips & Tricks

1. **Correlate Projects & Logs**: Timestamps match!
   - Project: `chat_project_20260208_214743/`
   - Log: `mcp-agent-20260208_214743.jsonl`

2. **Find Recent Work**:
   ```bash
   ls -lt deepcode_lab/papers/ | head -5
   ```

3. **Search All Projects**:
   ```bash
   grep -r "fibonacci" deepcode_lab/papers/
   ```

4. **Compare Implementations**:
   - Create same spec twice
   - Compare results in different timestamp folders

## 💡 Learning DeepCode

**Best Approach**:
1. Run a simple task (fibonacci, hello world)
2. Open log viewer: `python view_logs.py`
3. Load the matching log file
4. Search for agent names to trace workflow
5. Review generated code in project folder
6. Read `CLAUDE.md` for architecture details

**Agent Flow**:
```
Input → ChatPlanningAgent → StructureGeneratorAgent →
CodeImplementationAgent → Generated Code
```

Track this flow in the log viewer! 🎯

---

**Get Help**: `python deepcode.py --help`

**Report Issues**: https://github.com/anthropics/deepcode-hku/issues

**Happy Coding!** 🚀
