# UV/UVX Migration Plan for Zen MCP Server

## Phase 1: UV/UVX Support (No PyPI Publishing)

### Project Standards Compliance
- **PR Title**: `feat: add UV/UVX support with config file approach`
- **Quality Requirements**: All code must pass `./code_quality_checks.sh` (100%)
- **Testing**: New features require both unit and simulator tests
- **Documentation**: Update relevant docs and add examples

### Implementation Strategy

#### Option A: Config File Approach (Recommended)
```json
{
  "mcpServers": {
    "zen": {
      "command": "uvx",
      "args": ["--from", "/path/to/zen-mcp-server", "zen_mcp_server", "--config", "/path/to/zen-config.json"]
    }
  }
}
```

#### Option B: Environment Injection
```json
{
  "mcpServers": {
    "zen": {
      "command": "uvx", 
      "args": ["--from", "/path/to/zen-mcp-server", "zen_mcp_server"],
      "env": {
        "GEMINI_API_KEY": "your-key",
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

## Detailed Implementation Plan

### 1. Core Changes Required

**A. Create Entry Point Module** (`zen_mcp_server/__init__.py`)
```python
"""UV/UVX entry point for Zen MCP Server."""
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import main

if __name__ == "__main__":
    main()
```

**B. Update `pyproject.toml`**
```toml
[project.scripts]
zen_mcp_server = "zen_mcp_server:main"

[project]
name = "zen-mcp-server"
dynamic = ["version"]
dependencies = [
    "mcp>=1.0.0",
    "google-genai>=1.19.0", 
    "openai>=1.55.2",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0"
]
```

**C. Enhance `server.py`** - Add CLI argument parsing:
```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Zen MCP Server")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--env-file", help="Path to .env file") 
    return parser.parse_args()

def main():
    args = parse_args()
    # Handle config file loading
    # ... existing server logic
```

### 2. Configuration System

**A. Support Multiple Config Sources:**
1. **Command line config file**: `--config zen-config.json`
2. **Environment variables**: Current `.env` approach  
3. **Global config**: `~/.config/zen-mcp/config.json`

**B. Config File Format:**
```json
{
  "api_keys": {
    "gemini": "your-key-here",
    "openai": "your-key-here", 
    "xai": "your-key-here"
  },
  "settings": {
    "default_model": "auto",
    "log_level": "DEBUG"
  }
}
```

### 3. Files That Need Modification

**🔴 Core Files:**
- **`pyproject.toml`** - Add entry point and proper packaging
- **`server.py`** - Add CLI argument parsing and config loading  
- **`config.py`** - Extend to support JSON config files

**🟡 New Files:**  
- **`zen_mcp_server/__init__.py`** - Entry point module
- **`zen_mcp_server/__main__.py`** - Main execution entry
- **`utils/config_loader.py`** - Config file parsing logic

**🟢 Documentation:**
- **`README.md`** - Add UV/UVX installation section
- **`examples/`** - Add UV config examples
- **`docs/configuration.md`** - Update with new config options

**🔵 Testing:**
- **`tests/test_config_loader.py`** - Unit tests for config parsing
- **`tests/test_uv_entry_point.py`** - Entry point testing
- **`simulator_tests/test_uv_integration.py`** - End-to-end UV testing

### 4. Work Estimate Breakdown

| Task | Hours | Complexity |
|------|-------|------------|
| **Core Implementation** | | |
| Update `pyproject.toml` | 1 | Low |
| Create entry point module | 1 | Low |
| Add CLI argument parsing | 2 | Medium |
| Config file loading system | 3 | Medium |
| **Testing** | | |
| Unit tests for config system | 3 | Medium |
| UV integration simulator test | 2 | Medium |
| Cross-platform testing | 2 | Medium |
| **Documentation** | | |
| Update README with UV section | 1 | Low |
| Create config examples | 1 | Low |
| Update configuration docs | 1 | Low |
| **Quality Assurance** | | |
| Code quality checks | 1 | Low |
| Manual testing | 1 | Low |
| **TOTAL** | **19 hours** | |

## Phase 1 Summary

### What Phase 1 Delivers:
✅ **UV/UVX Support**: `uvx --from /path/to/repo zen_mcp_server`  
✅ **Config File System**: JSON-based configuration  
✅ **Backward Compatibility**: All existing functionality preserved  
✅ **Multiple Config Sources**: CLI args, config files, environment variables  
✅ **Cross-Platform**: Works on macOS, Linux, WSL  

### User Benefits:
- **Simpler Setup**: No more virtual environment management  
- **Cleaner Config**: Organize API keys in JSON files  
- **Flexibility**: Choose between `.env` files or JSON config  
- **Future-Ready**: Foundation for Phase 2 (PyPI publishing)

### Developer Benefits:
- **Follows Project Standards**: 100% compliant with contribution guidelines  
- **Comprehensive Testing**: Unit + simulator + integration tests  
- **Proper Documentation**: Updated README and config docs  
- **Quality Assured**: Passes all automated checks

### Implementation Strategy:
1. **Start Small**: Basic entry point + pyproject.toml
2. **Add Config System**: JSON config file support  
3. **Test Thoroughly**: Unit, simulator, and manual testing
4. **Document Everything**: README, examples, and configuration docs
5. **Quality Check**: Run `./code_quality_checks.sh` before PR

### PR Timeline:
- **Week 1**: Core implementation (entry point, config system)
- **Week 2**: Testing and documentation  
- **Week 3**: Quality assurance and PR submission

## Phase 2: PyPI Publishing (Future)

### Automated PyPI Releases
The project already has sophisticated automation that can be extended:

✅ **Current Automation:**
- Semantic versioning based on PR titles  
- Automatic version bumping  
- Git tagging and GitHub releases  
- Docker image publishing  
- Multi-Python version testing

### PyPI Integration Options:

#### Option 1: Tag-Triggered Release (Recommended)
```yaml
name: Publish to PyPI
on:
  push:
    tags:
      - 'v*'  # Triggers on version tags like v1.2.3
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install build tools
      run: pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

### Phase 2 Benefits:
✅ **Global Installation**: `uvx zen-mcp-server`  
✅ **Automatic Updates**: Users get latest versions  
✅ **Simplified Distribution**: No need to clone repos  
✅ **Professional Package**: Listed on PyPI  

### Phase 2 Setup Required:
1. **PyPI API Token** (~5 minutes)
2. **Package Configuration** (~2 hours)  
3. **Workflow File** (~1 hour)
4. **Testing Pipeline** (~2 hours)

**Total Phase 2 Effort**: ~5 hours

## Critical Challenge: API Key Configuration

### The Problem:
UVX runs tools in isolated environments, but this MCP needs access to multiple API keys:
- `GEMINI_API_KEY`
- `OPENAI_API_KEY` 
- `XAI_API_KEY`
- `OPENROUTER_API_KEY`
- Plus 13 optional configuration variables

**Issue**: UVX doesn't inherit shell environment variables by default.

### Solutions:

#### Solution 1: Environment Injection (Claude Desktop)
```json
{
  "mcpServers": {
    "zen": {
      "command": "uvx",
      "args": ["zen-mcp-server"],
      "env": {
        "GEMINI_API_KEY": "your-key-here",
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

#### Solution 2: Config File Approach (Recommended)
```json
{
  "mcpServers": {
    "zen": {
      "command": "uvx", 
      "args": ["zen-mcp-server", "--config", "/path/to/zen-config.json"]
    }
  }
}
```

Config file format:
```json
{
  "api_keys": {
    "gemini": "your-key-here",
    "openai": "your-key-here"
  },
  "settings": {
    "default_model": "auto"
  }
}
```

## Current vs Future Comparison

### Current Setup Issues:
- **Complex Paths**: `/path/to/zen-mcp-server/.zen_venv/bin/python`
- **Platform-Specific**: Different paths for macOS/Linux/WSL
- **Setup Required**: Must run `./run-server.sh` first to create venv
- **Path Dependencies**: Breaks if you move the project

### With Phase 1 (UV Support):
- **Simpler Command**: `uvx --from /path/to/repo zen_mcp_server`
- **No Virtual Environment**: UV handles isolation automatically
- **Cross-Platform**: Same command works everywhere  
- **Flexible Config**: JSON files or environment variables

### With Phase 2 (PyPI):
- **Ultra Simple**: `uvx zen-mcp-server`
- **Global Installation**: No path dependencies
- **Automatic Updates**: Latest versions always available
- **Professional Distribution**: Standard Python packaging

## Next Steps

1. **Save this plan** for reference
2. **Set up GitHub MCP** for issue/PR management  
3. **Start Phase 1 implementation** with entry point creation
4. **Test locally** with UV/UVX before PR submission
5. **Follow project standards** for quality and testing

This plan provides a clear roadmap for modernizing the Zen MCP Server with UV/UVX support while maintaining the project's high standards and backward compatibility.