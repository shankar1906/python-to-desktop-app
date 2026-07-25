import os
import socket
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))


def build_command():
    if os.name == "nt":
        venv_python = os.path.join(ROOT, "venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            return [venv_python, "manage.py", "runserver", "127.0.0.1:8000"]

        venv_waitress = os.path.join(ROOT, "venv", "Scripts", "waitress-serve.exe")
        if os.path.exists(venv_waitress):
            return [venv_waitress, "--host=127.0.0.1", "--port=8000", "standard_soft.wsgi:application"]

    python_exe = sys.executable
    return [python_exe, "manage.py", "runserver", "127.0.0.1:8000"]


def wait_for_port(host="127.0.0.1", port=8000, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def main():
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0

    subprocess.Popen(
        build_command(),
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
    )

    started = wait_for_port()
    if not started:
        raise RuntimeError("Django backend did not become available on http://127.0.0.1:8000")


if __name__ == "__main__":
    main()