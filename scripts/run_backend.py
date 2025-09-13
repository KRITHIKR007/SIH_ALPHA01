#!/usr/bin/env python3
"""
Development script to run the DyslexiaCare backend server.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the backend development server."""
    # Change to project root directory
    os.chdir(project_root)
    
    # Set environment variables
    os.environ["PYTHONPATH"] = str(project_root)
    
    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please copy config/.env.example to .env and configure it.")
        sys.exit(1)
    
    print("🚀 Starting DyslexiaCare Backend Server...")
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Python path: {sys.executable}")
    
    try:
        # Run the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.dyslexia_platform.backend.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped by user")

if __name__ == "__main__":
    main()