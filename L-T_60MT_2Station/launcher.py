import os
import socket
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"


def find_python():
    candidates = []

    venv_python = os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        candidates.append(venv_python)

    if sys.executable:
        candidates.append(sys.executable)

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    return "python"


def find_edge():
    candidates = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def wait_for_server(host=HOST, port=PORT, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def start_django_server(no_console=False):
    python_exe = find_python()
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" and no_console else 0

    subprocess.Popen(
        [python_exe, "manage.py", "runserver", f"{HOST}:{PORT}"],
        cwd=PROJECT_ROOT,
        creationflags=creationflags,
        stdout=subprocess.DEVNULL if no_console else None,
        stderr=subprocess.DEVNULL if no_console else None,
    )

    if not wait_for_server():
        raise RuntimeError(f"Django did not start on {URL}")


def open_browser():
    edge_path = find_edge()
    if edge_path is None:
        print("Edge was not found. Please open the app manually at:")
        print(URL)
        return

    subprocess.Popen([edge_path, f"--app={URL}", "--start-maximized"])


def main():
    args = [arg.lower() for arg in sys.argv[1:]]
    no_console = "--no-console" in args or "-n" in args

    print("Starting L&T 60MT 2Station launcher...")
    start_django_server(no_console=no_console)
    open_browser()
    print(f"Application started at {URL}")

    if not no_console:
        input("Press Enter to exit")


if __name__ == "__main__":
    main()