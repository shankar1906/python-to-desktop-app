import subprocess

subprocess.Popen([
    "waitress-serve",
    "--host=127.0.0.1",
    "--port=8000",
    "standard_soft.wsgi:application"
])