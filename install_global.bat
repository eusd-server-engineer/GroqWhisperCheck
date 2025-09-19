@echo off
echo Installing gq command globally...
echo.

REM Create a clean virtual environment for global install
echo Creating isolated environment...
python -m venv %TEMP%\gq_install_env

REM Activate and install
echo Installing gq...
call %TEMP%\gq_install_env\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install . >nul 2>&1

REM Copy the executable to Python Scripts (in PATH)
echo Copying to global Scripts directory...
copy %TEMP%\gq_install_env\Scripts\gq.exe %LOCALAPPDATA%\Programs\Python\Python312\Scripts\ >nul 2>&1
copy %TEMP%\gq_install_env\Scripts\groqchat.exe %LOCALAPPDATA%\Programs\Python\Python312\Scripts\ >nul 2>&1
copy %TEMP%\gq_install_env\Scripts\groq-cli.exe %LOCALAPPDATA%\Programs\Python\Python312\Scripts\ >nul 2>&1

REM Clean up
deactivate
rmdir /s /q %TEMP%\gq_install_env >nul 2>&1

echo.
echo Installation complete!
echo You can now use 'gq' from anywhere.
echo.
echo Test it:
echo   gq -q "Hello world"
echo.