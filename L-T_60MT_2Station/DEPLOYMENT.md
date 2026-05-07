# L&T 60MT 2Station - Deployment Guide

This guide explains how to install and set up the L&T Valve Testing Software on a new Windows machine.

## 🏗️ Architecture Overview
The application is built using:
- **Tauri**: Desktop interface (Windows EXE)
- **Django**: Backend logic
- **Waitress**: Production-grade web server
- **MySQL**: Local database

---

## 📋 Prerequisites
Before installing the software, ensure the target machine has:
1. **Operating System**: Windows 10 or 11 (64-bit).
2. **Database**: MySQL Community Server 8.x installed.
   - [Download MySQL](https://dev.mysql.com/downloads/mysql/)

---

## 🚀 Installation Steps

### 1. Install the Software
1. Locate the `l-t-60mt-2station_0.1.0_x64_en-US.msi` (or the setup EXE).
2. Double-click to run the installer.
3. Follow the on-screen instructions. The app will be installed to `C:\Program Files\l-t-60mt-2station\`.

### 2. Configure the Database
The software requires a MySQL database to function. Run the following commands in your **MySQL Workbench** or **MySQL Shell**:

```sql
-- 1. Create the database
CREATE DATABASE `landt60mt-2station`;

-- 2. Create the application user (matches the software config)
CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root';

-- 3. Grant permissions
GRANT ALL PRIVILEGES ON `landt60mt-2station`.* TO 'root'@'127.0.0.1';

-- 4. Apply changes
FLUSH PRIVILEGES;
```

> [!NOTE]
> If you wish to use a different password or user, you must update the `.env` file inside the installation folder's `resources` directory.

---

## 💻 Running the Application
1. Double-click the **l-t-60mt-2station** icon on your Desktop.
2. You will see a "Loading L&T Backend..." screen for a few seconds.
3. Once the database connection is established, the main interface will open automatically.

---

## 🔍 Troubleshooting

### "Backend Error" Popup
If you see a popup saying "Failed to start Django backend":
- Ensure no other application is using **Port 8000**.
- Check if the `venv` folder exists in the installation path.

### White Screen or "Asset not found"
- This usually means the backend is taking too long to start. Try closing the app and opening it again.
- Ensure **MySQL Service** is running in Windows Services (`services.msc`).

---

## 🛠️ Maintenance
The application logs errors internally. If you encounter persistent issues, please contact the development team with the error message displayed in the popup.
