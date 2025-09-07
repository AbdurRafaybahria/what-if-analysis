#!/usr/bin/env python3
"""
Launch script for What-If Analysis Dashboard
Starts both the FastAPI backend and serves the frontend
"""

import subprocess
import threading
import time
import webbrowser
import os
from pathlib import Path

def start_api_server():
    """Start the FastAPI backend server"""
    api_path = Path(__file__).parent / "api"
    os.chdir(api_path)
    subprocess.run(["python", "main.py"])

def start_frontend_server():
    """Start a simple HTTP server for the frontend"""
    frontend_path = Path(__file__).parent / "frontend"
    os.chdir(frontend_path)
    subprocess.run(["python", "-m", "http.server", "3000"])

def main():
    print("Starting What-If Analysis Dashboard...")
    print("=" * 50)
    
    # Start API server in background
    print("Starting API server on http://localhost:8002")
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # Wait a moment for API to start
    time.sleep(2)
    
    # Start frontend server in background
    print("Starting frontend server on http://localhost:3000")
    frontend_thread = threading.Thread(target=start_frontend_server, daemon=True)
    frontend_thread.start()
    
    # Wait a moment for frontend to start
    time.sleep(2)
    
    # Open browser
    print("Opening dashboard in browser...")
    webbrowser.open("http://localhost:3000")
    
    print("\nDashboard is ready!")
    print("Frontend: http://localhost:3000")
    print("API: http://localhost:8002")
    print("\nPress Ctrl+C to stop the servers")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")

if __name__ == "__main__":
    main()
