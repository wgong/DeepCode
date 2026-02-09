#!/usr/bin/env python3
"""
DeepCode Log Viewer Launcher

Quick launcher for the Streamlit-based log viewer.
Run this script to analyze DeepCode execution logs.

Usage:
    python view_logs.py
    # Or make it executable:
    chmod +x view_logs.py
    ./view_logs.py
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch the log viewer"""
    viewer_path = Path(__file__).parent / "utils" / "log_viewer.py"

    if not viewer_path.exists():
        print(f"❌ Error: Log viewer not found at {viewer_path}")
        sys.exit(1)

    print("🚀 Launching DeepCode Log Viewer...")
    print("📋 Opening at http://localhost:8501")
    print("💡 Press Ctrl+C to stop the viewer\n")

    try:
        subprocess.run([
            sys.executable,
            "-m", "streamlit",
            "run",
            str(viewer_path),
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Log viewer stopped")
    except Exception as e:
        print(f"❌ Error launching viewer: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
