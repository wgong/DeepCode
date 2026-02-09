# DeepCode Log Viewer Guide

## 📋 Overview

The DeepCode Log Viewer is a powerful Streamlit-based tool for analyzing and understanding DeepCode's execution flow through comprehensive log analysis. This tool is essential for developers who want to learn how DeepCode works by reviewing logs and call stack traces.

## 🚀 Quick Start

### Launch the Log Viewer

**Option 1: Quick Launch (Recommended)**
```bash
python view_logs.py
```

**Option 2: Direct Launch**
```bash
streamlit run utils/log_viewer.py --server.port=8501
```

The viewer will open at **http://localhost:8501**

## ✨ Features

### 1. **Statistics Dashboard**
- Total log entries count
- Error and warning counts with delta indicators
- Entries with structured data
- Execution duration analysis
- Log level distribution charts
- Top agent activity ranking

### 2. **Search & Filter Capabilities**
- **Log Level Filter**: Filter by INFO, ERROR, WARNING, DEBUG
- **Namespace Filter**: Search by component/module (e.g., `mcp_agent`, `orchestration`)
- **Full-Text Search**: Search across message content and JSON data fields
- **Real-time Filtering**: Instant results as you type

### 3. **Three Display Modes**

#### Formatted View (Default)
- Color-coded log levels (ERROR=red, WARNING=orange, INFO=blue, DEBUG=gray)
- Timestamp and line number display
- Namespace highlighting
- Expandable JSON data sections with syntax highlighting
- Search term highlighting

#### Table View
- Spreadsheet-like view of logs
- Sortable columns
- Compact display for quick scanning
- Includes: timestamp, level, namespace, message

#### Raw JSON View
- Complete log entry details
- Expandable/collapsible sections
- Full metadata and nested data structures
- Copy-paste friendly format

### 4. **Export Functionality**
- **JSON Export**: Download filtered logs in JSON format
- **CSV Export**: Export to CSV for spreadsheet analysis
- Timestamped filenames for easy organization

### 5. **Advanced Features**
- Pagination controls (10-1000 entries)
- Line number tracking
- File size and modification time display
- Session state management
- Automatic log parsing with error recovery

## 📊 Log File Format

DeepCode logs are stored in JSONL (JSON Lines) format in the `logs/` directory.

**Filename Pattern**: `logs/mcp-agent-YYYYMMDD_HHMMSS.jsonl`

**Example**: `logs/mcp-agent-20260208_214743.jsonl`

### Log Entry Structure

```json
{
  "level": "INFO",
  "timestamp": "2026-02-08T21:47:43.325896",
  "namespace": "mcp_agent.cli_agent_orchestration",
  "message": "Loading subagents from configuration...",
  "data": {
    "progress_action": "Running",
    "target": "cli_agent_orchestration",
    "agent_name": "mcp_application_loop",
    "session_id": "83fcfbb0-6d79-4931-98b9-e389f4ed9651"
  }
}
```

**Fields:**
- `level`: Log severity (INFO, ERROR, WARNING, DEBUG)
- `timestamp`: ISO 8601 formatted timestamp
- `namespace`: Component/module that generated the log
- `message`: Human-readable log message
- `data`: (Optional) Structured additional information

## 🔍 Understanding DeepCode Through Logs

### Key Namespaces to Watch

1. **`mcp_agent.cli_agent_orchestration`**
   - Main orchestration engine
   - Agent coordination and workflow management

2. **`mcp_agent.workflows.llm.augmented_llm_*`**
   - LLM request/response handling
   - Different agents (ChatPlanningAgent, StructureGeneratorAgent, etc.)

3. **`mcp_agent.mcp.mcp_connection_manager`**
   - MCP server lifecycle (startup, shutdown)
   - Tool availability and connections

4. **`mcp_agent.mcp.mcp_aggregator.*`**
   - Tool call requests and responses
   - Agent-specific tool usage

5. **`mcp_agent.executor.executor`**
   - Task execution flow
   - Error handling and exceptions

### Common Search Queries

**Planning Phase:**
```
Search: "ChatPlanningAgent"
```
- See how DeepCode analyzes requirements
- View the generated implementation plan

**File Structure Creation:**
```
Search: "StructureGeneratorAgent"
```
- Watch project scaffold generation
- See directory and file creation

**Code Generation:**
```
Search: "CodeImplementationAgent"
```
- Observe iterative code development
- Track which files are being written

**Error Debugging:**
```
Filter by Level: ERROR
```
- Identify failures and exceptions
- Analyze error messages and stack traces

**MCP Tool Usage:**
```
Search: "Requesting tool call"
```
- See which tools are being invoked
- Understand tool call patterns

**Agent Lifecycle:**
```
Search: "Up and running" OR "shutdown"
```
- Track MCP server connections
- Monitor agent initialization

## 🎯 Example Workflow Analysis

### Analyzing a Fibonacci Generation Run

1. **Load the Log File**
   - Select the most recent log file
   - Click "Load Log File"

2. **Check Statistics**
   - Total entries: ~500-1000 for simple projects
   - Agent activity: Look for ChatPlanningAgent, StructureGeneratorAgent, CodeImplementationAgent
   - Errors: Should be 0 for successful runs

3. **Review Planning Phase**
   - Search: "planning"
   - Look for YAML plan generation
   - Understand requirements analysis

4. **Track File Creation**
   - Search: "execute_commands"
   - Filter namespace: "StructureGeneratorAgent"
   - See mkdir, touch commands

5. **Follow Code Implementation**
   - Search: "write_file" or "edit_file"
   - See which files are being written
   - Track iteration count

6. **Identify Any Issues**
   - Filter level: ERROR or WARNING
   - Review error messages
   - Check stack traces in data field

## 📁 Generated Code Example

Here's what DeepCode generated for a simple Fibonacci specification:

### Project Structure
```
fibonacci-cli/
├── fibonacci.py              # Core implementation
├── fibonacci_cli.py          # CLI interface (Click framework)
├── utils.py                  # Helper utilities
├── tests/
│   ├── test_fibonacci.py     # 466 lines of comprehensive tests!
│   ├── test_cli.py          # CLI integration tests
│   └── __init__.py
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies
└── setup.py                  # Package setup
```

### Key Features Generated
- ✅ Core `generate_fibonacci(max_number)` function with O(n) complexity
- ✅ Additional utility functions: `fibonacci_count()`, `fibonacci_info()`
- ✅ Full-featured CLI with multiple output formats (list, inline, JSON)
- ✅ Comprehensive error handling and input validation
- ✅ 466 lines of unit tests with pytest
- ✅ Edge cases, performance tests, parameterized tests
- ✅ Professional documentation and type hints

### Testing the Generated Code
```bash
cd deepcode_lab/papers/chat_project_*/generate_code/fibonacci-cli

# Run the CLI
python fibonacci_cli.py --max-number 100

# Different formats
python fibonacci_cli.py --max-number 50 --format inline
python fibonacci_cli.py --max-number 20 --format json --count

# Run tests
pytest tests/test_fibonacci.py -v
```

## 🛠️ Technical Details

### Implementation
- **Framework**: Streamlit
- **Data Processing**: Pandas for log analysis
- **Port**: 8501 (default)
- **File Location**: `utils/log_viewer.py`
- **Launcher**: `view_logs.py`

### Dependencies
```python
streamlit
pandas
json (stdlib)
pathlib (stdlib)
datetime (stdlib)
re (stdlib)
```

### Custom Styling
- CSS-based log entry formatting
- Color-coded severity levels
- Monospace fonts for code/data
- Responsive layout
- Syntax highlighting for JSON

### Performance
- Handles logs with 10,000+ entries
- Pagination for large datasets
- Efficient filtering with pandas
- Session state caching

## 📚 Learning DeepCode Architecture

### Recommended Learning Path

**Step 1: Run a Simple Project**
```bash
python cli/main_cli.py
# Enter: "Generate a fibonacci sequence up to a given number"
```

**Step 2: Load Logs in Viewer**
```bash
python view_logs.py
```

**Step 3: Trace the Execution Flow**

1. **Input Analysis Phase**
   - Search: "PAPER_INPUT_ANALYZER"
   - See how DeepCode classifies your input (text/file/url)

2. **Planning Phase**
   - Search: "ChatPlanningAgent"
   - Review the YAML implementation plan
   - Understand requirements breakdown

3. **Structure Generation**
   - Search: "StructureGeneratorAgent"
   - Watch project structure creation
   - See file tree generation

4. **Code Implementation**
   - Search: "CodeImplementationAgent"
   - Follow iterative code development
   - Track file writes and edits

5. **Tool Usage**
   - Search: "tool_name"
   - See MCP tool invocations
   - Understand tool call patterns

**Step 4: Review Generated Code**
```bash
cd deepcode_lab/papers/chat_project_*/generate_code/
```

## 🎨 UI Components

### Sidebar
- Log file selector (sorted by date)
- File metadata (size, modification time)
- Load button

### Main Area
- Statistics dashboard with metrics
- Level distribution chart
- Agent activity ranking
- Filter controls (3-column layout)
- Display mode selector
- Log entries display
- Export buttons

### Color Scheme
- **ERROR**: Red (#f44336)
- **WARNING**: Orange (#ff9800)
- **INFO**: Blue (#2196F3)
- **DEBUG**: Gray (#9E9E9E)
- **Highlight**: Yellow (search matches)
- **Data**: Dark theme (#263238) with green text (#aed581)

## 💡 Pro Tips

### Debugging Failed Runs
1. Filter by ERROR level first
2. Check the namespace to identify which agent failed
3. Review the data field for detailed error info
4. Search for the error message in the codebase

### Understanding Agent Communication
1. Search for specific agent names (e.g., "ChatPlanningAgent")
2. Look for "Requesting tool call" entries
3. Check tool responses in subsequent log entries
4. Track session IDs for conversation threads

### Performance Analysis
1. Sort by timestamp to see execution timeline
2. Look for time gaps between log entries
3. Search for "progress_action" to track workflow stages
4. Use the duration metric in statistics

### Extracting Implementation Patterns
1. Search for "write_file" or "edit_file" tool calls
2. Review the data field to see file contents
3. Compare multiple runs to identify patterns
4. Export filtered logs for offline analysis

## 🔗 Related Documentation

- **CLAUDE.md**: Project overview and development guidelines
- **README.md**: Main DeepCode documentation
- **mcp_agent.config.yaml**: Configuration reference
- **prompts/code_prompts.py**: System prompts and instructions

## 📞 Support

For issues or questions:
- Check the logs for error messages first
- Review CLAUDE.md for architecture details
- Examine generated code in `deepcode_lab/papers/`
- Report issues at: https://github.com/anthropics/deepcode-hku/issues

## 🎉 Conclusion

The Log Viewer is your window into DeepCode's "thinking process." Use it to:
- 🧠 Understand the multi-agent architecture
- 🐛 Debug issues and failures
- 📖 Learn by example from successful runs
- 🔧 Optimize your prompts and configurations
- 🚀 Build confidence in DeepCode's capabilities

Happy exploring! 🚀
