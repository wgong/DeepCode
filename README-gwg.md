```bash
conda create -n deepcode python=3.11
conda activate deepcode

pip install -e .

git rm --cached mcp_agent.config.yaml mcp_agent.secrets.yaml
```