# Tauri + Django + MySQL Desktop Application Setup Guide

## Overview

This guide explains how to convert an existing Django + MySQL web application into a native Windows desktop application using:

* Tauri
* Django
* Waitress
* MySQL

Final architecture:

```text
Desktop EXE
    ↓
Tauri Desktop Window
    ↓
Local Django Server (Waitress)
    ↓
MySQL Database
```

---

# Existing Project Architecture

Current project already contains:

* Django frontend templates
* Django backend APIs
* Static JS/CSS assets
* MySQL database integration
* Service-layer architecture
* Modular Django app structure

No frontend rewrite is required.

---

# Recommended Stack

| Layer             | Technology  |
| ----------------- | ----------- |
| Desktop Shell     | Tauri       |
| Backend           | Django      |
| Database          | MySQL       |
| Production Server | Waitress    |
| Packaging         | Tauri Build |

---

# Step 1 — Install Required Software

## Install Rust

Download and install:

[https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

Verify installation:

```bash
rustc --version
cargo --version
```

---

## Install Node.js

Download:

[https://nodejs.org](https://nodejs.org)

Verify:

```bash
node -v
npm -v
```

---

## Install Visual Studio Build Tools

Download:

[https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Select workload:

* Desktop development with C++

Required components:

* MSVC Build Tools for x64/x86
* C++ CMake tools for Windows
* Windows 11 SDK

---

# Step 2 — Create Tauri Project

Inside project root:

```bash
mkdir desktop
cd desktop
```

Run:

```bash
npm create tauri-app@latest
```

Use these selections:

| Option          | Value             |
| --------------- | ----------------- |
| Project Name    | L-T-60MT-2Station |
| Package Manager | npm               |
| UI Template     | Vanilla           |
| UI Flavor       | JavaScript        |

---

# Step 3 — Install Dependencies

Go into generated Tauri project:

```bash
cd L-T-60MT-2Station
```

Install dependencies:

```bash
npm install
```

---

# Step 4 — Configure Tauri To Open Django

Open:

```text
src-tauri/tauri.conf.json
```

Update build section:

```json
"build": {
  "beforeDevCommand": "",
  "beforeBuildCommand": "",
  "devUrl": "http://127.0.0.1:8000"
}
```

---

# Step 5 — Install Waitress

Activate virtual environment:

```bash
.\venv\Scripts\activate
```

Install Waitress:

```bash
pip install waitress
```

---

# Step 6 — Configure Django For MySQL

Install MySQL driver:

```bash
pip install mysqlclient
```

If mysqlclient fails on Windows:

```bash
pip install PyMySQL
```

Then inside Django project's `__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

# Step 7 — Configure Database Settings

Inside:

```text
settings.py
```

Configure:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "lnt_db",
        "USER": "root",
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Recommended:

* Use dedicated MySQL user
* Do not use root in production

---

# Step 8 — Start Django Using Waitress

DO NOT use:

```bash
python manage.py runserver
```

Use:

```bash
waitress-serve --host=127.0.0.1 --port=8000 standard_soft.wsgi:application
```

Verify:

```text
http://127.0.0.1:8000
```

---

# Step 9 — Run Tauri Desktop App

Inside Tauri project:

```bash
npm run tauri dev
```

Expected result:

* Native desktop window opens
* Existing Django application loads
* Desktop application works locally

---

# Step 10 — Auto Start Django Backend

Create file:

```text
start_backend.py
```

Example:

```python
import subprocess

subprocess.Popen([
    "waitress-serve",
    "--host=127.0.0.1",
    "--port=8000",
    "standard_soft.wsgi:application"
])
```

---

# Step 11 — Install Tauri Shell Plugin

Inside Tauri project:

```bash
npm run tauri add shell
```

---

# Step 12 — Launch Backend Automatically

Inside Tauri startup code:

```javascript
import { Command } from '@tauri-apps/plugin-shell';

const command = Command.create('python', [
  '../start_backend.py'
]);

command.spawn();
```

Behavior:

* User opens desktop app
* Django backend starts automatically
* Tauri loads local Django application

---

# Step 13 — Build Production EXE

Build application:

```bash
npm run tauri build
```

Generated files:

```text
src-tauri/target/release/bundle/msi/
```

Outputs:

* .exe
* .msi installer

---

# Production Deployment Requirements

Each target system requires:

| Component      | Required |
| -------------- | -------- |
| MySQL Server   | Yes      |
| Python Runtime | Yes      |
| Desktop EXE    | Yes      |
| Django Project | Yes      |

---

# Recommended Security Settings

## Use localhost only

Use:

```text
127.0.0.1
```

Avoid:

```text
0.0.0.0
```

---

## Disable Django Debug

Inside `settings.py`:

```python
DEBUG = False
```

---

## Use Environment Variables

Do not hardcode:

* Database passwords
* API keys
* SAP credentials
* Secret keys

---

# Recommended MySQL User Setup

Example:

```sql
CREATE USER 'lnt_user'@'localhost' IDENTIFIED BY 'StrongPassword';

GRANT ALL PRIVILEGES ON lnt_db.* TO 'lnt_user'@'localhost';

FLUSH PRIVILEGES;
```

---

# Final Architecture

```text
Desktop EXE
      ↓
Tauri
      ↓
Waitress Server
      ↓
Django
      ↓
MySQL
```

---

# Future Improvements

Recommended future enhancements:

* Embedded Python runtime
* Embedded MySQL
* Single-click installer
* Auto updates
* Printer integration
* USB/Serial device support
* Offline sync
* Kiosk mode
* Local database backup automation
* Windows service support

---

# Recommended Production Workflow

1. User installs MSI
2. User opens desktop application
3. Waitress starts Django automatically
4. Django connects MySQL locally
5. Application opens instantly

Result:

Full offline industrial desktop application using existing Django architecture.
