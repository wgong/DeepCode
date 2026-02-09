"""
Configuration loader with environment variable injection support.

This module provides utilities to load configuration files with automatic
environment variable injection for API keys and other sensitive values.
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


def inject_env_vars_to_mcp_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inject system environment variables into MCP server configurations.

    This ensures that API keys set as environment variables are passed to
    MCP servers even if not explicitly set in the config file.

    Args:
        config: Loaded configuration dictionary

    Returns:
        Modified configuration with environment variables injected
    """
    if "mcp" not in config or "servers" not in config["mcp"]:
        return config

    # Map of server names to environment variable names
    env_var_mappings = {
        "brave": {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")},
        "bocha-mcp": {"BOCHA_API_KEY": os.getenv("BOCHA_API_KEY", "")},
    }

    # Inject environment variables into server configs
    for server_name, env_vars in env_var_mappings.items():
        if server_name in config["mcp"]["servers"]:
            server_config = config["mcp"]["servers"][server_name]

            # Initialize env dict if it doesn't exist
            if "env" not in server_config:
                server_config["env"] = {}

            # Inject environment variables - system env takes precedence over config
            for env_key, env_value in env_vars.items():
                if env_value:  # Only inject if env var is actually set
                    server_config["env"][env_key] = env_value
                    print(f"✅ Injected {env_key} from environment variable for {server_name}")
                elif not server_config["env"].get(env_key):
                    # Keep the config value if system env is not set
                    # (it might already be set in the config file)
                    pass

    return config


def load_config_with_env_injection(config_path: str = "mcp_agent.config.yaml") -> Dict[str, Any]:
    """
    Load configuration file with automatic environment variable injection.

    Args:
        config_path: Path to the configuration YAML file

    Returns:
        Configuration dictionary with environment variables injected

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load base configuration
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Inject environment variables
    config = inject_env_vars_to_mcp_config(config)

    return config


def save_config(config: Dict[str, Any], config_path: str = "mcp_agent.config.yaml") -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Configuration dictionary to save
        config_path: Path to save the configuration
    """
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"✅ Configuration saved to {config_path}")


if __name__ == "__main__":
    # Test the configuration loader
    print("🔍 Testing configuration loader with environment variable injection...\n")

    try:
        config = load_config_with_env_injection()

        print("\n📋 MCP Server Environment Variables:")
        for server_name, server_config in config.get("mcp", {}).get("servers", {}).items():
            if "env" in server_config:
                print(f"\n  {server_name}:")
                for env_key, env_value in server_config["env"].items():
                    masked_value = f"{env_value[:10]}..." if env_value and len(env_value) > 10 else "(empty)"
                    print(f"    {env_key}: {masked_value}")

        print("\n✅ Configuration loaded successfully!")

    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
