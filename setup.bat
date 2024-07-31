@echo off
SETLOCAL

:: Set the Python version and download URL
SET PYTHON_VERSION=3.11.2
SET PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
SET DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%
SET PYTHON_PATH=C:\Python%PYTHON_VERSION%\python.exe
SET PIP_PATH=C:\Python%PYTHON_VERSION%\Scripts\pip.exe

:: Download Python installer
echo Downloading Python %PYTHON_VERSION%...
powershell -Command "Invoke-WebRequest -Uri %DOWNLOAD_URL% -OutFile %PYTHON_INSTALLER%"

:: Install Python
echo Installing Python %PYTHON_VERSION%...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 TargetDir=C:\Python%PYTHON_VERSION% PrependPath=1

:: Verify Python installation
echo Verifying Python installation...
%PYTHON_PATH% --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python installation failed.
    EXIT /B 1
)

:: Upgrade pip
echo Upgrading pip...
%PYTHON_PATH% -m pip install --upgrade pip

:: Install requirements from requirements.txt
echo Installing requirements from requirements.txt...
%PYTHON_PATH% -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements.
    EXIT /B 1
)

:: Clean up
echo Cleaning up...
DEL %PYTHON_INSTALLER%

echo Installation completed successfully.
ENDLOCAL
pause
