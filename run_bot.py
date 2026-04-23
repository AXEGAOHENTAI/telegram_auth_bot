#!/usr/bin/env python3
"""
Simple script to run the bot on server without encoding issues
"""

import os
import sys

# Set environment variables for proper encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['LANG'] = 'en_US.UTF-8'

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the bot"""
    try:
        # Import and run the bot
        from telegram_bot import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 