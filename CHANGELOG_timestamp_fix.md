# Timestamp Format Enhancement - Changelog

## Date: 2026-02-08

## Summary
Enhanced project folder naming to use human-readable datetime strings instead of Unix timestamps for better developer experience and log readability.

## Changes Made

### 1. Chat Project Directory Naming
**File**: `workflows/agent_orchestration_engine.py` (Line 1930-1934)

**Before**:
```python
import time
timestamp = str(int(time.time()))
paper_name = f"chat_project_{timestamp}"
# Example: chat_project_1770605298
```

**After**:
```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
paper_name = f"chat_project_{timestamp}"
# Example: chat_project_20260208_214743
```

### 2. Research Paper Directory Naming
**File**: `workflows/agent_orchestration_engine.py` (Line 499-512)

**Before**:
```python
existing_ids = [
    int(d)
    for d in os.listdir(papers_dir)
    if os.path.isdir(os.path.join(papers_dir, d)) and d.isdigit()
]
next_id = max(existing_ids) + 1 if existing_ids else 1
paper_dir = os.path.join(papers_dir, str(next_id))
# Example: ./deepcode_lab/papers/1
```

**After**:
```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
paper_id = f"paper_{timestamp}"
paper_dir = os.path.join(papers_dir, paper_id)
# Example: ./deepcode_lab/papers/paper_20260208_214743
```

### 3. Global Replacements
All references to `next_id` were updated to `paper_id` throughout the file for consistency.

## Benefits

### 1. **Improved Readability**
- **Before**: `chat_project_1770605298` (requires timestamp converter to understand)
- **After**: `chat_project_20260208_214743` (instantly readable as Feb 8, 2026 at 21:47:43)

### 2. **Better Debugging**
- Easier to correlate project folders with log files
- Timestamps match the log file naming pattern: `logs/mcp-agent-20260208_214743.jsonl`
- Quick chronological sorting in file explorers

### 3. **Enhanced Developer Experience**
- No need for external tools to convert Unix timestamps
- Natural sorting in file systems
- Better compatibility with log viewer timestamps

## Example Folder Structure

### Before:
```
deepcode_lab/papers/
├── 1/
├── 2/
├── chat_project_1770605298/
└── chat_project_1770605350/
```

### After:
```
deepcode_lab/papers/
├── paper_20260208_210000/
├── paper_20260208_213000/
├── chat_project_20260208_214743/
└── chat_project_20260208_215530/
```

## Format Specification

**Timestamp Format**: `%Y%m%d_%H%M%S`
- `%Y` - 4-digit year (2026)
- `%m` - 2-digit month (02)
- `%d` - 2-digit day (08)
- `%H` - 2-digit hour (24-hour format, 21)
- `%M` - 2-digit minute (47)
- `%S` - 2-digit second (43)

**Result**: `20260208_214743` = February 8, 2026 at 9:47:43 PM

## Backward Compatibility

⚠️ **Note**: This change does not affect existing project folders. Old folders with integer IDs will continue to work normally. New projects created after this update will use the datetime-based naming convention.

## Testing Recommendations

1. **Create New Chat Project**:
   ```bash
   python cli/main_cli.py
   # Enter your requirements
   # Check that new folder uses format: chat_project_YYYYMMDD_HHMMSS
   ```

2. **Process Research Paper**:
   ```bash
   python deepcode.py
   # Upload a paper or provide URL
   # Check that new folder uses format: paper_YYYYMMDD_HHMMSS
   ```

3. **Verify Log Viewer**:
   ```bash
   python view_logs.py
   # Confirm log files and project folders have matching timestamp patterns
   ```

## Related Files

- `workflows/agent_orchestration_engine.py` - Main changes
- `utils/log_viewer.py` - Log viewer (unchanged, but benefits from consistent naming)
- `README_view_logs.md` - Documentation for log viewer
- `mcp_agent.config.yaml` - Log file naming configuration (unchanged)

## Impact Assessment

- ✅ **Code Impact**: Minimal - localized to project folder creation
- ✅ **Performance**: No impact - timestamp generation is O(1)
- ✅ **Existing Projects**: No impact - old folders continue to work
- ✅ **Log Correlation**: Significantly improved - matching timestamp formats
- ✅ **Developer Experience**: Major improvement in readability

## Migration Notes

No migration required. The system will automatically use the new naming convention for all new projects while continuing to support existing projects with integer-based naming.

---

**Author**: DeepCode Team
**Reviewed**: 2026-02-08
**Status**: ✅ Completed
