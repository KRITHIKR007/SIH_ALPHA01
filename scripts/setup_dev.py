#!/usr/bin/env python3
"""
Development setup script for DyslexiaCare platform.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Setup development environment."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🛠️  Setting up DyslexiaCare Development Environment...")
    print(f"📁 Project root: {project_root}")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create .env file if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / "config" / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created - please review and update settings")
    
    # Create required directories
    directories = [
        "src/dyslexia_platform/data/uploads",
        "src/dyslexia_platform/data/outputs", 
        "src/dyslexia_platform/data/models",
        "logs"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Install dependencies
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Please install manually: pip install -r requirements.txt")
    
    # Initialize database
    print("🗄️  Initializing database...")
    try:
        # Add project to Python path
        sys.path.insert(0, str(project_root))
        
        from config import get_settings
        from src.dyslexia_platform.database import create_tables
        
        settings = get_settings()
        create_tables()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("You may need to run this manually later")
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Review and update .env file with your settings")
    print("2. Run backend: python scripts/run_backend.py")
    print("3. Run frontend: python scripts/run_frontend.py")
    print("4. Access the application at http://localhost:8501")
    print("5. API documentation at http://localhost:8000/docs")

if __name__ == "__main__":
    main()