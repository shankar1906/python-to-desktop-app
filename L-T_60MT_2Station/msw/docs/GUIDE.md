# L&T 60MT 2Station — Full Windows Application Guide

This guide explains how to **build**, **package**, and **test** the L&T Valve Testing Software as a **Windows desktop application**, and how to install it on **other Windows machines**.

---

## 1. What This Application Is

| Layer | Technology | Role |
| ----- | ---------- | ---- |
| Desktop shell | Tauri | Native Windows window (EXE / MSI) |
| Backend | Django | Business logic, UI templates, APIs |
| Server | Waitress | Serves Django on `127.0.0.1:8000` |
| Database | MySQL 8 | Local data storage |

### Runtime flow

```text
User double-clicks desktop icon
        ↓
Tauri Windows EXE starts
        ↓
Bundled Waitress starts Django (venv\Scripts\waitress-serve.exe)
        ↓
App waits until http://127.0.0.1:8000 is ready
        ↓
Tauri window loads the Django UI
        ↓
Django talks to local MySQL
```

### Project folders that matter

```text
L-T_60MT_2Station/
├── standard_app/          # Django app (views, templates, services)
├── standard_soft/         # Django project settings / WSGI
├── manage.py
├── requirements.txt
├── .env                   # DB credentials (required; create on Windows)
├── venv/                  # Windows Python virtualenv (required for build)
├── start_backend.py
├── desktop/
│   └── L-T-60MT-2Station/ # Tauri desktop project
│       └── src-tauri/
│           ├── tauri.conf.json
│           └── src/lib.rs # Starts Waitress + opens UI
├── DEPLOYMENT.md          # Install steps for target PCs
├── Readme.md              # Setup / architecture notes
└── guide.md               # This document
```

---

## 2. Critical Rule — Build Only on Windows

| Goal | Where to do it |
| ---- | -------------- |
| Build MSI / EXE for customers | **Windows 10/11 only** |
| Test installer on other PCs | Other **Windows** machines |
| Edit Django code | Windows or Linux (optional) |
| Use Wine on Ubuntu | **Not recommended** for real packaging / QA |

Why:

- Tauri Windows builds need **Visual Studio C++ Build Tools**
- The app starts `venv\Scripts\waitress-serve.exe` (Windows paths)
- The bundled `venv` must be a **Windows** virtual environment

**Do not** try to produce the customer Windows installer from Ubuntu alone.  
Use a real Windows PC, or a **Windows VM** on Ubuntu (VirtualBox / VMware).

---

## 3. What You Need

### A. Build machine (Windows 10/11 64-bit)

Install all of the following:

| Software | Purpose | Download |
| -------- | ------- | -------- |
| Python 3.11 or 3.12 (64-bit) | Create Windows `venv` | https://www.python.org/downloads/ |
| MySQL Community Server 8.x | Database while building/testing | https://dev.mysql.com/downloads/mysql/ |
| Node.js LTS | Tauri / npm | https://nodejs.org |
| Rust (rustup) | Tauri backend compile | https://rustup.rs |
| Visual Studio Build Tools | MSVC + Windows SDK | https://visualstudio.microsoft.com/visual-cpp-build-tools/ |

**Visual Studio Build Tools workload**

- Select: **Desktop development with C++**
- Include: MSVC x64/x86, CMake tools, Windows 10/11 SDK

**Verify tools**

```powershell
python --version
node -v
npm -v
rustc --version
cargo --version
mysql --version
```

### B. Target / test machines (other Windows PCs)

Each PC that will run the installed app needs:

1. Windows 10 or 11 (64-bit)
2. MySQL Server 8.x installed and running
3. Your built MSI or NSIS EXE installer
4. Network/USB access to copy the installer + optional SQL dump

---

## 4. Prepare the Project on the Windows Build Machine

### Step 1 — Copy the project

Copy the full `L-T_60MT_2Station` folder to Windows, for example:

```text
C:\work\L-T_60MT_2Station
```

Or clone from git onto that machine.

### Step 2 — Create `.env` in the project root

Create file:

```text
C:\work\L-T_60MT_2Station\.env
```

Example content (match your MySQL setup):

```env
NAME=landt60mt-2station
USER=root
PASSWORD=root
HOST=127.0.0.1
PORT=3306
```

These keys match `standard_soft/settings.py`:

- `NAME`
- `USER`
- `PASSWORD`
- `HOST`
- `PORT`

### Step 3 — Create Windows Python virtual environment

Open **PowerShell** or **Command Prompt**:

```powershell
cd C:\work\L-T_60MT_2Station

python -m venv venv
.\venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install waitress whitenoise
```

If `mysqlclient` fails to install on Windows, use PyMySQL:

```powershell
pip install PyMySQL
```

Then ensure Django can use it (e.g. in `standard_soft/__init__.py`):

```python
import pymysql
pymysql.install_as_MySQLdb()
```

Confirm Waitress exists:

```powershell
dir .\venv\Scripts\waitress-serve.exe
```

This path is required by Tauri (`lib.rs`).

### Step 4 — Collect static files (recommended before packaging)

```powershell
.\venv\Scripts\activate
python manage.py collectstatic --noinput
```

`tauri.conf.json` bundles `staticfiles` when present.

---

## 5. Configure MySQL on the Build Machine

### Create database and user

In MySQL Workbench or MySQL Shell:

```sql
CREATE DATABASE `landt60mt-2station`;

CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root';

GRANT ALL PRIVILEGES ON `landt60mt-2station`.* TO 'root'@'127.0.0.1';

FLUSH PRIVILEGES;
```

Adjust user/password if your `.env` uses different values.

### Import existing data (optional)

If you have the dump file in the project:

```powershell
mysql -u root -p landt60mt-2station < dump-landt60mt-2station-202605070959.sql
```

### Ensure MySQL service is running

```powershell
# Check service
Get-Service -Name MySQL*

# Or start from Services (services.msc) → MySQL80 / MySQL
```

---

## 6. Test Backend Before Building the Desktop App

### Option A — Django development server

```powershell
cd C:\work\L-T_60MT_2Station
.\venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
```

### Option B — Waitress (same as packaged app)

```powershell
cd C:\work\L-T_60MT_2Station
.\venv\Scripts\activate
waitress-serve --host=127.0.0.1 --port=8000 standard_soft.wsgi:application
```

Open in browser:

```text
http://127.0.0.1:8000
```

Fix login / DB / static issues **before** running `tauri build`.

---

## 7. Run Desktop App in Dev Mode (optional)

```powershell
cd C:\work\L-T_60MT_2Station\desktop\L-T-60MT-2Station
npm install
npm run tauri dev
```

Expected:

- Native Tauri window opens
- Backend starts (or uses `devUrl` `http://127.0.0.1:8000`)
- Django UI loads inside the desktop window

If port 8000 is already in use by a manual server, stop that process first or keep only one listener.

---

## 8. Build the Windows Installer (Production)

### What gets bundled

From `desktop/L-T-60MT-2Station/src-tauri/tauri.conf.json`, the installer packages:

- `standard_soft`
- `standard_app`
- `staticfiles`
- `venv` (Windows virtualenv with Waitress)
- `.env`
- `manage.py`

### Build command

```powershell
cd C:\work\L-T_60MT_2Station\desktop\L-T-60MT-2Station
npm install
npm run tauri build
```

First build can take a long time (Rust compile).

### Output locations

After a successful build:

```text
desktop\L-T-60MT-2Station\src-tauri\target\release\bundle\msi\
desktop\L-T-60MT-2Station\src-tauri\target\release\bundle\nsis\
```

Typical files:

- `l-t-60mt-2station_0.1.0_x64_en-US.msi`
- NSIS setup `.exe` (if NSIS target is enabled)

**These MSI/EXE files are what you copy to other Windows PCs for testing.**

---

## 9. Install and Test on Other Windows Operating Systems

Use this checklist on **each** test PC (Windows 10, Windows 11, different machines, etc.).

### Step 1 — Install MySQL

1. Install MySQL Community Server 8.x
2. Start the MySQL Windows service
3. Create the database and user (same as Section 5)
4. Import the SQL dump if the site needs existing master data

### Step 2 — Install the application

1. Copy the MSI or setup EXE from the build machine
2. Run the installer
3. Default install location is typically under:

```text
C:\Program Files\l-t-60mt-2station\
```

### Step 3 — Match database settings

If the test PC MySQL password/user differs from the build machine:

1. Find `.env` inside the installation **resources** directory
2. Update `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`
3. Save and restart the app

### Step 4 — Launch

1. Double-click **l-t-60mt-2station** on the Desktop / Start Menu
2. You should see a short loading period while Waitress starts
3. The main Django UI opens in the Tauri window

### Step 5 — Smoke test checklist

On every Windows OS / machine, verify:

- [ ] App starts without “Backend Error”
- [ ] Login page loads
- [ ] Can log in with a known user
- [ ] Dashboard / station pages open
- [ ] MySQL data is readable
- [ ] Reports / PDF / Excel features you care about work
- [ ] Closing and reopening the app still works
- [ ] Port 8000 is free before start (no other Django instance)

---

## 10. What to Copy Between Machines

| Item | Copy to test PC? | Notes |
| ---- | ---------------- | ----- |
| MSI / NSIS EXE | **Yes** | Main deliverable |
| SQL dump | Recommended | For same data as production/dev |
| Full source + `venv` | No | Already inside installer resources |
| Ubuntu Wine build | No | Not a valid customer package |

Suggested USB / share layout:

```text
L-T_Release_0.1.0/
├── l-t-60mt-2station_0.1.0_x64_en-US.msi
├── dump-landt60mt-2station-YYYYMMDD.sql
└── INSTALL_NOTES.txt   (MySQL steps + default DB password)
```

---

## 11. How the Packaged App Starts Django

On launch, Tauri (`src-tauri/src/lib.rs`) does roughly:

1. Resolve the bundled resources folder
2. Run:

```text
venv\Scripts\waitress-serve.exe --host=127.0.0.1 --port=8000 standard_soft.wsgi:application
```

3. Wait up to ~20 seconds for port `8000`
4. Navigate the window to `http://127.0.0.1:8000`
5. If Waitress fails to start or respond → show **Backend Error** popup and exit

So a broken Windows `venv`, missing `.env`, or MySQL down will show up as a backend/startup failure.

---

## 12. Troubleshooting

### “Failed to start Django backend”

- Confirm `venv\Scripts\waitress-serve.exe` exists in packaged resources
- Rebuild after creating a proper **Windows** `venv` (not a Linux venv copied over)
- Ensure no antivirus is blocking the EXE

### Backend starts but port 8000 never responds

- Another app is using port 8000 — close it
- Wrong working directory / missing `standard_soft`
- Check Django can import (`settings.py`, missing packages in `venv`)

### White screen / blank window

- Backend slow to start — close app and reopen
- Confirm MySQL service is running
- Confirm `.env` points to `127.0.0.1` and correct DB name

### Login / database errors

- MySQL not installed or not running on that PC
- Wrong password in `.env`
- Database not created / dump not imported
- User not granted privileges for `127.0.0.1`

### Build fails on Windows (`tauri build`)

- Install Visual Studio Build Tools (C++ workload)
- Run `rustup update`
- Close other heavy processes; first compile needs disk + RAM
- Ensure WebView2 runtime is available (usually present on Win10/11)

### Built on Linux / Wine — app broken on real Windows

- Rebuild on a real Windows machine or Windows VM
- Recreate `venv` with Windows Python before packaging

---

## 13. Recommended Production Settings (before customer release)

In `standard_soft/settings.py` for release builds:

```python
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

Also:

- Use a dedicated MySQL user (not shared root passwords if possible)
- Keep secrets only in `.env`
- Bind Waitress to `127.0.0.1` only (already done)
- Version the MSI (`productName` / `version` in `tauri.conf.json`)

---

## 14. End-to-End Workflow Summary

```text
1. On Windows build PC:
   - Install Python, MySQL, Node, Rust, VS Build Tools
   - Create .env
   - Create Windows venv + install requirements + waitress
   - Import DB / verify http://127.0.0.1:8000
   - npm run tauri build
   - Collect MSI/EXE from target\release\bundle\

2. On each test Windows PC:
   - Install MySQL
   - Create DB + import dump
   - Install MSI/EXE
   - Adjust .env if needed
   - Launch app and run smoke tests

3. For official QA across OS versions:
   - Test Windows 10 and Windows 11 separately
   - Prefer clean PCs/VMs (no leftover port 8000 / old installs)
```

---

## 15. Related Documents

| File | Use when |
| ---- | -------- |
| `guide.md` | Full Windows build + multi-PC testing (this file) |
| `DEPLOYMENT.md` | Short install guide for a new Windows machine |
| `Readme.md` | Tauri + Django architecture and setup notes |
| `LAUNCHER_GUIDE.md` | Browser / PyInstaller launcher (alternate web launch path) |

---

## 16. Quick Commands Cheat Sheet

```powershell
# Activate venv
cd C:\work\L-T_60MT_2Station
.\venv\Scripts\activate

# Test with Waitress
waitress-serve --host=127.0.0.1 --port=8000 standard_soft.wsgi:application

# Desktop build
cd desktop\L-T-60MT-2Station
npm install
npm run tauri build

# Installer output
explorer .\src-tauri\target\release\bundle\msi
```

---

**Bottom line:** Build the Windows MSI/EXE on a Windows machine, then install that same package on every other Windows OS you want to test — with MySQL prepared on each target PC.