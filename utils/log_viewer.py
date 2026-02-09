"""
DeepCode Log Viewer - A Streamlit app for viewing and analyzing JSONL logs

This tool helps developers understand DeepCode's execution flow by providing:
- Interactive log browsing with syntax highlighting
- Search and filter capabilities
- Timeline visualization
- Call stack and agent flow analysis
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import re
from typing import List, Dict, Any, Optional
from collections import defaultdict

# Page configuration
st.set_page_config(
    page_title="DeepCode Log Viewer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .log-entry {
        border-left: 4px solid #4CAF50;
        padding: 10px;
        margin: 10px 0;
        background-color: #f5f5f5;
        border-radius: 4px;
    }
    .log-entry.ERROR {
        border-left-color: #f44336;
    }
    .log-entry.WARNING {
        border-left-color: #ff9800;
    }
    .log-entry.INFO {
        border-left-color: #2196F3;
    }
    .log-entry.DEBUG {
        border-left-color: #9E9E9E;
    }
    .timestamp {
        color: #666;
        font-size: 0.85em;
        font-family: monospace;
    }
    .namespace {
        color: #1976D2;
        font-weight: bold;
        font-size: 0.9em;
    }
    .message {
        margin-top: 5px;
        font-size: 1em;
    }
    .data-section {
        background-color: #263238;
        color: #aed581;
        padding: 10px;
        border-radius: 4px;
        margin-top: 5px;
        font-family: monospace;
        font-size: 0.85em;
        overflow-x: auto;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        text-align: center;
    }
    .search-highlight {
        background-color: yellow;
        padding: 2px 4px;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)


class LogViewer:
    """Main log viewer class"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.logs: List[Dict[str, Any]] = []
        self.df: Optional[pd.DataFrame] = None

    def get_log_files(self) -> List[Path]:
        """Get all JSONL log files sorted by modification time (newest first)"""
        if not self.log_dir.exists():
            return []
        return sorted(
            self.log_dir.glob("*.jsonl"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

    def load_log_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load and parse a JSONL log file"""
        logs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        log_entry = json.loads(line)
                        log_entry['_line_number'] = line_num
                        logs.append(log_entry)
                    except json.JSONDecodeError as e:
                        st.warning(f"⚠️ Skipped malformed JSON at line {line_num}: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error reading log file: {str(e)}")
        return logs

    def parse_logs_to_dataframe(self) -> pd.DataFrame:
        """Convert logs to pandas DataFrame for analysis"""
        if not self.logs:
            return pd.DataFrame()

        df_data = []
        for log in self.logs:
            row = {
                'timestamp': log.get('timestamp', ''),
                'level': log.get('level', 'UNKNOWN'),
                'namespace': log.get('namespace', ''),
                'message': log.get('message', ''),
                'has_data': 'data' in log,
                '_line_number': log.get('_line_number', 0),
                '_raw': log
            }
            df_data.append(row)

        df = pd.DataFrame(df_data)
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        return df

    def filter_logs(
        self,
        level_filter: List[str],
        namespace_filter: str,
        search_query: str,
        time_range: Optional[tuple] = None
    ) -> pd.DataFrame:
        """Apply filters to the logs DataFrame"""
        df = self.df.copy()

        if df.empty:
            return df

        # Level filter
        if level_filter:
            df = df[df['level'].isin(level_filter)]

        # Namespace filter
        if namespace_filter:
            df = df[df['namespace'].str.contains(namespace_filter, case=False, na=False)]

        # Search query (searches in message and data)
        if search_query:
            mask = df['message'].str.contains(search_query, case=False, na=False)
            # Also search in data fields
            for idx, row in df.iterrows():
                if not mask.loc[idx]:
                    raw_log = row['_raw']
                    if 'data' in raw_log:
                        data_str = json.dumps(raw_log['data'])
                        if search_query.lower() in data_str.lower():
                            mask.loc[idx] = True
            df = df[mask]

        # Time range filter
        if time_range and 'timestamp' in df.columns:
            start_time, end_time = time_range
            df = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

        return df

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from logs"""
        if self.df.empty:
            return {}

        stats = {
            'total_entries': len(self.df),
            'level_counts': self.df['level'].value_counts().to_dict(),
            'namespace_counts': self.df['namespace'].value_counts().head(10).to_dict(),
            'time_range': (
                self.df['timestamp'].min() if 'timestamp' in self.df.columns else None,
                self.df['timestamp'].max() if 'timestamp' in self.df.columns else None
            ),
            'entries_with_data': self.df['has_data'].sum()
        }

        # Agent activity analysis
        agent_namespaces = self.df[self.df['namespace'].str.contains('Agent', na=False)]
        stats['agent_activity'] = agent_namespaces['namespace'].value_counts().head(10).to_dict()

        return stats

    def render_log_entry(self, log: Dict[str, Any], search_query: str = ""):
        """Render a single log entry with nice formatting"""
        level = log.get('level', 'UNKNOWN')
        timestamp = log.get('timestamp', '')
        namespace = log.get('namespace', '')
        message = log.get('message', '')
        line_num = log.get('_line_number', '')

        # Highlight search query in message
        if search_query:
            pattern = re.compile(f'({re.escape(search_query)})', re.IGNORECASE)
            message = pattern.sub(r'<span class="search-highlight">\1</span>', message)

        # Build HTML
        html = f"""
        <div class="log-entry {level}">
            <div class="timestamp">⏰ {timestamp} | Line #{line_num}</div>
            <div class="namespace">📦 {namespace}</div>
            <div class="message"><strong>{level}:</strong> {message}</div>
        """

        # Add data section if present
        if 'data' in log:
            try:
                data_json = json.dumps(log['data'], indent=2)
                if search_query:
                    pattern = re.compile(f'({re.escape(search_query)})', re.IGNORECASE)
                    data_json = pattern.sub(r'<span class="search-highlight">\1</span>', data_json)
                html += f'<div class="data-section">{data_json}</div>'
            except:
                html += f'<div class="data-section">{str(log["data"])}</div>'

        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)


def main():
    """Main Streamlit app"""
    st.title("📋 DeepCode Log Viewer")
    st.markdown("**Analyze and understand DeepCode's execution flow through comprehensive log analysis**")

    # Initialize log viewer
    log_viewer = LogViewer()

    # Sidebar - File Selection
    st.sidebar.header("📁 Log File Selection")
    log_files = log_viewer.get_log_files()

    if not log_files:
        st.error("❌ No log files found in the 'logs/' directory")
        st.info("💡 Run DeepCode to generate logs first")
        return

    # File selector
    file_options = {f.name: f for f in log_files}
    selected_file_name = st.sidebar.selectbox(
        "Select log file:",
        options=list(file_options.keys()),
        help="Log files are sorted by modification time (newest first)"
    )
    selected_file = file_options[selected_file_name]

    # Display file info
    file_size = selected_file.stat().st_size / 1024  # KB
    file_mtime = datetime.fromtimestamp(selected_file.stat().st_mtime)
    st.sidebar.info(f"📊 **Size:** {file_size:.2f} KB\n\n🕒 **Modified:** {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}")

    # Load button
    if st.sidebar.button("🔄 Load Log File", type="primary"):
        with st.spinner("Loading log file..."):
            log_viewer.logs = log_viewer.load_log_file(selected_file)
            log_viewer.df = log_viewer.parse_logs_to_dataframe()
            st.session_state['logs_loaded'] = True
            st.session_state['log_viewer'] = log_viewer
            st.success(f"✅ Loaded {len(log_viewer.logs)} log entries")

    # Check if logs are loaded
    if 'logs_loaded' not in st.session_state:
        st.info("👆 Select a log file and click 'Load Log File' to begin analysis")
        return

    log_viewer = st.session_state['log_viewer']

    # Statistics Section
    st.header("📊 Log Statistics")
    stats = log_viewer.get_statistics()

    if stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Entries", stats['total_entries'])

        with col2:
            error_count = stats['level_counts'].get('ERROR', 0)
            st.metric("Errors", error_count, delta=f"{error_count} issues" if error_count > 0 else "No issues")

        with col3:
            st.metric("Entries with Data", stats['entries_with_data'])

        with col4:
            if stats['time_range'][0] and stats['time_range'][1]:
                duration = (stats['time_range'][1] - stats['time_range'][0]).total_seconds()
                st.metric("Duration", f"{duration:.1f}s")

        # Level distribution
        st.subheader("📈 Log Level Distribution")
        col1, col2 = st.columns([2, 1])

        with col1:
            level_df = pd.DataFrame(list(stats['level_counts'].items()), columns=['Level', 'Count'])
            st.bar_chart(level_df.set_index('Level'))

        with col2:
            st.dataframe(level_df, use_container_width=True)

        # Agent activity
        if stats['agent_activity']:
            st.subheader("🤖 Top Agent Activity")
            agent_df = pd.DataFrame(list(stats['agent_activity'].items()), columns=['Agent', 'Events'])
            st.dataframe(agent_df, use_container_width=True)

    # Filters Section
    st.header("🔍 Filter & Search")

    col1, col2, col3 = st.columns(3)

    with col1:
        available_levels = log_viewer.df['level'].unique().tolist() if not log_viewer.df.empty else []
        level_filter = st.multiselect(
            "Log Level:",
            options=available_levels,
            default=available_levels,
            help="Filter by log level (INFO, ERROR, WARNING, DEBUG)"
        )

    with col2:
        namespace_filter = st.text_input(
            "Namespace Filter:",
            placeholder="e.g., mcp_agent, orchestration",
            help="Filter by namespace (case-insensitive, partial match)"
        )

    with col3:
        search_query = st.text_input(
            "🔎 Search:",
            placeholder="Search in messages and data...",
            help="Search across message content and data fields"
        )

    # Apply filters
    filtered_df = log_viewer.filter_logs(
        level_filter=level_filter,
        namespace_filter=namespace_filter,
        search_query=search_query
    )

    st.info(f"📋 Showing {len(filtered_df)} of {len(log_viewer.df)} entries")

    # Display options
    st.header("📄 Log Entries")

    col1, col2 = st.columns([3, 1])
    with col1:
        display_mode = st.radio(
            "Display Mode:",
            options=["Formatted View", "Table View", "Raw JSON"],
            horizontal=True
        )

    with col2:
        max_entries = st.number_input(
            "Max entries to show:",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )

    # Display logs
    if filtered_df.empty:
        st.warning("⚠️ No log entries match the current filters")
    else:
        display_df = filtered_df.head(max_entries)

        if display_mode == "Formatted View":
            for _, row in display_df.iterrows():
                log_viewer.render_log_entry(row['_raw'], search_query)

        elif display_mode == "Table View":
            # Prepare table data
            table_data = display_df[['timestamp', 'level', 'namespace', 'message']].copy()
            st.dataframe(
                table_data,
                use_container_width=True,
                height=600
            )

        else:  # Raw JSON
            for _, row in display_df.iterrows():
                with st.expander(f"Line #{row['_line_number']} - {row['level']} - {row['namespace']}", expanded=False):
                    st.json(row['_raw'])

        # Export section
        st.header("💾 Export")
        col1, col2 = st.columns(2)

        with col1:
            # Export filtered logs as JSON
            export_json = filtered_df['_raw'].to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download Filtered Logs (JSON)",
                data=export_json,
                file_name=f"filtered_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        with col2:
            # Export as CSV
            export_csv = filtered_df[['timestamp', 'level', 'namespace', 'message']].to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Logs (CSV)",
                data=export_csv,
                file_name=f"filtered_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
