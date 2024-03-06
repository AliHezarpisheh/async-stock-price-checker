"""
Script Entry Point.

This script serves as the entry point for the application.

Notes
-----
This script configures logging, imports the main module, and runs the main asynchronous
function using asyncio.
"""

import asyncio
from pathlib import Path

from config import setup_logging
from src import main

if __name__ == "__main__":
    setup_logging(Path("logging.toml"))
    asyncio.run(main())
