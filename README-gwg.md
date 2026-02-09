# DeepCode Setup Guide

## Prerequisites

Activate your conda environment:

```bash
conda create -n deepcode python=3.11
conda activate deepcode

pip install -e .

git rm --cached mcp_agent.config.yaml mcp_agent.secrets.yaml
```


## Setup

### 1. Install DeepCode

```bash
pip install deepcode-hku

# OR install from source for development
pip install -r requirements.txt
```

### 2. Get API Keys

#### OpenRouter API Key (Required for LLM access)

1. Visit https://openrouter.ai/keys
2. Sign up or log in
3. Click "Create Key"
4. Copy your API key (starts with `sk-or-v1-...`)
5. Set environment variable:

```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# Make it permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Why OpenRouter?** Single API key gives you access to 200+ models:
- Anthropic Claude (claude-sonnet-4)
- Google Gemini (gemini-2.0-flash-thinking-exp)
- OpenAI GPT-4 (gpt-4o)
- DeepSeek (deepseek-chat)
- Meta LLaMA and many more

See all models: https://openrouter.ai/models

#### Brave Search API Key (Optional, for web search)

1. Visit https://brave.com/search/api/
2. Sign up for Brave Search API
3. Choose a plan:
   - **Free tier**: 2,000 queries/month
   - **Paid plans**: Higher limits
4. Get your API key from the dashboard
5. Set environment variable:

```bash
export BRAVE_API_KEY='your-brave-api-key'

# Make it permanent
echo 'export BRAVE_API_KEY="your-brave-api-key"' >> ~/.bashrc
source ~/.bashrc
```

**Note:** Brave Search is used by DeepCode's MCP servers for web searches during research and code reference discovery.

#### Bocha Search API Key (Optional, for Chinese content)

If you need Chinese language search capabilities:

1. Visit Bocha Search API website
2. Sign up and get your API key
3. Set environment variable:

```bash
export BOCHA_API_KEY='your-bocha-api-key'
echo 'export BOCHA_API_KEY="your-bocha-api-key"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Configure DeepCode

The configuration files are:
- `mcp_agent.config.yaml` - Main configuration (LLM provider, models, servers)
- `mcp_agent.secrets.yaml` - API keys (optional if using env vars)

**Current setup uses environment variables**, so you don't need to edit `mcp_agent.secrets.yaml`.

To change the LLM model, edit `mcp_agent.config.yaml`:

```yaml
# Line 106
llm_provider: "openrouter"  # Current setting

# Line 134 - Change model here
openrouter:
  default_model: "anthropic/claude-sonnet-4"  # Default
  # Other options:
  # default_model: "google/gemini-2.0-flash-thinking-exp:free"
  # default_model: "deepseek/deepseek-chat"
  # default_model: "openai/gpt-4o"
```

### 4. Verify Setup

Check that your environment variables are set:

```bash
# Check API keys
echo "OPENROUTER_API_KEY: ${OPENROUTER_API_KEY:+✓ Set}"
echo "BRAVE_API_KEY: ${BRAVE_API_KEY:+✓ Set}"

# Or run the verification script
python3 << 'EOF'
import os
print("Environment Variables:")
print(f"  OPENROUTER_API_KEY: {'✓' if os.getenv('OPENROUTER_API_KEY') else '✗'}")
print(f"  BRAVE_API_KEY: {'✓' if os.getenv('BRAVE_API_KEY') else '✗ (optional)'}")
print(f"  BOCHA_API_KEY: {'✓' if os.getenv('BOCHA_API_KEY') else '✗ (optional)'}")
EOF
```

### 5. Run DeepCode

```bash
# Launch web interface (opens at http://localhost:8503)
python deepcode.py

# OR use the CLI interface
python cli/main_cli.py

# OR if installed via pip
deepcode
```

## Quick Start Example

```bash
# 1. Set your API key
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# 2. Launch DeepCode
python deepcode.py

# 3. Open browser to http://localhost:8503
# 4. Try "Text2Web" or "Paper2Code" modes
```

## Troubleshooting

### "No API key configured" error

Make sure `OPENROUTER_API_KEY` is set:

```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY='sk-or-v1-...'

# Verify DeepCode can see it
python3 -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"
```

### Brave Search not working

If you get "BRAVE_API_KEY not configured" warnings:

1. Get a free key from https://brave.com/search/api/
2. Set `export BRAVE_API_KEY='your-key'`
3. Restart DeepCode

### Model not found

Check available models at https://openrouter.ai/models and update `mcp_agent.config.yaml` line 134.

## More Information

- **Full Documentation**: See `CLAUDE.md` for architecture details
- **Environment Variables Guide**: See `ENV_VARS.md`
- **Main README**: See `README.md`


## Evaluations

### smart note-taking

- use claude code to write a user-guide on ~/projects/digital-duck/st_note/README-notetaking.md
- convert it to .pdf: 
  - (1) preview .md (2) open in browser (3) save as .pdf
  - `pandoc README-notetaking.md -o smart_note.pdf --pdf-engine=xelatex -V mainfont="DejaVu Sans"`
- ask DeepCode to build an app out of it
