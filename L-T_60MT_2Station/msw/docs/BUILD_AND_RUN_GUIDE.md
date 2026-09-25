# L&T 60MT 2Station — Build and Run Guide

This document explains how to build the desktop app and run the project using the provided launcher.

## 1. Prerequisites

Install these on a Windows machine:

- Python 3.11 or 3.12 (64-bit)
- Node.js LTS
- Rust and Cargo
- Visual Studio Build Tools with C++ workload
- MySQL 8.x

### Verify tools

```powershell
python --version
node --version
npm --version
cargo --version
rustc --version
```

## 2. Project structure

```text
L-T_60MT_2Station/
├── build_desktop.ps1
├── launcher.py
├── manage.py
├── start_backend.py
├── .env
├── venv/
├── desktop/
│   └── L-T_60MT_2STATION/
│       ├── package.json
│       └── src-tauri/
```

## 3. Create the Python environment

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install waitress whitenoise
```

If needed for MySQL support:

```powershell
pip install PyMySQL
```

## 4. Configure the database

Create a .env file in the project root with values like:

```env
NAME=landt60mt-2station
USER=root
PASSWORD=root
HOST=127.0.0.1
PORT=3306
```

Then make sure MySQL is running and the database exists.

## 5. Apply migrations

```powershell
.\venv\Scripts\python.exe .\manage.py migrate
```

## 6. Run the launcher

### Console mode

```powershell
.\venv\Scripts\python.exe .\launcher.py
```

### No-console mode

```powershell
.\venv\Scripts\python.exe .\launcher.py --no-console
```

The launcher will:
- start Django on http://127.0.0.1:8000
- wait until the server responds
- open Microsoft Edge in app mode

## 7. Build the desktop app

From the project root, run:

```powershell
.\build_desktop.ps1
```

This script will:
- check required tools
- collect Django static files
- install desktop dependencies
- build the Tauri MSI installer

### Output

The MSI installer will be created here:

```text
desktop/L-T_60MT_2STATION/src-tauri/target/release/bundle/msi/
```

## 8. Run the desktop app in development mode

```powershell
cd desktop\L-T_60MT_2STATION
npm run tauri dev
```

## 9. Notes

- The launcher uses the local project files and the Windows virtual environment.
- For a full working installation, MySQL and the database must be available.
- The build script assumes Rust/Cargo is available in the PATH.
