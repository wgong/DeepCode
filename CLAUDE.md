# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepCode is a multi-agent AI research automation platform that transforms research papers, natural language, and URLs into production-ready code. The system uses a sophisticated agent orchestration engine with MCP (Model Context Protocol) integration to coordinate specialized agents for code generation.

**Core Capabilities:**
- **Paper2Code**: Automatically implement algorithms from research papers
- **Text2Web**: Generate full-stack web applications from natural language
- **Text2Backend**: Create backend services from text descriptions

## Essential Commands

### Running the Application

```bash
# Launch web interface (Streamlit) - runs on port 8503
streamlit run ui/streamlit_app.py
# Or using the entry point (recommended):
python deepcode.py  # Opens at http://localhost:8503

# Launch CLI interface
python cli/main_cli.py

# Using the installed package (requires: pip install deepcode-hku)
deepcode  # Command launches web interface on port 8503

# Show help and list available papers
python deepcode.py --help
```

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Using UV (recommended for development)
uv venv --python=3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Testing

```bash
# Test paper reproduction (two-phase workflow)
# Phase 1: Setup - prepares files in deepcode_lab/papers/
python deepcode.py test <paper_name>
python deepcode.py test <paper_name> --fast

# Phase 2: Full pipeline execution (after setup)
python -m workflows.paper_test_engine --paper <paper_name>
python -m workflows.paper_test_engine --paper <paper_name> --fast

# Example: Test RICE paper
python deepcode.py test rice
python -m workflows.paper_test_engine --paper rice
```

## Architecture Overview

### Multi-Agent System

DeepCode uses a hierarchical multi-agent architecture coordinated by the **Agent Orchestration Engine** (`workflows/agent_orchestration_engine.py`). The system workflow is:

1. **Input Processing** → Intent Understanding & Document Parsing
2. **Planning** → Code Architecture & Planning Agent generates implementation plan
3. **Knowledge Discovery** → Code Reference Mining & Repository Acquisition
4. **Indexing** → Codebase Intelligence builds knowledge graph
5. **Implementation** → Code Generation Agent synthesizes final code
6. **Execution** → Testing and validation

### Key Workflows

**Primary workflow classes:**
- `CodeImplementationWorkflow` (workflows/code_implementation_workflow.py) - Basic implementation pipeline
- `CodeImplementationWorkflowWithIndex` (workflows/code_implementation_workflow_index.py) - Enhanced with code indexing

**Specialized agents in `workflows/agents/`:**
- `RequirementAnalysisAgent` (`requirement_analysis_agent.py`) - Analyzes user requirements
- `CodeImplementationAgent` (`code_implementation_agent.py`) - Generates implementation code
- `ConciseMemoryAgent` (`memory_agent_concise.py`) - Manages context and memory efficiently
- `ConciseMemoryAgentMulti` (`memory_agent_concise_multi.py`) - Multi-context memory management
- `ConciseMemoryAgentIndex` (`memory_agent_concise_index.py`) - Index-aware memory management
- `DocumentSegmentationAgent` (`document_segmentation_agent.py`) - Handles large documents exceeding token limits

### MCP (Model Context Protocol) Integration

DeepCode leverages MCP for tool integration. Configuration is in `mcp_agent.config.yaml`:

**MCP Servers (located in `tools/`):**
- `code_implementation_server.py` - File operations, code execution, workspace management
- `code_reference_indexer.py` - Intelligent code search from indexed repositories
- `document_segmentation_server.py` - Smart document analysis for large papers
- `bocha_search_server.py` - Alternative web search server
- `git_command.py` - GitHub repository operations
- `pdf_downloader.py` - Document download and conversion
- `command_executor.py` - Shell command execution

**External MCP Servers:**
- `brave` - Web search via Brave API
- `filesystem` - Local file operations
- `fetch` - Web content retrieval

### Configuration Files

- `mcp_agent.config.yaml` - Main configuration (LLM provider, MCP servers, logging)
- `mcp_agent.secrets.yaml` - API keys and sensitive credentials
- `tools/indexer_config.yaml` - Code indexer configuration

### LLM Provider Selection

The system supports multiple LLM providers (configured in `mcp_agent.config.yaml`):
- `llm_provider: "google"` - Use Google Gemini models (default: gemini-3-pro-preview)
- `llm_provider: "anthropic"` - Use Anthropic Claude models (default: claude-sonnet-4.5)
- `llm_provider: "openai"` - Use OpenAI or compatible API endpoints (supports custom base URLs)
- `llm_provider: "openrouter"` - **NEW**: Use OpenRouter.ai as unified LLM provider (access to 200+ models)
- `llm_provider: "bedrock"` - **NEW**: Use AWS Bedrock for enterprise deployments

**Model Configuration Details** (in `mcp_agent.config.yaml`):
```yaml
llm_provider: "google"  # Set to "google", "anthropic", or "openai"

# OpenAI configuration (also supports OpenAI-compatible APIs)
openai:
  default_model: anthropic/claude-sonnet-4.5  # Or google/gemini-2.5-pro, etc.
  base_max_tokens: 40000
  max_tokens_policy: adaptive  # Automatically adjusts based on content
  reasoning_effort: low  # For thinking/reasoning models
  retry_max_tokens: 32768

# Google configuration
google:
  default_model: "gemini-3-pro-preview"

# Anthropic configuration
anthropic:
  default_model: "claude-sonnet-4.5"

# OpenRouter configuration (unified LLM provider)
openrouter:
  base_max_tokens: 40000
  default_model: "anthropic/claude-sonnet-4"  # Or any OpenRouter model
  max_tokens_policy: adaptive
  site_url: ""  # Optional: for OpenRouter rankings
  app_name: "DeepCode"

# AWS Bedrock configuration
bedrock:
  base_max_tokens: 40000
  default_model: "anthropic.claude-3-5-sonnet-20241022-v2:0"
  max_tokens_policy: adaptive
```

**OpenRouter Models Examples**:
- `anthropic/claude-sonnet-4`
- `google/gemini-2.0-flash-thinking-exp:free`
- `openai/gpt-4o`
- `deepseek/deepseek-chat`
- See full list: https://openrouter.ai/models

**AWS Bedrock Models Examples**:
- `anthropic.claude-3-5-sonnet-20241022-v2:0`
- `anthropic.claude-3-opus-20240229-v1:0`
- `meta.llama3-2-90b-instruct-v1:0`

The system uses adaptive token management and automatic fallback to available providers if the primary provider is unavailable.

## Codebase Structure

```
DeepCode/
├── cli/                      # CLI interface and workflow adapters
├── config/                   # MCP tool definitions
├── prompts/                  # System prompts for agents (code_prompts.py)
├── schema/                   # Configuration schemas
├── tools/                    # MCP server implementations
├── ui/                       # Streamlit web interface
│   ├── streamlit_app.py     # Main UI entry point
│   ├── app.py, handlers.py  # UI logic and handlers
│   └── components.py        # Reusable UI components
├── utils/                    # Shared utilities
│   ├── llm_utils.py         # LLM provider abstraction
│   ├── file_processor.py    # File handling
│   └── dialogue_logger.py   # Conversation logging
├── workflows/               # Core workflow orchestration
│   ├── agent_orchestration_engine.py  # Main orchestrator
│   ├── agents/              # Specialized agent implementations
│   └── code_implementation_workflow.py # Implementation pipeline
├── deepcode.py              # Main entry point
└── setup.py                 # Package setup
```

## Important Implementation Details

### Workflow Execution Pattern

The core workflow follows this pattern:

1. **Input Analysis** - `PAPER_INPUT_ANALYZER_PROMPT` identifies input type (text/file/url)
2. **Document Processing** - Files/URLs are downloaded and converted to markdown
3. **Document Segmentation** - Large documents are intelligently segmented (if enabled and threshold exceeded)
4. **Planning Phase** - Agent analyzes requirements and generates YAML implementation plan
5. **File Structure Generation** - Creates project scaffold with `STRUCTURE_GENERATOR_PROMPT`
6. **Code Implementation** - Iterative development using `CodeImplementationAgent`
7. **Memory Management** - `ConciseMemoryAgent` maintains context across long conversations

### Prompt Architecture

All prompts are centralized in `prompts/code_prompts.py`:
- `PAPER_INPUT_ANALYZER_PROMPT` - Input type classification
- `PAPER_DOWNLOADER_PROMPT` - Document download orchestration
- `PAPER_REFERENCE_ANALYZER_PROMPT` - Extract reference code repositories
- `CHAT_AGENT_PLANNING_PROMPT` - Generate implementation plans
- `STRUCTURE_GENERATOR_PROMPT` - Create file tree structure
- `GENERAL_CODE_IMPLEMENTATION_SYSTEM_PROMPT` - Code generation instructions

### Agent Communication

Agents communicate through:
- Structured JSON messages for data exchange
- YAML-formatted plans for implementation specs
- MCP protocol for tool calls
- Dialogue logging for conversation history (legacy, being phased out)

### Document Segmentation

When enabled (`document_segmentation.enabled: true` in config), documents exceeding `size_threshold_chars` are automatically segmented:
- Preserves semantic coherence (algorithms, concepts, formulas)
- Maintains section relationships
- Enables processing of papers that exceed token limits
- Falls back to traditional processing for smaller documents

## Development Considerations

### Adding New Agents

1. Create agent class in `workflows/agents/`
2. Inherit from appropriate base (e.g., `Agent` from mcp_agent)
3. Define agent prompts in `prompts/code_prompts.py`
4. Register in orchestration engine if needed

### Adding New MCP Tools

1. Create MCP server in `tools/` (see existing servers as templates)
2. Add server configuration to `mcp_agent.config.yaml` under `mcp.servers`
3. Update tool definitions in `config/mcp_tool_definitions.py` if needed

### Modifying Workflows

The main workflows are in `workflows/`. To modify:
- `agent_orchestration_engine.py` - Overall coordination logic
- `code_implementation_workflow.py` - Core implementation pipeline
- Agent-specific files in `workflows/agents/` - Individual agent behavior

### Working with Prompts

When modifying prompts in `prompts/code_prompts.py`:
- Maintain structured output format requirements (JSON/YAML)
- Preserve critical instruction sections
- Test with various input types
- Consider token limits for different LLM providers

### LLM Provider Utilities

`utils/llm_utils.py` provides abstraction layer:
- `get_preferred_llm_class()` - Get configured LLM client
- `get_default_models()` - Retrieve model configurations
- `should_use_document_segmentation()` - Document processing decision
- `get_adaptive_agent_config()` - Dynamic configuration based on content
- `get_token_limits()` - Provider-specific token constraints

## Entry Points

- **Web UI**: `deepcode.py` → launches `ui/streamlit_app.py` on port 8503 (http://localhost:8503)
- **CLI**: `cli/main_cli.py` → interactive terminal interface
- **Package**: Install via `pip install deepcode-hku`, then run command `deepcode`

**Note**: The package name is `deepcode-hku` but the command is simply `deepcode`.

## Windows-Specific Notes

Windows users need to manually configure MCP server paths in `mcp_agent.config.yaml`:
1. Install MCP servers globally: `npm i -g @modelcontextprotocol/server-brave-search @modelcontextprotocol/server-filesystem`
2. Find global node_modules: `npm -g root`
3. Update config with absolute paths to `.js` files using `node` command instead of `npx`

## API Keys and Secrets

Configure in `mcp_agent.secrets.yaml`:
- **OpenAI**: `api_key`, `base_url` (for OpenAI or compatible endpoints)
- **Anthropic**: `api_key`
- **Google**: `api_key`
- **OpenRouter**: `api_key` (get from https://openrouter.ai/keys), `base_url` (pre-configured)
- **AWS Bedrock**: `aws_access_key_id`, `aws_secret_access_key`, `aws_region`
- **Search APIs**: `BRAVE_API_KEY` or `BOCHA_API_KEY` in mcp_agent.config.yaml

## Common Development Workflows

### Testing Paper Reproduction

```bash
# 1. Prepare paper files in papers/<paper_name>/
# 2. Run test
python deepcode.py test <paper_name>

# Fast mode (skips some validation)
python deepcode.py test <paper_name> --fast
```

### Debugging Agent Behavior

Check logs in `logs/` directory (configured in `mcp_agent.config.yaml`):
- Log pattern: `logs/mcp-agent-{unique_id}.jsonl`
- Contains full conversation history and tool calls

### Modifying UI

Edit files in `ui/`:
- `streamlit_app.py` - Main application layout
- `handlers.py` - Event handlers and workflow triggers
- `components.py` - Reusable UI components
- `styles.py` - CSS styling

The UI uses Streamlit's session state for managing workflow state and conversation history.
