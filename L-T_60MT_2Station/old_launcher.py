#   ==================== With Console ===============

import subprocess
import time
import socket

python_path = r"S:\work\code\L-T_60MT_2Station\venv\Scripts\python.exe"

project_path = r"S:\work\code\L-T_60MT_2Station"


# Start Django server
subprocess.Popen(
    [
        python_path,
        "manage.py",
        "runserver",
        "127.0.0.1:8000"
    ],
    cwd=project_path
)

time.sleep(5)

# Open Edge in app mode

subprocess.Popen([
r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
"--app=http://127.0.0.1:8000",
"--start-maximized"
])

print("TESLEAD HMI Started Successfully")
input("Press Enter to Exit")

#   ==================== Without Console ===============

"""

import subprocess
import time

python_path = r"S:\work\code\L-T_60MT_2Station\venv\Scripts\python.exe"

project_path = r"S:\work\code\L-T_60MT_2Station"

PORT = 8000

# Kill existing process on port 8000

try:
    result = subprocess.check_output(
        f'netstat -ano | findstr :{PORT}',
        shell=True
    ).decode()

    lines = result.strip().split("\n")

    for line in lines:
        if "LISTENING" in line:
            pid = line.strip().split()[-1]

        subprocess.call(
            f'taskkill /PID {pid} /F',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
except:
    pass

# Start Django silently

subprocess.Popen(
    [
        python_path,
        "manage.py",
        "runserver",
        f"127.0.0.1:{PORT}"
    ],
    cwd=project_path,
    creationflags=subprocess.CREATE_NO_WINDOW
)

# Wait for startup

time.sleep(5)

# Open Edge App Mode

subprocess.Popen([
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    f"--app=http://127.0.0.1:{PORT}",
    "--start-maximized"
])


"""