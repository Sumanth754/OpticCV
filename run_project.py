import subprocess
import time
import sys
import os
import requests

def is_backend_up():
    try:
        response = requests.get("http://127.0.0.1:7777/health", timeout=1)
        return response.status_code == 200
    except:
        return False

def run():
    print("🚀 Starting NexusDocs Production Suite...")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(project_root, "data"), exist_ok=True)
    os.makedirs(os.path.join(project_root, "vector_store"), exist_ok=True)

    env = os.environ.copy()
    env["PYTHONPATH"] = project_root

    # Start Backend on explicit IPv4
    print("📂 Initializing Backend (127.0.0.1:7777)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api.main:app", "--port", "7777", "--host", "127.0.0.1"],
        cwd=project_root,
        env=env
    )

    # Smart Waiting
    print("⏳ Waiting for backend to verify system state...")
    max_retries = 30
    ready = False
    for i in range(max_retries):
        if is_backend_up():
            ready = True
            break
        time.sleep(1)
        if i % 5 == 0 and i > 0:
            print(f"   Still initializing ({i}s)...")

    if not ready:
        print("❌ Backend failed to start. Please check the logs.")
        backend_process.terminate()
        return

    print("✅ Backend is ALIVE and listening.")

    # Start Frontend
    print("🎨 Launching Interactive UI...")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "ui/app.py", "--server.port", "8501", "--server.address", "127.0.0.1"],
            cwd=project_root,
            env=env
        )
    except KeyboardInterrupt:
        print("\nShutting down NexusDocs...")
        backend_process.terminate()

if __name__ == "__main__":
    run()
