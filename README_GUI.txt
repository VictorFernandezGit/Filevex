# File Traverser GUI

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
1. Select source folder (e.g., C:\Documents\Project)
2. Select destination folder (e.g., C:\Backup)
3. Uncheck "Preserve directory structure"
4. Click "Start Copying"
Result: All files from Project and its subfolders will be copied directly to Backup

### Keep Folder Structure
1. Select source folder (e.g., C:\Documents\Project)
2. Select destination folder (e.g., C:\Backup)
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
