# Web Based Application Launcher Guide

This document provides instructions for using, building, and troubleshooting the launcher for the **TESLEAD HMI** application.

---

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

The application can be compiled into a single executable file using **PyInstaller**. 

### Prerequisites
Before building, ensure you have PyInstaller installed in your environment:
```powershell
pip install pyinstaller
```

### Build Commands
Run these commands from the project root directory.

*   **Production Version (No Console):**
    Use this for the final release. No terminal window will appear.
    ```powershell
    pyinstaller --onefile --noconsole --icon=teslead.ico --name="TESLEAD_HMI_MAIN" launcher.py
    ```

*   **Debug Version (With Console):**
    Use this if you need to see logs or troubleshoot startup issues.
    ```powershell
    pyinstaller --onefile --console --icon=teslead.ico --name="TESLEAD_HMI_DEBUG" launcher.py
    ```

### Output Location
After the build completes, your `.exe` file will be located in the `dist/` folder:
- `dist/TESLEAD_HMI_MAIN.exe`
- `dist/TESLEAD_HMI_DEBUG.exe`

> [!NOTE]
> Ensure `teslead.ico` is present in the root directory before running the build commands.

---

## 3. Launcher Logic Details

The `launcher.py` script performs the following steps:
1.  **Starts the Django Server:** Runs `manage.py runserver` in the background.
2.  **Process Management:** (Production version) Automatically kills any existing processes on port 8000 to avoid conflicts.
3.  **Wait Period:** Waits for 5 seconds to ensure the server is fully initialized.
4.  **Launches Browser:** Opens Microsoft Edge in **App Mode** pointing to `127.0.0.1:8000`.

---

## 4. Troubleshooting

- **Server Not Starting:** Ensure your virtual environment is active or the `python_path` in `launcher.py` is correct.
- **Port Conflict:** If the app fails to start, check if another application is using port 8000.
- **Missing Icon:** If PyInstaller errors out about `teslead.ico`, make sure the file exists or remove the `--icon` flag.
- **Browser Not Found:** Verify the path to `msedge.exe` in `launcher.py` matches your system installation.
