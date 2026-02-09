# Environment Variable Configuration Guide

DeepCode now supports loading API keys and configuration from environment variables, providing a more secure and flexible way to manage credentials.

## Supported Environment Variables

### LLM Provider API Keys

DeepCode automatically detects and uses API keys from environment variables, with the following priority:

**Priority:** Environment Variable → Config File (`mcp_agent.secrets.yaml`)

| Environment Variable | Provider | Used For |
|---------------------|----------|----------|
| `OPENROUTER_API_KEY` | OpenRouter | Access to 200+ models via OpenRouter.ai |
| `ANTHROPIC_API_KEY` | Anthropic | Claude models directly |
| `GOOGLE_API_KEY` | Google | Gemini models |
| `OPENAI_API_KEY` | OpenAI | OpenAI models and compatible endpoints |
| `AWS_ACCESS_KEY_ID`<br>`AWS_SECRET_ACCESS_KEY` | AWS Bedrock | Claude/LLaMA models via AWS Bedrock |

### MCP Server API Keys

For Model Context Protocol (MCP) servers that provide web search and other services:

| Environment Variable | Service | Used For |
|---------------------|---------|----------|
| `BRAVE_API_KEY` | Brave Search | Web search via Brave API |
| `BOCHA_API_KEY` | Bocha Search | Chinese AI search engine |

## Setup Instructions

### Option 1: Environment Variables (Recommended)

Set environment variables in your shell:

```bash
# Linux/macOS
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
export BRAVE_API_KEY='your-brave-key'

# Make permanent by adding to ~/.bashrc or ~/.zshrc
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
```

```powershell
# Windows PowerShell
$env:OPENROUTER_API_KEY='sk-or-v1-your-key-here'
$env:BRAVE_API_KEY='your-brave-key'

# Make permanent (System-wide)
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-...', 'User')
```

### Option 2: .env File

Create a `.env` file in the project root:

```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
BRAVE_API_KEY=your-brave-key
ANTHROPIC_API_KEY=sk-ant-your-key
GOOGLE_API_KEY=your-google-key
```

**Important:** Add `.env` to your `.gitignore` to avoid committing secrets!

### Option 3: Configuration Files (Legacy)

Edit `mcp_agent.secrets.yaml`:

```yaml
openrouter:
  api_key: "sk-or-v1-your-key-here"
  base_url: "https://openrouter.ai/api/v1"
```

## How It Works

### LLM Provider API Keys

The `utils/llm_utils.py` module checks for API keys in this order:

1. **Environment variable** (e.g., `OPENROUTER_API_KEY`)
2. **Config file** (`mcp_agent.secrets.yaml`)
3. **Fallback** to next available provider

Code snippet from `llm_utils.py`:

```python
# Environment variables take precedence
openrouter_key = os.getenv("OPENROUTER_API_KEY") or secrets.get("openrouter", {}).get("api_key", "")
```

### MCP Server API Keys

MCP servers are launched as subprocesses that inherit the parent process environment. The workflow classes (`CodeImplementationWorkflow`, `CodeImplementationWorkflowWithIndex`) automatically:

1. Check for environment variables
2. Propagate them to MCP server subprocesses
3. Fall back to config file values if env vars not set

This happens in the `_prepare_mcp_environment()` method:

```python
def _prepare_mcp_environment(self) -> None:
    """Ensure API keys are propagated to MCP server subprocesses"""
    env_vars_to_check = {
        'BRAVE_API_KEY': 'Brave Search',
        'BOCHA_API_KEY': 'Bocha Search',
    }
    # Sets os.environ so subprocesses inherit these values
```

## Verification

Check which API keys are detected:

```bash
python3 << 'EOF'
import os
print("Detected API Keys:")
print(f"  OPENROUTER_API_KEY: {'✓' if os.getenv('OPENROUTER_API_KEY') else '✗'}")
print(f"  BRAVE_API_KEY: {'✓' if os.getenv('BRAVE_API_KEY') else '✗'}")
print(f"  ANTHROPIC_API_KEY: {'✓' if os.getenv('ANTHROPIC_API_KEY') else '✗'}")
EOF
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for production deployments
3. **Add `.env` to `.gitignore`**
4. **Rotate keys regularly** if exposed
5. **Use different keys** for development and production

## Getting API Keys

### OpenRouter (Recommended for Multi-Model Access)

1. Visit https://openrouter.ai/keys
2. Sign up/login
3. Create a new API key
4. Set `export OPENROUTER_API_KEY='sk-or-v1-...'`

**Benefits:**
- Single key for 200+ models
- Access Claude, GPT-4, Gemini, DeepSeek, and more
- Pay-as-you-go pricing
- No vendor lock-in

### Brave Search

1. Visit https://brave.com/search/api/
2. Sign up for API access
3. Get your API key
4. Set `export BRAVE_API_KEY='...'`

### Other Providers

- **Anthropic:** https://console.anthropic.com/
- **Google AI Studio:** https://makersuite.google.com/app/apikey
- **OpenAI:** https://platform.openai.com/api-keys

## Troubleshooting

### Environment variable not detected

```bash
# Check if variable is set
echo $OPENROUTER_API_KEY

# Set it in current session
export OPENROUTER_API_KEY='your-key'

# Verify DeepCode can see it
python3 -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"
```

### MCP servers not using environment variables

The environment preparation happens during workflow initialization. Make sure:

1. Environment variable is set **before** running DeepCode
2. Variable name matches exactly (case-sensitive)
3. Check logs for any warnings about API key loading

### Mixed configuration (env + config file)

This is supported! Environment variables take precedence:

- LLM keys: `$OPENROUTER_API_KEY` overrides `mcp_agent.secrets.yaml`
- MCP keys: `$BRAVE_API_KEY` supplements config file values

## Migration from Config Files

To migrate from config files to environment variables:

```bash
# 1. Extract your existing keys
grep "api_key:" mcp_agent.secrets.yaml

# 2. Set them as environment variables
export OPENROUTER_API_KEY='your-key-from-yaml'

# 3. (Optional) Clear config file
# You can keep empty strings in the config - env vars take precedence
```

## Summary

**Before (Config File Only):**
```yaml
# mcp_agent.secrets.yaml
openrouter:
  api_key: "sk-or-v1-abc123..."  # Committed to git by accident!
```

**After (Environment Variables):**
```bash
export OPENROUTER_API_KEY='sk-or-v1-abc123...'
# More secure, no risk of committing secrets
```

**Best Practice:**
```bash
# Set env vars
export OPENROUTER_API_KEY='...'

# Config file stays empty (safe to commit)
# openrouter:
#   api_key: ""  # Loaded from $OPENROUTER_API_KEY
```

---

**Modified Files:**
- `utils/llm_utils.py` - LLM provider key detection
- `workflows/code_implementation_workflow.py` - MCP environment preparation
- `workflows/code_implementation_workflow_index.py` - MCP environment preparation
- `utils/config_loader.py` - Configuration loading utilities
