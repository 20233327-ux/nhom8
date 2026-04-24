#!/usr/bin/env python
"""
ABC Document Management System - App Launcher
Khởi động ứng dụng Django trên Windows/Mac/Linux
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import platform

# Get project root
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

# Environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abc_core.settings')


class AppLauncher:
    def __init__(self):
        self.venv_path = PROJECT_ROOT / '.venv'
        self.manage_py = PROJECT_ROOT / 'manage.py'
        self.port = 8000
        self.host = '127.0.0.1'
        self.url = f'http://{self.host}:{self.port}'
        
    def check_venv(self):
        """Check if virtual environment exists"""
        if not self.venv_path.exists():
            print("❌ Virtual environment not found!")
            print("📦 Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], check=True)
            print("✅ Virtual environment created!")
            
    def activate_venv(self):
        """Activate virtual environment"""
        if platform.system() == 'Windows':
            activate_script = self.venv_path / 'Scripts' / 'activate.bat'
        else:
            activate_script = self.venv_path / 'bin' / 'activate'
        return str(activate_script)
    
    def install_requirements(self):
        """Install dependencies"""
        print("📚 Installing requirements...")
        requirements_file = PROJECT_ROOT / 'requirements.txt'
        
        if platform.system() == 'Windows':
            pip_exe = self.venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_exe = self.venv_path / 'bin' / 'pip'
            
        subprocess.run([str(pip_exe), 'install', '-r', str(requirements_file)], check=True)
        print("✅ Requirements installed!")
    
    def run_migrations(self):
        """Run Django migrations"""
        print("🗄️  Running database migrations...")
        if platform.system() == 'Windows':
            python_exe = self.venv_path / 'Scripts' / 'python.exe'
        else:
            python_exe = self.venv_path / 'bin' / 'python'
            
        subprocess.run([str(python_exe), str(self.manage_py), 'migrate'], cwd=PROJECT_ROOT)
        print("✅ Migrations completed!")
    
    def create_superuser_prompt(self):
        """Prompt to create superuser"""
        print("\n" + "="*50)
        print("🔐 Create Superuser (Admin Account)")
        print("="*50)
        
        if platform.system() == 'Windows':
            python_exe = self.venv_path / 'Scripts' / 'python.exe'
        else:
            python_exe = self.venv_path / 'bin' / 'python'
        
        try:
            subprocess.run(
                [str(python_exe), str(self.manage_py), 'createsuperuser'],
                cwd=PROJECT_ROOT
            )
        except KeyboardInterrupt:
            print("\n⏭️  Skipping superuser creation...")
    
    def run_server(self):
        """Run Django development server"""
        print(f"\n" + "="*60)
        print(f"🚀 Starting ABC Document Management System")
        print(f"📍 URL: {self.url}")
        print(f"🔐 Admin: {self.url}/admin/")
        print(f"📝 Login: {self.url}/auth/login/")
        print(f"="*60)
        print("\n✨ Loading... (This may take 10-15 seconds)")
        
        if platform.system() == 'Windows':
            python_exe = self.venv_path / 'Scripts' / 'python.exe'
        else:
            python_exe = self.venv_path / 'bin' / 'python'
        
        # Start server in background and open browser
        time.sleep(3)
        try:
            webbrowser.open(f'{self.url}/auth/login/')
        except:
            print(f"\n📂 Open browser and go to: {self.url}/auth/login/")
        
        # Run server
        subprocess.run(
            [str(python_exe), str(self.manage_py), 'runserver', f'{self.host}:{self.port}'],
            cwd=PROJECT_ROOT
        )
    
    def launch(self):
        """Main launch sequence"""
        print("\n" + "="*60)
        print("🎯 ABC Document Management System - Launcher")
        print("="*60 + "\n")
        
        try:
            # Step 1: Check virtual environment
            print("📋 Step 1: Checking virtual environment...")
            self.check_venv()
            
            # Step 2: Install requirements (if needed)
            print("\n📋 Step 2: Checking dependencies...")
            self.install_requirements()
            
            # Step 3: Run migrations
            print("\n📋 Step 3: Setting up database...")
            self.run_migrations()
            
            # Step 4: Ask to create superuser
            print("\n📋 Step 4: Admin account setup (optional)")
            response = input("Create superuser account? (y/n): ").strip().lower()
            if response == 'y':
                self.create_superuser_prompt()
            
            # Step 5: Run server
            print("\n📋 Step 5: Starting server...")
            self.run_server()
            
        except KeyboardInterrupt:
            print("\n\n👋 Application stopped by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)


if __name__ == '__main__':
    launcher = AppLauncher()
    launcher.launch()
