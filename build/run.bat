@echo off
setlocal

REM Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    REM Replace the URL with the latest Python installer URL
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.x.x/python-3.x.x-amd64.exe' -ArgumentList '/silent InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait"
    if %errorlevel% neq 0 (
        echo Failed to install Python. Exiting.
        exit /b 1
    )
) else (
    echo Python is already installed.
)

REM Verify Python version
python --version
if %errorlevel% neq 0 (
    echo Failed to verify Python installation. Exiting.
    exit /b 1
)

REM Set up the virtual environment if needed
if not exist ".venv" (
    python -m venv .venv
    call .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM Run the GUI script
REM The following command assumes that 'gui.py' is in the same directory as the .bat file
REM and that the virtual environment is activated
start "" /B python gui.py

REM To ensure the script finishes before closing the window, remove the 'start' command if not needed
REM To hide the command window, use:
REM pythonw gui.py

endlocal
