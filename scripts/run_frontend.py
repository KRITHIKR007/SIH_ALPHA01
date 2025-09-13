#!/usr/bin/env python3
"""
Development script to run the DyslexiaCare frontend.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the frontend development server."""
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
    
    # Check if frontend app exists
    frontend_app = project_root / "src" / "dyslexia_platform" / "frontend" / "app.py"
    if not frontend_app.exists():
        # Fall back to old location if new structure not complete
        frontend_app = project_root / "frontend" / "app.py"
        if not frontend_app.exists():
            print("❌ Frontend app not found!")
            print("Please ensure the frontend application exists.")
            sys.exit(1)
    
    print("🎨 Starting DyslexiaCare Frontend Server...")
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Python path: {sys.executable}")
    print(f"📄 Frontend app: {frontend_app}")
    
    try:
        # Run the Streamlit server
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(frontend_app),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")

if __name__ == "__main__":
    main()