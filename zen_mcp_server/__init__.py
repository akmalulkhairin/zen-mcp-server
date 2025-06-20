"""UV/UVX entry point for Zen MCP Server."""

import asyncio
import sys
from pathlib import Path


def main_entry():
    """Entry point for UV/UVX that handles async main function."""
    try:
        # Add the parent directory to Python path to find server module
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        # Import the server main function
        from server import main

        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown
        pass
    except ImportError as e:
        print(f"Error importing server module: {e}")
        print("This might indicate a packaging issue or missing dependencies.")
        print(f"Python path: {sys.path}")
        print(f"Current working directory: {Path.cwd()}")
        sys.exit(1)


if __name__ == "__main__":
    main_entry()
