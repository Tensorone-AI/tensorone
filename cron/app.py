from flask import Flask, jsonify
import threading
import time
import atexit
from log_generator import insert_random_log
from log_cleanup import cleanup_old_logs

app = Flask(__name__)

# Global flag to control threads
shutdown_flag = threading.Event()

def log_generator_task():
    print("Starting log generator task...")
    while not shutdown_flag.is_set():
        try:
            result = insert_random_log()
            print(f"Log generated successfully: {result}")
            time.sleep(5)  # random 4 seconds
        except Exception as e:
            print(f"Error in log generator: {e}")
            time.sleep(5)

def log_cleanup_task():
    print("Starting log cleanup task...")
    while not shutdown_flag.is_set():
        try:
            result = cleanup_old_logs()
            print(f"Log cleanup completed: {result}")
            time.sleep(1200)  # Every 20 minutes
        except Exception as e:
            print(f"Error in log cleanup: {e}")
            time.sleep(300)

def start_background_tasks():
    print("Initializing background tasks...")
    threading.Thread(target=log_generator_task, daemon=True).start()
    threading.Thread(target=log_cleanup_task, daemon=True).start()
    print("Background tasks started")

def shutdown_tasks():
    print("Shutting down background tasks...")
    shutdown_flag.set()

# Start background tasks when module is imported (works with gunicorn)
start_background_tasks()

# Register shutdown handler
atexit.register(shutdown_tasks)

@app.route('/')
def health():
    return jsonify({"status": "running", "service": "cron-tasks"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)