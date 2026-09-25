# Web Based Application Launcher Guide

This document provides instructions for using and building the launcher for the **TESLEAD HMI** application.

## 1. Browser Launch Modes

You can run the application in various modes using different browsers. These commands can be used in shortcuts or the terminal.

### Google Chrome
*   **Full Screen (Kiosk Mode):**
    ```powershell
    & "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk http://127.0.0.1:8000
    ```
*   **App Mode (Standalone Window):**
    ```powershell
    & "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8000
    ```

### Microsoft Edge 👍
*   **Full Screen (Kiosk Mode):**
    ```powershell
    & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --kiosk http://127.0.0.1:8000 --edge-kiosk-type=fullscreen
    ```
*   **App Mode (Standalone Window):**
    ```powershell
    & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=http://127.0.0.1:8000
    ```

---

## 2. Building the Executable (.exe)

The application can be compiled into a single executable file using **PyInstaller**. Use the following commands depending on whether you need a console window for debugging.

### Production Version (No Console)
Use this command to create a clean, app-like experience without a background terminal window.
```powershell
pyinstaller --onefile --noconsole --icon=teslead.ico --name="TESLEAD_HMI_MAIN" launcher.py
```

### Debug Version (With Console)
Use this command if you need to see logs or troubleshoot startup issues.
```powershell
pyinstaller --onefile --console --icon=teslead.ico --name="TESLEAD_HMI_DEBUG" launcher.py
```

---

## 3. Launcher Logic Details

The launcher performs the following steps:
1.  **Starts the Django Server:** Runs `python manage.py runserver` in the background.
2.  **Wait Period:** Waits for 5 seconds to ensure the server is up.
3.  **Launches Browser:** Opens the default browser (Edge) in App mode pointing to `127.0.0.1:8000`.
