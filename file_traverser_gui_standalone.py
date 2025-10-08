#!/usr/bin/env python3
"""
Standalone GUI File Traverser Application
A complete GUI application for copying files from folders
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os
from pathlib import Path
import shutil


class FileTraverserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FileVex - Copy Files from Folders - Victor Fernandez")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Variables
        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.preserve_structure = tk.BooleanVar()
        self.overwrite = tk.BooleanVar()
        self.verbose = tk.BooleanVar(value=True)
        
        # Statistics
        self.copied_files = 0
        self.skipped_files = 0
        self.errors = 0
        
        self.setup_ui()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🗂️ File Traverser", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="Copy all files from folders and subfolders", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Source folder selection
        source_frame = ttk.LabelFrame(main_frame, text="📁 Source Folder", padding="10")
        source_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(source_frame, text="Select the folder to traverse:", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        source_entry_frame = ttk.Frame(source_frame)
        source_entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.source_entry = ttk.Entry(source_entry_frame, textvariable=self.source_var, 
                                     width=60, font=("Arial", 9))
        self.source_entry.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(source_entry_frame, text="Browse", command=self.browse_source,
                  style="Accent.TButton").grid(row=0, column=1)
        
        source_entry_frame.columnconfigure(0, weight=1)
        
        # Destination folder selection
        dest_frame = ttk.LabelFrame(main_frame, text="📂 Destination Folder", padding="10")
        dest_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(dest_frame, text="Select where to copy all files:", 
                 font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        dest_entry_frame = ttk.Frame(dest_frame)
        dest_entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.dest_entry = ttk.Entry(dest_entry_frame, textvariable=self.dest_var, 
                                   width=60, font=("Arial", 9))
        self.dest_entry.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(dest_entry_frame, text="Browse", command=self.browse_dest,
                  style="Accent.TButton").grid(row=0, column=1)
        
        dest_entry_frame.columnconfigure(0, weight=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="15")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(options_frame, text="📂 Preserve directory structure", 
                       variable=self.preserve_structure,
                       command=self.on_option_change).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_frame, text="🔄 Overwrite existing files", 
                       variable=self.overwrite,
                       command=self.on_option_change).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Checkbutton(options_frame, text="📝 Show detailed output", 
                       variable=self.verbose,
                       command=self.on_option_change).grid(row=2, column=0, sticky=tk.W, pady=5)


    
        
        # Info labels
        self.info_label = ttk.Label(options_frame, text="", font=("Arial", 9), foreground="blue")
        self.info_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Copying", 
                                      command=self.start_copy, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=10)
        
        ttk.Button(button_frame, text="🗑️ Clear Log", command=self.clear_log).grid(row=0, column=1, padx=10)
        
        ttk.Button(button_frame, text="❓ Help", command=self.show_help).grid(row=0, column=2, padx=10)
        
        # Current file display
        current_file_frame = ttk.LabelFrame(main_frame, text="📄 Current File", padding="10")
        current_file_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.current_file_var = tk.StringVar(value="Ready to start...")
        self.current_file_label = ttk.Label(current_file_frame, textvariable=self.current_file_var, 
                                           font=("Arial", 10), foreground="blue", wraplength=700)
        self.current_file_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="📋 Operation Log", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                 font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Initial info update
        self.on_option_change()
    
    def on_option_change(self):
        """Update info label when options change."""
        preserve = self.preserve_structure.get()
        overwrite = self.overwrite.get()
        
        if preserve and overwrite:
            info = "Files will be copied with original folder structure and existing files will be replaced."
        elif preserve:
            info = "Files will be copied with original folder structure. Existing files will be skipped."
        elif overwrite:
            info = "All files will be copied to the destination folder (flattened). Existing files will be replaced."
        else:
            info = "All files will be copied to the destination folder (flattened). Existing files will be skipped."
        
        self.info_label.config(text=info)
    
    def browse_source(self):
        """Browse for source folder."""
        folder = filedialog.askdirectory(title="Select Source Folder to Traverse")
        if folder:
            self.source_var.set(folder)
            self.log(f"📁 Source folder selected: {folder}")
            self.status_var.set(f"Source: {os.path.basename(folder)}")
    
    def browse_dest(self):
        """Browse for destination folder."""
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_var.set(folder)
            self.log(f"📂 Destination folder selected: {folder}")
            self.status_var.set(f"Destination: {os.path.basename(folder)}")
    
    def log(self, message):
        """Add message to log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_current_file(self, filename, status="Processing"):
        """Update the current file display."""
        if status == "Processing":
            display_text = f"📄 {status}: {filename}"
        elif status == "Copied":
            display_text = f"✅ {status}: {filename}"
        elif status == "Skipped":
            display_text = f"⏭️  {status}: {filename}"
        elif status == "Error":
            display_text = f"❌ {status}: {filename}"
        else:
            display_text = f"📄 {filename}"
        
        self.current_file_var.set(display_text)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log."""
        self.log_text.delete(1.0, tk.END)
        self.current_file_var.set("Ready to start...")
        self.copied_files = 0
        self.skipped_files = 0
        self.errors = 0
    
    def show_help(self):
        """Show help dialog."""
        help_text = """File Traverser Help

This tool copies all files from a source folder (including all subfolders) to a destination folder.

OPTIONS:
• Preserve directory structure: Keeps the original folder structure in the destination
• Overwrite existing files: Replaces files that already exist in the destination
• Show detailed output: Displays information about each file being copied

USAGE:
1. Select the source folder (the folder containing files you want to copy)
2. Select the destination folder (where you want the files copied to)
3. Choose your options
4. Click "Start Copying"

EXAMPLES:
• Copy all files to one folder: Uncheck "Preserve directory structure"
• Keep folder structure: Check "Preserve directory structure"
• Replace existing files: Check "Overwrite existing files"

The tool will automatically handle file naming conflicts by adding numbers (file_1.txt, file_2.txt, etc.) when not overwriting.
"""
        
        messagebox.showinfo("Help", help_text)
    
    def validate_inputs(self):
        """Validate user inputs."""
        source = self.source_var.get().strip()
        dest = self.dest_var.get().strip()
        
        if not source:
            messagebox.showerror("Error", "Please select a source folder!")
            return False
        
        if not dest:
            messagebox.showerror("Error", "Please select a destination folder!")
            return False
        
        if not os.path.exists(source):
            messagebox.showerror("Error", "Source folder does not exist!")
            return False
        
        if source == dest:
            messagebox.showerror("Error", "Source and destination folders cannot be the same!")
            return False
        
        return True
    
    def start_copy(self):
        """Start the copy operation."""
        if not self.validate_inputs():
            return
        
        # Disable start button and start progress
        self.start_button.config(state='disabled')
        self.progress.start()
        self.status_var.set("Copying files...")
        
        # Start copying in a separate thread
        thread = threading.Thread(target=self.copy_files)
        thread.daemon = True
        thread.start()
    
    def copy_files(self):
        """Copy files (runs in separate thread)."""
        try:
            source = self.source_var.get().strip()
            dest = self.dest_var.get().strip()
            
            self.log("=" * 60)
            self.log("🚀 Starting file traversal and copy operation...")
            self.log(f"📁 Source: {source}")
            self.log(f"📂 Destination: {dest}")
            self.log(f"📂 Preserve structure: {self.preserve_structure.get()}")
            self.log(f"🔄 Overwrite: {self.overwrite.get()}")
            self.log(f"📝 Verbose: {self.verbose.get()}")
            self.log("-" * 60)
            
            # Call the file traverser function
            self.traverse_and_copy_files(
                source_dir=source,
                dest_dir=dest,
                preserve_structure=self.preserve_structure.get(),
                overwrite=self.overwrite.get(),
                verbose=self.verbose.get()
            )
            
            self.log("-" * 60)
            self.log("✅ Copy operation completed successfully!")
            self.log(f"📊 Summary: {self.copied_files} copied, {self.skipped_files} skipped, {self.errors} errors")
            self.log("=" * 60)
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"Copy operation completed!\n\n"
                f"Files copied: {self.copied_files}\n"
                f"Files skipped: {self.skipped_files}\n"
                f"Errors: {self.errors}"))
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Copy operation failed: {e}"))
        
        finally:
            # Re-enable start button and stop progress
            self.root.after(0, self.copy_completed)
    
    def copy_completed(self):
        """Called when copy operation is completed."""
        self.start_button.config(state='normal')
        self.progress.stop()
        self.status_var.set("Ready")
    
    def traverse_and_copy_files(self, source_dir, dest_dir, preserve_structure=False, overwrite=False, verbose=False):
        """Traverse source directory and copy all files to destination directory."""
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)
        
        # Create destination directory if it doesn't exist
        dest_path.mkdir(parents=True, exist_ok=True)
        
        # Walk through all files in source directory
        for root, dirs, files in os.walk(source_path):
            root_path = Path(root)
            
            for file in files:
                source_file = root_path / file
                
                # Update current file display
                self.root.after(0, lambda f=file: self.update_current_file(f, "Processing"))
                
                if preserve_structure:
                    # Calculate relative path from source directory
                    relative_path = source_file.relative_to(source_path)
                    dest_file = dest_path / relative_path
                    
                    # Create subdirectories if needed
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                else:
                    # Flatten structure - all files go directly to destination
                    dest_file = dest_path / file
                    
                    # Handle naming conflicts by adding a number suffix
                    if not overwrite and dest_file.exists():
                        counter = 1
                        name_parts = file.rsplit('.', 1)
                        if len(name_parts) == 2:
                            base_name, extension = name_parts
                            new_name = f"{base_name}_{counter}.{extension}"
                        else:
                            new_name = f"{file}_{counter}"
                        
                        dest_file = dest_path / new_name
                        
                        # Keep incrementing until we find a unique name
                        while dest_file.exists():
                            counter += 1
                            if len(name_parts) == 2:
                                new_name = f"{base_name}_{counter}.{extension}"
                            else:
                                new_name = f"{file}_{counter}"
                            dest_file = dest_path / new_name
                
                try:
                    # Check if destination file exists and handle accordingly
                    if dest_file.exists() and not overwrite:
                        self.root.after(0, lambda f=file: self.update_current_file(f, "Skipped"))
                        if verbose:
                            self.log(f"⏭️  Skipped (exists): {source_file.name}")
                        self.skipped_files += 1
                        continue
                    
                    # Copy the file
                    shutil.copy2(source_file, dest_file)
                    
                    # Update current file display to show completion
                    self.root.after(0, lambda f=file: self.update_current_file(f, "Copied"))
                    
                    if verbose:
                        self.log(f"✅ Copied: {source_file.name}")
                    
                    self.copied_files += 1
                    
                except Exception as e:
                    self.root.after(0, lambda f=file: self.update_current_file(f, "Error"))
                    self.log(f"❌ Error copying {source_file.name}: {e}")
                    self.errors += 1





def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    
    # Set the application icon and title
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    app = FileTraverserGUI(root)
    
    # Handle window closing
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
