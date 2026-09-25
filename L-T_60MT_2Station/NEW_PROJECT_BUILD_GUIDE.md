# New Project End-to-End Build Guide
## Blueprint: Django Backend + Waitress + MySQL + Tauri / Edge Desktop Shell

This document is also available at [msw/docs/NEW_PROJECT_BUILD_GUIDE.md](file:///home/ms/Desktop/work/code/L-T_60MT_2Station/msw/docs/NEW_PROJECT_BUILD_GUIDE.md).

---

## 1. Architecture Overview

This architecture combines the stability of Python/Django with a native desktop shell:

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Desktop Shell** | **Pick one:** Option A PyInstaller + Edge, **or** Option B Tauri v2 | Starts Django and opens the UI window (see comparison below) |
| **WSGI Server** | Waitress | Production-grade WSGI server running Django locally on `127.0.0.1:8000` |
| **Backend Framework** | Django | Core business logic, APIs, database ORM, HTML templates |
| **Database** | MySQL Server 8.x | Robust local database storage |
| **Automated Builder** | PowerShell (`build_desktop.ps1`) | **Option B only** — collects static files and builds the Tauri MSI/EXE installer |

### System Execution Flow
```text
User launches Application Executable / Desktop Shortcut
                 │
                 ▼
     [Desktop Launcher Shell]
 (Option A: PyInstaller launcher.exe  OR  Option B: Tauri app.exe)
                 │
                 ├─► Spawns `start_backend.py` in background (Windowless)
                 │     │
                 │     └─► Launches Waitress WSGI server (`waitress-serve`) on port 8000
                 │
                 ├─► Polls http://127.0.0.1:8000 until responsive (max 30s)
                 │
                 └─► Opens Window loading UI at http://127.0.0.1:8000
```

### Choose ONE Desktop Packaging Option (they are NOT the same)

Both produce a `.exe`, but they are **different products**. Build **one** path for a given project — do not expect PyInstaller and Tauri outputs to match.

| | **Option A — PyInstaller Launcher** | **Option B — Tauri Desktop App** |
| :--- | :--- | :--- |
| **What you build** | `pyinstaller ... launcher.py` | `.\build_desktop.ps1` / `npm run tauri build` |
| **Output** | `dist\MyNewApp_Launcher.exe` | `desktop\...\bundle\msi\` (installer) and/or `...\bundle\nsis\` / exe |
| **What the EXE is** | Thin starter: runs `start_backend.py`, then opens **installed Microsoft Edge** in `--app=` mode | Real **native Windows app** with its own WebView2 window (no Edge browser UI) |
| **Needs on build PC** | Python + PyInstaller only | Python + Node.js + Rust + VS C++ Build Tools |
| **Needs on client PC** | Project folder (or deploy layout) + Python venv + Edge + MySQL | Installer run once; WebView2 runtime; MySQL; app files as shipped |
| **Installer / Start Menu** | No — just a single launcher EXE | Yes — MSI/NSIS installer, shortcuts, native window |
| **Best for** | Quick internal/dev use, demos, machines that already have Edge | Customer / production desktop delivery |

**Rule of thumb**
- Want a fast “double-click to open Edge app mode”? → **Option A** (Step 6). Stop after Step 6 if that is enough.
- Want a real desktop product with installer? → **Option B** (Steps 7–8). Skip PyInstaller packaging unless you also want a separate lightweight launcher.

---

## 2. System Requirements & Prerequisites

### Build Machine Setup (Windows 10/11 64-bit)

Install what you need for the option you chose:

| Dependency | Option A (PyInstaller) | Option B (Tauri) |
| :--- | :---: | :---: |
| **Python 3.11 or 3.12 (64-bit)** — “Add Python to PATH” | Required | Required |
| **MySQL Community Server 8.x** (port `3306`) | Required | Required |
| **Node.js LTS (v18+)** / `npm` | Not required | Required |
| **Rust** via `rustup` (`https://rustup.rs`) | Not required | Required |
| **Visual Studio 2022 Build Tools** — workload **Desktop development with C++** (MSVC v143, Windows SDK, CMake) | Not required | Required |

---

## 3. Step-by-Step Project Creation

### Step 1 — Create Project Folder Structure

Create the root directory for your new project (e.g., `MyNewIndustrialApp`):

```text
MyNewIndustrialApp/
├── .env                       # Environment & DB credentials
├── .gitignore
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management CLI
├── start_backend.py           # Background WSGI launcher script
├── launcher.py                # Standalone Edge/Chrome app launcher script
├── build_desktop.ps1          # Automated installer build pipeline script
├── standard_soft/             # Django project configuration package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── standard_app/              # Main Django application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── msw/
│   └── docs/                  # Project documentation
└── desktop/
    └── MyNewAppShell/         # Tauri desktop shell root
        ├── package.json
        └── src-tauri/
            ├── tauri.conf.json
            ├── Cargo.toml
            └── src/
                ├── main.rs
                └── lib.rs
```

---

### Step 2 — Set Up Python Virtual Environment & Install Dependencies

Open PowerShell in the project root:

```powershell
# Create virtual environment named 'venv'
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

Create `requirements.txt` in the root directory:

```text
Django>=4.2,<5.0
waitress>=2.1.2
whitenoise>=6.5.0
PyMySQL>=1.1.0
python-dotenv>=1.0.0
pyinstaller>=6.0.0
```

Install requirements:

```powershell
pip install -r requirements.txt
```

---

### Step 3 — Initialize Django Project & Application

Run Django administrative commands to set up the Django project:

```powershell
# Initialize project configuration folder
django-admin startproject standard_soft .

# Initialize application module
python manage.py startapp standard_app
```

#### 1. Update `standard_soft/__init__.py`
Enable `PyMySQL` as the MySQL database driver for Python:

```python
import pymysql

pymysql.install_as_MySQLdb()
```

#### 2. Configure `standard_soft/settings.py`
Configure environment variable loading, static file handling with WhiteNoise, database connections, and registered apps:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key-change-this-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'standard_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'standard_soft.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'standard_app' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'standard_soft.wsgi.application'

# Database configuration using .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'mynewapp_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

### Step 4 — Environment & MySQL Database Setup

#### 1. Create `.env` file in the root directory:

```env
DB_NAME=mynewapp_db
DB_USER=root
DB_PASSWORD=root
DB_HOST=127.0.0.1
DB_PORT=3306
DEBUG=True
SECRET_KEY=your-custom-secure-secret-key
```

#### 2. Create MySQL Database
Execute in MySQL Shell or MySQL Workbench:

```sql
CREATE DATABASE `mynewapp_db`;
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON `mynewapp_db`.* TO 'root'@'127.0.0.1';
FLUSH PRIVILEGES;
```

#### 3. Run Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

### Step 5 — Create Backend Production Launcher (`start_backend.py`)

Create `start_backend.py` in the root directory. This script handles launching the Django backend using Waitress (or Django dev server) in background mode, and verifies port availability:

```python
import os
import socket
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = "127.0.0.1"
PORT = 8000

def build_command():
    if os.name == "nt":
        venv_waitress = os.path.join(ROOT, "venv", "Scripts", "waitress-serve.exe")
        if os.path.exists(venv_waitress):
            return [venv_waitress, f"--host={HOST}", f"--port={PORT}", "standard_soft.wsgi:application"]

        venv_python = os.path.join(ROOT, "venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            return [venv_python, "manage.py", "runserver", f"{HOST}:{PORT}"]

    python_exe = sys.executable
    return [python_exe, "manage.py", "runserver", f"{HOST}:{PORT}"]

def wait_for_port(host=HOST, port=PORT, timeout=60):
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
        raise RuntimeError(f"Django backend did not become available on http://{HOST}:{PORT}")

if __name__ == "__main__":
    main()
```

---

### Step 6 — Option A only: Browser App Launcher & PyInstaller EXE (`launcher.py`)

> **Skip this entire step if you are shipping Option B (Tauri) only.**  
> This path does **not** produce the same EXE as Tauri. It only packages `launcher.py`.

Create `launcher.py` in the root directory to start Django and open Edge in app/kiosk mode (no Rust required):

```python
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
    venv_python = os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable or "python"

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
        [python_exe, "start_backend.py"],
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
        print("Edge was not found. Please open manually at:", URL)
        return

    subprocess.Popen([edge_path, f"--app={URL}", "--start-maximized"])

def main():
    args = [arg.lower() for arg in sys.argv[1:]]
    no_console = "--no-console" in args or "-n" in args

    print("Starting Application Launcher...")
    start_django_server(no_console=no_console)
    open_browser()
    print(f"Application started at {URL}")

    if not no_console:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
```

#### Compile Option A launcher EXE with PyInstaller

```powershell
# From project root, with venv activated
pip install pyinstaller
pyinstaller --onefile --noconsole --name="MyNewApp_Launcher" launcher.py
```

| Item | Detail |
| :--- | :--- |
| **Output file** | `dist\MyNewApp_Launcher.exe` |
| **What it does** | Starts Waitress via `start_backend.py`, then launches Edge at `http://127.0.0.1:8000` |
| **What it does NOT do** | Does **not** embed Django, templates, MySQL, or a native WebView. Client still needs the project folder + `venv` + Edge + MySQL. |
| **Same as Tauri?** | **No.** Different binary, different UI host (Edge vs WebView2), no MSI installer. |

Run for a quick smoke test:

```powershell
.\dist\MyNewApp_Launcher.exe
```

If Option A is all you need, you can stop here. For a customer installer / native window, continue with **Option B** (Steps 7–8).

---

### Step 7 — Option B only: Native Desktop Shell with Tauri v2

> **Skip Steps 7–8 if you only want Option A (PyInstaller + Edge).**  
> Tauri’s MSI/EXE is a **different** deliverable from `MyNewApp_Launcher.exe`.

Create the `desktop` directory in the project root:

```powershell
mkdir desktop
cd desktop
```

Initialize Tauri App:

```powershell
npm create tauri-app@latest MyNewAppShell -- --template vanilla
cd MyNewAppShell
```

#### 1. Update `package.json`
Configure `package.json` to generate an HTML document that immediately redirects the webview window to the local Django server:

```json
{
  "name": "mynewappshell",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "node -e \"const fs=require('fs'); fs.mkdirSync('dist',{recursive:true}); fs.writeFileSync('dist/index.html', '<!DOCTYPE html><html><head><meta charset=\\\"utf-8\\\"><meta http-equiv=\\\"refresh\\\" content=\\\"0; url=http://127.0.0.1:8000\\\" /><title>My New App</title></head><body>Launching application...</body></html>');\"",
    "build": "node -e \"const fs=require('fs'); fs.mkdirSync('dist',{recursive:true}); fs.writeFileSync('dist/index.html', '<!DOCTYPE html><html><head><meta charset=\\\"utf-8\\\"><meta http-equiv=\\\"refresh\\\" content=\\\"0; url=http://127.0.0.1:8000\\\" /><title>My New App</title></head><body>Launching application...</body></html>');\"",
    "tauri": "tauri"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^2.0.0"
  }
}
```

#### 2. Update `src-tauri/tauri.conf.json`

```json
{
  "$schema": "../node_modules/@tauri-apps/cli/config.schema.json",
  "productName": "MyNewApp",
  "version": "0.1.0",
  "identifier": "com.mynewapp.desktop",
  "build": {
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "windows": [
      {
        "title": "My New Industrial Application",
        "width": 1280,
        "height": 800,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

#### 3. Configure Rust Backend Supervisor (`src-tauri/src/lib.rs`)
Edit `src-tauri/src/lib.rs` to locate the project directory, spawn `start_backend.py` without opening a command window, and await port readiness:

```rust
use std::env;
use std::net::TcpStream;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;
use tauri::Manager;

fn find_project_dir(search_roots: &[PathBuf]) -> Option<PathBuf> {
    for root in search_roots {
        let mut current = root.clone();
        loop {
            if current.join("start_backend.py").exists() && current.join("manage.py").exists() {
                return Some(current);
            }
            if !current.pop() {
                break;
            }
        }
    }
    None
}

fn find_python_executable(project_dir: &Path) -> Option<String> {
    let windows_candidates = [
        project_dir.join("venv").join("Scripts").join("python.exe"),
        project_dir.join("venv").join("Scripts").join("python"),
    ];

    for candidate in &windows_candidates {
        if candidate.exists() {
            return candidate.to_str().map(|v| v.to_string());
        }
    }

    if cfg!(windows) {
        Some("python".to_string())
    } else {
        Some("python3".to_string())
    }
}

fn wait_for_backend(host: &str, port: u16, timeout_secs: u64) -> bool {
    let deadline = std::time::Instant::now() + Duration::from_secs(timeout_secs);
    while std::time::Instant::now() < deadline {
        if TcpStream::connect(format!("{host}:{port}")).is_ok() {
            return true;
        }
        thread::sleep(Duration::from_secs(1));
    }
    false
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let app_dir = app
                .path()
                .resource_dir()
                .unwrap_or_else(|_| app.path().app_local_data_dir().unwrap());

            let current_dir = env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
            let search_roots = [
                app_dir.clone(),
                current_dir.clone(),
                app_dir.join(r"..\..\.."),
                app_dir.join(r"..\..\..\.."),
            ];

            if let Some(project_dir) = find_project_dir(&search_roots) {
                let backend_script = project_dir.join("start_backend.py");
                let python_executable = find_python_executable(&project_dir);

                if backend_script.exists() {
                    let project_dir_clone = project_dir.clone();
                    let python_executable_clone = python_executable.clone();
                    thread::spawn(move || {
                        if let Some(python) = python_executable_clone {
                            let mut command = Command::new(&python);
                            command
                                .arg(&backend_script)
                                .current_dir(&project_dir_clone)
                                .stdout(Stdio::null())
                                .stderr(Stdio::null());

                            #[cfg(windows)]
                            {
                                use std::os::windows::process::CommandExt;
                                const CREATE_NO_WINDOW: u32 = 0x0800_0000;
                                command.creation_flags(CREATE_NO_WINDOW);
                            }

                            let _ = command.spawn();
                        }
                    });

                    if wait_for_backend("127.0.0.1", 8000, 30) {
                        println!("Backend is ready at http://127.0.0.1:8000");
                    } else {
                        eprintln!("Backend server did not respond in time.");
                    }
                }
            } else {
                eprintln!("Could not locate project root directory for backend process.");
            }

            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|_app_handle, _event| {});
}
```

---

### Step 8 — Option B only: Automated Build Pipeline Script (`build_desktop.ps1`)

> This script builds the **Tauri** MSI. It does **not** run PyInstaller and will not create `MyNewApp_Launcher.exe`.

Create `build_desktop.ps1` in the project root directory:

```powershell
$ErrorActionPreference = 'Stop'

function Write-Step {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Ensure-Tool {
    param([string]$Name, [string]$DownloadUrl, [string]$InstallHint)
    if (Test-Command $Name) {
        Write-Host "[OK] $Name is available" -ForegroundColor Green
        return
    }
    Write-Host "[MISSING] $Name was not found on PATH." -ForegroundColor Yellow
    Write-Host "Download: $DownloadUrl" -ForegroundColor Yellow
    Write-Host "Install hint: $InstallHint" -ForegroundColor Yellow
    throw "Missing required tool: $Name"
}

$projectRoot = $PSScriptRoot
$desktopDir = Join-Path $projectRoot 'desktop/MyNewAppShell'
$msiOutputDir = Join-Path $desktopDir 'src-tauri/target/release/bundle/msi'

Write-Step 'Checking prerequisites'
Ensure-Tool -Name 'python' -DownloadUrl 'https://www.python.org/downloads/' -InstallHint 'Install Python 3.11/3.12'
Ensure-Tool -Name 'node' -DownloadUrl 'https://nodejs.org/' -InstallHint 'Install Node.js LTS'
Ensure-Tool -Name 'npm' -DownloadUrl 'https://nodejs.org/' -InstallHint 'Install Node.js LTS'
Ensure-Tool -Name 'cargo' -DownloadUrl 'https://rustup.rs/' -InstallHint 'Install Rust via rustup'

Write-Step 'Checking project structure'
if (-not (Test-Path "$projectRoot\manage.py")) { throw "manage.py missing in $projectRoot" }
if (-not (Test-Path "$projectRoot\start_backend.py")) { throw "start_backend.py missing in $projectRoot" }

Write-Step 'Collecting Django static files'
Set-Location $projectRoot
if (Test-Path '.\venv\Scripts\python.exe') {
    .\venv\Scripts\python.exe .\manage.py collectstatic --noinput
} else {
    Write-Warning 'Virtual environment not found; static file collection skipped.'
}

Write-Step 'Installing Tauri desktop shell dependencies'
Set-Location $desktopDir
npm install

Write-Step 'Building Tauri desktop MSI installer'
npm run tauri build -- --bundles msi

Write-Step 'Build Complete'
if (Test-Path $msiOutputDir) {
    Get-ChildItem -Path $msiOutputDir -File | Select-Object Name, FullName | Format-Table -AutoSize
} else {
    throw "Installer directory not found: $msiOutputDir"
}
```

---

## 4. End-to-End Verification Checklist

### 1. Local Development Verification (both options)
1. Start MySQL server and verify database credentials in `.env`.
2. Activate virtual environment and run migrations:
   ```powershell
   .\venv\Scripts\activate
   python manage.py migrate
   ```
3. Test production WSGI server manually (use **your** project package name, e.g. `standard_soft` or `fcs_project`):
   ```powershell
   waitress-serve --host=127.0.0.1 --port=8000 standard_soft.wsgi:application
   ```
   Open `http://127.0.0.1:8000` in your web browser.

### 2. Option A — PyInstaller launcher verification
```powershell
pyinstaller --onefile --noconsole --name="MyNewApp_Launcher" launcher.py
.\dist\MyNewApp_Launcher.exe
```
Expect: Django comes up on port 8000, Edge opens in `--app=` mode.  
This is **not** the Tauri installer.

### 3. Option B — Tauri verification & production build
Dev mode:
```powershell
cd desktop/MyNewAppShell
npm run tauri dev
```

Production build from project root:
```powershell
.\build_desktop.ps1
```

Tauri outputs (not the PyInstaller file):
```text
desktop/MyNewAppShell/src-tauri/target/release/bundle/msi/     # Windows MSI installer
desktop/MyNewAppShell/src-tauri/target/release/bundle/nsis/    # optional NSIS/EXE installer (if enabled)
```

### 4. Deploying to Target Client PCs

**If Option A (PyInstaller):**
1. Copy the full project (including `venv`, or recreate venv + `pip install -r requirements.txt` on the PC).
2. Install MySQL and create the DB; set `.env`.
3. Ensure Microsoft Edge is installed.
4. Run `dist\MyNewApp_Launcher.exe` (or `python launcher.py`).

**If Option B (Tauri):**
1. Install MySQL 8.x and create the application database.
2. Run the compiled Tauri `.msi` / NSIS installer (not `MyNewApp_Launcher.exe`).
3. Configure `.env` in the installed resources directory if DB credentials differ.
4. Launch via Desktop / Start Menu shortcut.
