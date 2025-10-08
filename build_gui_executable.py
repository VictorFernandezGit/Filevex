#!/usr/bin/env python3
"""
Build a standalone Windows GUI executable
"""

import subprocess
import sys
import os
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing PyInstaller: {e}")
            return False


def create_gui_executable():
    """Create a standalone GUI executable."""
    
    if not install_pyinstaller():
        return False
    
    current_dir = Path.cwd()
    gui_script = current_dir / "file_traverser_gui_standalone.py"
    
    if not gui_script.exists():
        print(f"✗ Error: {gui_script} not found!")
        return False
    
    print(f"Creating standalone GUI executable from: {gui_script}")
    
    # PyInstaller command for GUI executable
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (GUI only)
        "--name=FileTraverserGUI",      # Name of the executable
        "--distpath=dist_gui",          # Output directory
        "--clean",                      # Clean cache before building
        "--noconfirm",                  # Don't ask for confirmation
        "--add-data=icon.ico:." if Path("icon.ico").exists() else "",  # Add icon if exists
        str(gui_script)
    ]
    
    # Remove empty strings from command
    cmd = [arg for arg in cmd if arg]
    
    try:
        print("Building standalone GUI executable...")
        print(f"Command: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        
        exe_path = current_dir / "dist_gui" / "FileTraverserGUI.exe"
        
        if exe_path.exists():
            print("\n" + "="*60)
            print("🎉 SUCCESS! Standalone GUI executable created!")
            print("="*60)
            print(f"📁 Location: {exe_path}")
            print(f"📏 Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            print("\n✅ This executable:")
            print("   • Works on ANY Windows computer")
            print("   • Does NOT require Python installation")
            print("   • Has a beautiful GUI interface")
            print("   • Includes folder selection dialogs")
            print("   • Shows real-time progress and logs")
            print("   • Can be copied to USB drive and run anywhere")
            print("\n📋 Usage:")
            print("   Just double-click FileTraverserGUI.exe to open the application!")
            print("   No command line needed - everything is graphical!")
            
            return True
        else:
            print("✗ GUI executable was not created successfully")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Error creating GUI executable: {e}")
        return False


def create_icon():
    """Create a simple icon file for the application."""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a folder icon
        draw.rectangle([8, 16, 56, 48], fill=(100, 150, 200), outline=(50, 100, 150), width=2)
        draw.rectangle([8, 8, 20, 16], fill=(100, 150, 200), outline=(50, 100, 150), width=2)
        
        # Save as ICO
        img.save("icon.ico", format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
        print("✓ Created application icon")
        return True
        
    except ImportError:
        print("⚠️  PIL not available, skipping icon creation")
        return False
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return False


def create_installer_script():
    """Create a simple installer script for the GUI executable."""
    
    installer_content = '''@echo off
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
set "desktop=%USERPROFILE%\\Desktop"
set "shortcut=%desktop%\\File Traverser GUI.lnk"

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%CD%\\FileTraverserGUI.exe'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'File Traverser GUI'; $Shortcut.Save()"

echo.
echo ✅ Installation completed!
echo ✅ Desktop shortcut created!
echo.
echo You can now run File Traverser GUI from your desktop or by double-clicking the .exe file.
echo.
pause
'''
    
    installer_path = Path("Install_GUI.bat")
    installer_path.write_text(installer_content)
    
    print(f"✓ Created installer script: {installer_path}")
    return installer_path


def create_readme():
    """Create a README file for the GUI application."""
    
    readme_content = '''# File Traverser GUI

A beautiful, easy-to-use graphical application for copying files from folders and subfolders.

## Features

- 🖥️ **Beautiful GUI Interface** - No command line needed
- 📁 **Folder Selection Dialogs** - Easy browsing for source and destination folders
- ⚙️ **Flexible Options** - Choose how files are copied
- 📊 **Real-time Progress** - See what's happening as files are copied
- 📋 **Detailed Logging** - Complete log of all operations
- 🚀 **Standalone Executable** - No Python installation required

## How to Use

1. **Double-click** `FileTraverserGUI.exe` to start the application
2. **Select Source Folder** - Click "Browse" to choose the folder containing files you want to copy
3. **Select Destination Folder** - Click "Browse" to choose where you want the files copied
4. **Choose Options**:
   - **Preserve directory structure**: Keep the original folder structure
   - **Overwrite existing files**: Replace files that already exist
   - **Show detailed output**: See information about each file being copied
5. **Click "Start Copying"** - The application will copy all files and show progress

## Options Explained

### Preserve Directory Structure
- **Checked**: Files keep their original folder structure in the destination
- **Unchecked**: All files are copied directly to the destination folder (flattened)

### Overwrite Existing Files
- **Checked**: Files that already exist in the destination will be replaced
- **Unchecked**: Existing files will be skipped (new files get numbered names like file_1.txt)

### Show Detailed Output
- **Checked**: See information about each file being copied
- **Unchecked**: Only see summary information

## Examples

### Copy All Files to One Folder
1. Select source folder (e.g., C:\\Documents\\Project)
2. Select destination folder (e.g., C:\\Backup)
3. Uncheck "Preserve directory structure"
4. Click "Start Copying"
Result: All files from Project and its subfolders will be copied directly to Backup

### Keep Folder Structure
1. Select source folder (e.g., C:\\Documents\\Project)
2. Select destination folder (e.g., C:\\Backup)
3. Check "Preserve directory structure"
4. Click "Start Copying"
Result: The folder structure will be maintained in the backup

## System Requirements

- Windows 7, 8, 10, or 11
- No additional software required
- No Python installation needed

## Troubleshooting

- **Application won't start**: Make sure you're running it on Windows
- **Can't select folders**: Make sure the folders exist and you have permission to access them
- **Files not copying**: Check that you have write permission to the destination folder

## Support

This is a standalone application that works on any Windows computer without requiring additional software installation.
'''
    
    readme_path = Path("README_GUI.txt")
    readme_path.write_text(readme_content)
    
    print(f"✓ Created README: {readme_path}")
    return readme_path


def create_complete_package():
    """Create a complete package with the GUI executable and all supporting files."""
    
    import zipfile
    
    # Files to include in the package
    files_to_include = []
    
    # Add the executable if it exists
    exe_path = Path("dist_gui/FileTraverserGUI.exe")
    if exe_path.exists():
        files_to_include.append(("dist_gui/FileTraverserGUI.exe", "FileTraverserGUI.exe"))
    
    # Add supporting files
    supporting_files = [
        "Install_GUI.bat",
        "README_GUI.txt"
    ]
    
    for file_name in supporting_files:
        file_path = Path(file_name)
        if file_path.exists():
            files_to_include.append((str(file_path), file_path.name))
    
    if not files_to_include:
        print("⚠️  No files to package")
        return None
    
    zip_path = Path("FileTraverser_GUI_Complete.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for source_path, archive_name in files_to_include:
            zipf.write(source_path, archive_name)
            print(f"✓ Added {archive_name} to package")
    
    print(f"\n✓ Created complete GUI package: {zip_path}")
    return zip_path


def main():
    """Main function to build the GUI executable."""
    print("🔧 Building Standalone GUI Executable")
    print("=" * 50)
    
    # Create icon
    print("Creating application icon...")
    create_icon()
    
    # Create GUI executable
    print("\nCreating GUI executable...")
    success = create_gui_executable()
    
    if success:
        print("\nCreating supporting files...")
        create_installer_script()
        create_readme()
        
        print("\nCreating complete package...")
        create_complete_package()
        
        print("\n" + "="*60)
        print("🎉 GUI Application Build Complete!")
        print("="*60)
        print("\n📁 Files created:")
        print("   • FileTraverserGUI.exe - Standalone GUI application")
        print("   • Install_GUI.bat - Installation script")
        print("   • README_GUI.txt - User instructions")
        print("   • FileTraverser_GUI_Complete.zip - Complete package")
        
        print("\n📋 For Windows users:")
        print("1. Copy FileTraverserGUI.exe to any Windows computer")
        print("2. Double-click to run - no installation needed!")
        print("3. Or use the complete package for easy distribution")
        
        print("\n💡 The GUI application includes:")
        print("   • Beautiful interface with folder selection dialogs")
        print("   • Real-time progress and logging")
        print("   • All the features of the command-line version")
        print("   • No Python installation required")
        
    else:
        print("\n❌ Failed to create GUI executable")


if __name__ == "__main__":
    main()
