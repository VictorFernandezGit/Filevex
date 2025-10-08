@echo off
echo ================================================
echo File Traverser GUI - Installation
echo ================================================
echo.

REM Check if the executable exists
if not exist "FileTraverserGUI.exe" (
    echo ERROR: FileTraverserGUI.exe not found!
    echo Make sure this script is in the same folder as the executable.
    pause
    exit /b 1
)

echo File Traverser GUI is ready to use!
echo.
echo To use:
echo 1. Double-click FileTraverserGUI.exe
echo 2. Select your source and destination folders
echo 3. Choose your options
echo 4. Click "Start Copying"
echo.

REM Create desktop shortcut
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\File Traverser GUI.lnk"

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%CD%\FileTraverserGUI.exe'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'File Traverser GUI'; $Shortcut.Save()"

echo.
echo ✅ Installation completed!
echo ✅ Desktop shortcut created!
echo.
echo You can now run File Traverser GUI from your desktop or by double-clicking the .exe file.
echo.
pause
