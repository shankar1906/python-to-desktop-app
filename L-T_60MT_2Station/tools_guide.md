# Development Tools Guide

This project requires a Windows build machine for packaging the desktop app.

## Required tools

### 1. Python 3.11 or 3.12 (64-bit)
- Download: https://www.python.org/downloads/
- Install: select "Add Python to PATH"
- Verify:
  ```powershell
  python --version
  ```

### 2. Node.js LTS
- Download: https://nodejs.org/
- Verify:
  ```powershell
  node --version
  npm --version
  ```

### 3. Rust and Cargo
- Download: https://rustup.rs/
- Verify:
  ```powershell
  cargo --version
  rustc --version
  ```

### 4. Visual Studio Build Tools 2022
- Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Required workload:
  - Desktop development with C++
- Required components:
  - MSVC v143 - VS 2022 C++ x64/x86 build tools
  - Windows 10/11 SDK

### 5. MySQL 8.x (for app runtime/database)
- Download: https://dev.mysql.com/downloads/mysql/
- Verify:
  ```powershell
  mysql --version
  ```

## Project folder structure

```text
L-T_60MT_2Station/
├── build_desktop.ps1
├── manage.py
├── start_backend.py
├── .env
├── venv/
├── desktop/
│   └── L-T_60MT_2STATION/
│       ├── package.json
│       └── src-tauri/
│           ├── tauri.conf.json
│           └── src/
```

## Build flow

Run the build script from the project root:

```powershell
./build_desktop.ps1
```

The script will:
1. Check required tools.
2. Ensure the Python virtual environment exists.
3. Collect Django static files.
4. Install desktop dependencies.
5. Build the Tauri MSI installer.

## Installer output

The generated installer will appear at:

```text
desktop/L-T_60MT_2STATION/src-tauri/target/release/bundle/msi/
```

## Common issues

### Cargo not found
If `cargo` is not recognized, add Rust to PATH or reinstall Rustup.

### Visual Studio Build Tools missing
Install the C++ workload before building Tauri.

### MySQL not running
The app needs MySQL for the Django backend/database connection.
