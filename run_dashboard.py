#!/usr/bin/env python3
"""
Bitcoin Price Analysis Dashboard Launcher
Simple script to launch the dashboard with error handling
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'dash', 'pandas', 'numpy', 'requests', 
        'plotly', 'dash-bootstrap-components', 'yfinance'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing dependencies with:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_files():
    """Check if required files exist"""
    print("\nChecking project files...")
    
    required_files = [
        'dashboard.py',
        'data_fetcher.py', 
        'technical_analysis.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present!")
    return True

def run_tests():
    """Run the test suite to verify functionality"""
    print("\nRunning tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_data.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            print("Test output:")
            print(result.stdout)
            print("Test errors:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out!")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def launch_dashboard():
    """Launch the dashboard"""
    print("\n🚀 Launching Bitcoin Price Analysis Dashboard...")
    print("=" * 60)
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the dashboard")
    print("=" * 60)
    
    try:
        # Launch the dashboard
        subprocess.run([sys.executable, 'dashboard.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")

def main():
    """Main launcher function"""
    print("Bitcoin Price Analysis Dashboard Launcher")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        return False
    
    # Check files
    if not check_files():
        print("\n❌ File check failed. Please ensure all project files are present.")
        return False
    
    # Ask user if they want to run tests
    print("\nWould you like to run tests before launching? (y/n): ", end="")
    try:
        user_input = input().lower().strip()
        if user_input in ['y', 'yes']:
            if not run_tests():
                print("\n❌ Tests failed. Dashboard may not work correctly.")
                print("Continue anyway? (y/n): ", end="")
                continue_input = input().lower().strip()
                if continue_input not in ['y', 'yes']:
                    return False
        elif user_input not in ['n', 'no']:
            print("Invalid input. Skipping tests.")
    except KeyboardInterrupt:
        print("\n\n🛑 Launcher stopped by user")
        return False
    
    # Launch dashboard
    launch_dashboard()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Launcher stopped by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

