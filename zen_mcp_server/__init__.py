"""UV/UVX entry point for Zen MCP Server."""
import asyncio
import sys
from pathlib import Path


def main_entry():
    """Entry point for UV/UVX that handles async main function."""
    try:
        # Import the server main function
        from server import main
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown
        pass
    except ImportError as e:
        print(f"Error importing server module: {e}")
        print("This might indicate a packaging issue or missing dependencies.")
        sys.exit(1)


if __name__ == "__main__":
    main_entry()