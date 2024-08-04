@echo off
setlocal EnableDelayedExpansion

echo Checking if Python 3.11.2 is already installed...
python --version 2>nul | findstr /r "^Python 3\.11\." >nul
if %errorlevel% equ 0 (
    echo Python 3.11 is already installed.
    set "PYTHON_PATH=python"
) else (
    echo Python 3.11 is not installed. Proceeding with download and installation...

    REM Download Python 3.11.2 installer
    echo Downloading Python 3.11.2 installer...
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe', 'python-3.11.2-amd64.exe')"

    echo Installing Python 3.11.2...
    start /wait python-3.11.2-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo Cleaning up Python installer...
    del python-3.11.2-amd64.exe

    set "PYTHON_PATH=%ProgramFiles%\Python311\python.exe"
)

echo Using Python at: "!PYTHON_PATH!"

REM Download repository as ZIP file
echo Downloading the repository...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/bytewired9/dirtydubs/archive/refs/heads/main.zip', 'dirtydubs.zip')"

REM Extract the ZIP file
echo Extracting the repository...
powershell -Command "Expand-Archive -Path dirtydubs.zip -DestinationPath . -Force"

REM Rename extracted folder to dirtydubs
echo Renaming the extracted folder...
if exist dirtydubs-main (
    rename dirtydubs-main dirtydubs
) else (
    echo The extracted folder "dirtydubs-main" does not exist.
    exit /b 1
)

REM Clean up downloaded ZIP file
echo Cleaning up downloaded ZIP file...
del dirtydubs.zip

REM Change to the dirtydubs directory
echo Changing to the dirtydubs directory...
cd /d "%~dp0dirtydubs"
echo Current directory: %cd%

REM Install requirements from the repo
echo Installing requirements from requirements.txt...
if exist requirements.txt (
    echo Found requirements.txt in %cd%
    "!PYTHON_PATH!" -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install requirements.
        exit /b 1
    )
) else (
    echo requirements.txt not found in the directory.
    exit /b 1
)

REM Prompt user for store ID
set /p STORE_ID=Please enter your store number:

REM Create config.ini file with provided content
echo Creating config.ini file...
(
    echo # Store ID: The store number of your BWW
    echo [store_id]
    echo id = %STORE_ID%
    echo.
    echo # Order types: you can specify multiple types separated by spaces
    echo [order]
    echo type_of_order = call web app walkin
    echo.
    echo # Order reception modes: you can specify multiple modes separated by spaces
    echo order_reception = carryout delivery dinein
    echo.
    echo # Order times: you can specify multiple times separated by spaces
    echo order_time = breakfast lunch midday dinner latenight overnight
) > config.ini

echo Setup complete!
pause