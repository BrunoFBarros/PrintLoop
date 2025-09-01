#!/usr/bin/env python3
"""
PrintLoop Hybrid - Combining minimal UI with V4 visuals and full functionality
This version uses the stable minimal UI framework with enhanced visuals and all features.
"""

import os
import sys
import zipfile
import tempfile
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import getpass  # To get the current username
import webbrowser  # To open web links
from PIL import Image, ImageTk


class PrintLoopHybrid:
    """Hybrid version of PrintLoop with minimal UI framework and V4 visuals."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("PrintLoop V4")
        self.root.geometry("800x700")
        style = ttk.Style(self.root)
        style.theme_use("default")  # or "clam" for better visuals
        style.configure("TButton", foreground="black")


        # Print debug info to console
        print("Initializing PrintLoop Hybrid...")
        print(f"Python version: {sys.version}")
        print(f"Tkinter version: {tk.TkVersion}")
        print(f"Current directory: {os.getcwd()}")
        
        # Set application icon if available
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "printloop_logo.ico")
            self.root.iconbitmap(icon_path)
            print(f"Set application icon from: {icon_path}")
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Get username and set default printer
        self.username = getpass.getuser()
        self.selected_printer = "Bambu A1"
        print(f"Username: {self.username}")
        print(f"Selected printer: {self.selected_printer}")
        
        # Variables
        self.input_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.output_filename_var = tk.StringVar()
        
        # Color mode (primary mode)
        self.color_mode_var = tk.StringVar(value="single")
        
        # Operation mode (secondary mode)
        self.operation_mode_var = tk.StringVar(value="simple")
        
        # Repetition variables
        self.simple_repetitions_var = tk.IntVar(value=1)
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)
        self.open_after_var = tk.BooleanVar(value=True)
        
        # For advanced mode
        self.plate_repetitions_vars = {}
        
        # Last used directory
        self.last_directory = os.path.expanduser("~")
        
        # Define colors for V4 branding
        self.colors = {
            "deep_blue": "#1E3A8A",
            "vibrant_teal": "#0D9488",
            "light_gray": "#F1F5F9",
            "dark_gray": "#334155",
            "white": "#FFFFFF"
        }
        
        # Apply custom styles
        self.apply_styles()
        
        # Show welcome message and license warning
        self.show_welcome_message()
        
        # Create UI
        self.create_widgets()
        
        # Detected plates
        self.detected_plates = []
        
        # Print debug info
        print("UI initialization complete")
    
    def apply_styles(self):
        """Apply custom styles to the UI elements."""
        style = ttk.Style()
        
        # Configure styles
        style.configure("TFrame", background=self.colors["white"])
        style.configure("TLabel", background=self.colors["white"], foreground=self.colors["dark_gray"])
        
        # Fix button text color to ensure contrast with background
        style.configure("TButton", background=self.colors["vibrant_teal"])
        style.map("TButton", 
                 foreground=[("active", self.colors["white"]), 
                             ("pressed", self.colors["white"]),
                             ("!disabled", self.colors["white"])],
                 background=[("active", self.colors["deep_blue"]), 
                             ("pressed", self.colors["deep_blue"])])
        
        style.configure("Header.TFrame", background=self.colors["deep_blue"])
        style.configure("Header.TLabel", background=self.colors["deep_blue"], foreground=self.colors["white"], font=("Helvetica", 12))
        
        style.configure("Title.TLabel", background=self.colors["white"], foreground=self.colors["deep_blue"], font=("Helvetica", 16, "bold"))
        style.configure("Subtitle.TLabel", background=self.colors["white"], foreground=self.colors["vibrant_teal"], font=("Helvetica", 12))
        
        style.configure("Mode.TRadiobutton", background=self.colors["white"])
        
        style.configure("Console.TFrame", background=self.colors["light_gray"])
        
        # Configure progress bar
        style.configure("TProgressbar", background=self.colors["vibrant_teal"])
    
    def show_welcome_message(self):
        """Show welcome message and license warning."""
        # Create a simple welcome dialog
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to PrintLoop V4")
        
        # Make the window much larger (nearly full screen)
        screen_width = welcome_window.winfo_screenwidth()
        screen_height = welcome_window.winfo_screenheight()
        window_width = int(screen_width * 0.8)  # 80% of screen width
        window_height = int(screen_height * 0.8)  # 80% of screen height
        welcome_window.geometry(f"{window_width}x{window_height}")
        
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        
        # Center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        welcome_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(welcome_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "printloop_logo.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((150, 150), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = ttk.Label(main_frame, image=logo_photo)
            logo_label.image = logo_photo  # Keep a reference
            logo_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Welcome text
        ttk.Label(main_frame, text=f"Welcome, {self.username}!", style="Title.TLabel").pack(pady=(0, 10))
        ttk.Label(main_frame, text="PrintLoop V4", style="Subtitle.TLabel").pack(pady=(0, 20))
        
        # Printer selection
        printer_frame = ttk.Frame(main_frame)
        printer_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(printer_frame, text="Select your printer:").pack(side=tk.LEFT, padx=(0, 10))
        
        printer_var = tk.StringVar(value="Bambu A1")
        printer_combo = ttk.Combobox(printer_frame, textvariable=printer_var, state="readonly")
        printer_combo["values"] = ["Bambu A1"]
        printer_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Warning text
        warning_frame = ttk.Frame(main_frame, padding="10")
        warning_frame.pack(fill=tk.X, pady=20)
        
        warning_text = ("WARNING: Using PrintLoop to automate multiple prints may cause damage to your 3D printer "
                       "if not properly configured. The developers of PrintLoop are not responsible for any damage "
                       "to 3D printers or other equipment that may result from using this software. "
                       "Users assume all risks associated with automated printing.")
        
        warning_label = ttk.Label(warning_frame, text=warning_text, wraplength=400)
        warning_label.pack(fill=tk.X)
        
        # License text
        license_var = tk.BooleanVar(value=False)
        license_check = ttk.Checkbutton(main_frame, text="I accept the license agreement and understand the risks", 
                                      variable=license_var)
        license_check.pack(pady=10)
        
        # Continue button
        def on_continue():
            if license_var.get():
                self.selected_printer = printer_var.get()
                welcome_window.destroy()
            else:
                messagebox.showwarning("License Agreement", "You must accept the license agreement to continue.")
        
        continue_button = ttk.Button(main_frame, text="Continue", command=on_continue)
        continue_button.pack(pady=10)
        
        # Wait for the window to be closed
        self.root.wait_window(welcome_window)
    
    def create_widgets(self):
        """Create and arrange all UI widgets."""
        # Create a main canvas with scrollbar to ensure all content is accessible
        self.main_canvas = tk.Canvas(self.root, background=self.colors["white"])
        self.main_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        
        # Configure the canvas
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.main_canvas.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        
        # Pack the canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")
        
        # Create a main frame inside the canvas
        self.main_frame = ttk.Frame(self.main_canvas, padding="10")
        self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw", width=self.root.winfo_width()-20)
        
        # Enable mousewheel scrolling
        self.root.bind_all("<MouseWheel>", lambda event: self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        # For Linux
        self.root.bind_all("<Button-4>", lambda event: self.main_canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Button-5>", lambda event: self.main_canvas.yview_scroll(1, "units"))
        
        # Header with user and printer info
        self.create_header()
        
        # Title
        title_label = ttk.Label(self.main_frame, text="PrintLoop V4", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Primary mode selection (color mode)
        color_mode_frame = ttk.LabelFrame(self.main_frame, text="Printing Mode", padding="10")
        color_mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Radiobutton(color_mode_frame, text="Single Color Printing", 
                       variable=self.color_mode_var, value="single", 
                       command=self.on_color_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(color_mode_frame, text="Multicolor Printing", 
                       variable=self.color_mode_var, value="multicolor", 
                       command=self.on_color_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        # Secondary mode selection (operation mode)
        operation_mode_frame = ttk.LabelFrame(self.main_frame, text="Operation Mode", padding="10")
        operation_mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.single_mode_frame = ttk.Frame(operation_mode_frame)
        self.multi_mode_frame = ttk.Frame(operation_mode_frame)
        
        # Single color operation modes
        ttk.Radiobutton(self.single_mode_frame, text="Simple Mode: Repeat single plate multiple times", 
                       variable=self.operation_mode_var, value="simple", 
                       command=self.on_operation_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(self.single_mode_frame, text="Advanced Mode: Handle multiple plates with individual repetition counts", 
                       variable=self.operation_mode_var, value="advanced", 
                       command=self.on_operation_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        # Multicolor operation modes
        ttk.Radiobutton(self.multi_mode_frame, text="Simple Mode: Repeat single multicolor setup multiple times", 
                       variable=self.operation_mode_var, value="simple", 
                       command=self.on_operation_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(self.multi_mode_frame, text="Advanced Mode: Handle multiple multicolor setups with individual repetition counts", 
                       variable=self.operation_mode_var, value="advanced", 
                       command=self.on_operation_mode_change, style="Mode.TRadiobutton").pack(anchor=tk.W, padx=10, pady=5)
        
        # Initially show single color mode
        self.single_mode_frame.pack(fill=tk.X)
        
        # File selection section
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_dir_var, width=50).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_filename_var, width=50).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        self.plates_label = ttk.Label(file_frame, text="")
        self.plates_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        # Repetition settings section
        self.repetition_frame = ttk.LabelFrame(self.main_frame, text="Repetition Settings", padding="10")
        self.repetition_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Simple mode repetition settings
        self.simple_repetition_frame = ttk.Frame(self.repetition_frame)
        self.simple_repetition_frame.pack(fill=tk.X)
        
        ttk.Label(self.simple_repetition_frame, text="Number of repetitions:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(self.simple_repetition_frame, from_=1, to=100, textvariable=self.simple_repetitions_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Advanced mode repetition settings (will be created dynamically)
        self.advanced_repetition_frame = ttk.Frame(self.repetition_frame)
        
        # Additional options
        options_frame = ttk.LabelFrame(self.main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Checkbutton(options_frame, text="Open output folder after processing", 
                       variable=self.open_after_var).pack(anchor=tk.W, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Process", command=self.process_file).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.on_exit).pack(side=tk.RIGHT, padx=5)
        
        # Status section
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(status_frame, textvariable=self.status_var).pack(fill=tk.X, padx=5, pady=5)

    def create_header(self):
        """Create the header section with user and printer info."""
        header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text=f"PrintLoop V4 initialized.", style="Header.TLabel").pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(header_frame, text=f"User: {self.username}", style="Header.TLabel").pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Label(header_frame, text=f"Printer: {self.selected_printer}", style="Header.TLabel").pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add a link to the project's GitHub page
        github_link = ttk.Label(header_frame, text="GitHub", foreground="blue", cursor="hand2", style="Header.TLabel")
        github_link.pack(side=tk.RIGHT, padx=10, pady=5)
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/your-repo/printloop"))

    def on_color_mode_change(self):
        """Handle changes in color mode selection."""
        color_mode = self.color_mode_var.get()
        
        # Hide both operation mode frames
        self.single_mode_frame.pack_forget()
        self.multi_mode_frame.pack_forget()
        
        if color_mode == "single":
            self.single_mode_frame.pack(fill=tk.X)
            # Default to simple mode for single color
            self.operation_mode_var.set("simple")
        elif color_mode == "multicolor":
            self.multi_mode_frame.pack(fill=tk.X)
            # Default to advanced mode for multicolor
            self.operation_mode_var.set("advanced")
        
        self.on_operation_mode_change()
    
    def on_operation_mode_change(self):
        """Handle changes in operation mode selection."""
        operation_mode = self.operation_mode_var.get()
        
        # Hide both repetition frames
        self.simple_repetition_frame.pack_forget()
        self.advanced_repetition_frame.pack_forget()
        
        if operation_mode == "simple":
            self.simple_repetition_frame.pack(fill=tk.X)
        elif operation_mode == "advanced":
            self.advanced_repetition_frame.pack(fill=tk.X)
            self.update_advanced_repetition_settings()
    
    def browse_input_file(self):
        """Open a file dialog to select the input .gcode.3mf file."""
        print("Browsing for input file...")
        file_path = filedialog.askopenfilename(
            initialdir=self.last_directory,
            title="Select .gcode.3mf file",
            filetypes=(("G-code 3MF files", "*.gcode.3mf"), ("All files", "*.*" ))
        )
        if file_path:
            self.input_file_var.set(file_path)
            self.last_directory = os.path.dirname(file_path)
            
            # Set output filename automatically
            base_name = os.path.basename(file_path).replace(".gcode.3mf", "")
            self.output_filename_var.set(f"{base_name}_single_x1.gcode.3mf")
            print(f"Output filename set to: {self.output_filename_var.get()}")
            
            # Detect plates and update UI for advanced mode
            self.detect_plates(file_path)
    
    def browse_output_dir(self):
        """Open a directory dialog to select the output folder."""
        print("Browsing for output directory...")
        dir_path = filedialog.askdirectory(
            initialdir=self.last_directory,
            title="Select Output Directory"
        )
        if dir_path:
            self.output_dir_var.set(dir_path)
            self.last_directory = dir_path
    
    def open_output_folder(self, path):
        """Open the output folder in the file explorer."""
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            print(f"Opening output folder: {path}")
        except Exception as e:
            print(f"Error opening folder: {e}")
            messagebox.showerror("Error", f"Could not open output folder: {e}")
            
    def detect_plates(self, input_file):
        """Detects plate files within the .gcode.3mf archive and updates the UI for advanced mode."""
        self.detected_plates = []
        self.plate_repetitions_vars = {}
        
        temp_dir = None
        try:
            print(f"Detecting plates in: {input_file}")
            temp_dir = tempfile.mkdtemp()
            print(f"Created temporary directory: {temp_dir}")
            
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            metadata_dir = os.path.join(temp_dir, "Metadata")
            if not os.path.exists(metadata_dir):
                self.plates_label.config(text="Error: Metadata directory not found in 3MF.")
                return
            
            for file in os.listdir(metadata_dir):
                if file.startswith("plate_") and file.endswith(".gcode"):
                    self.detected_plates.append(file)
            
            self.detected_plates.sort(key=lambda x: int(re.search(r'plate_(\d+)', x).group(1)))
            
            if self.detected_plates:
                self.plates_label.config(text=f"Detected {len(self.detected_plates)} plate(s): {', '.join(self.detected_plates)}")
                # Initialize repetition variables for advanced mode
                for plate in self.detected_plates:
                    self.plate_repetitions_vars[plate] = tk.IntVar(value=1)
            else:
                self.plates_label.config(text="No plates detected in the 3MF file.")
            
            # Update advanced repetition settings UI
            self.update_advanced_repetition_settings()
            
        except Exception as e:
            self.plates_label.config(text=f"Error detecting plates: {e}")
            print(f"Error detecting plates: {e}")
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def update_advanced_repetition_settings(self):
        """Dynamically update the advanced repetition settings UI based on detected plates."""
        # Clear existing widgets
        for widget in self.advanced_repetition_frame.winfo_children():
            widget.destroy()
        
        if not self.detected_plates:
            ttk.Label(self.advanced_repetition_frame, text="No plates detected for advanced settings.").pack(padx=5, pady=5)
            return
            
        ttk.Label(self.advanced_repetition_frame, text="Set repetitions for each plate:").pack(anchor=tk.W, padx=5, pady=5)
        
        for plate in self.detected_plates:
            frame = ttk.Frame(self.advanced_repetition_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=f"{plate}:").pack(side=tk.LEFT, padx=5)
            ttk.Spinbox(frame, from_=0, to=100, textvariable=self.plate_repetitions_vars[plate], width=5).pack(side=tk.LEFT, padx=5)
            
        # Add a set all button
        set_all_frame = ttk.Frame(self.advanced_repetition_frame)
        set_all_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(set_all_frame, text="Set all to:").pack(side=tk.LEFT, padx=5)
        set_all_var = tk.IntVar(value=1)
        ttk.Spinbox(set_all_frame, from_=0, to=100, textvariable=set_all_var, width=5).pack(side=tk.LEFT, padx=5)
        
        def set_all_repetitions():
            value = set_all_var.get()
            for var in self.plate_repetitions_vars.values():
                var.set(value)
        
        ttk.Button(set_all_frame, text="Apply", command=set_all_repetitions).pack(side=tk.LEFT, padx=5)
    
    def process_file(self):
        """Process the input file."""
        # Validate inputs
        input_file = self.input_file_var.get()
        output_dir = self.output_dir_var.get()
        output_filename = self.output_filename_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
        
        if not output_filename:
            messagebox.showerror("Error", "Please enter an output filename")
            return
        
        # Get processing parameters
        color_mode = self.color_mode_var.get()
        operation_mode = self.operation_mode_var.get()
        is_multicolor = (color_mode == "multicolor")
        
        # Get repetition counts
        if operation_mode == "simple":
            repetitions = self.simple_repetitions_var.get()
            print(f"Simple mode: {repetitions} repetitions")
        else:
            if not self.detected_plates:
                messagebox.showerror("Error", "No plates detected in the input file")
                return
            
            if not self.plate_repetitions_vars:
                messagebox.showerror("Error", "Plate repetition settings not available")
                return
            
            # Get repetitions for each plate
            repetitions = {}
            for plate, var in self.plate_repetitions_vars.items():
                count = var.get()
                if count > 0:
                    repetitions[plate] = count
            
            if not repetitions:
                messagebox.showerror("Error", "No plates selected for processing")
                return
            
            print(f"Advanced mode: {len(repetitions)} plates with custom repetitions")
        
        # Confirm processing
        if not messagebox.askyesno("Confirm", "Are you sure you want to process the file?"):
            return
        
        # Process the file
        try:
            print("\n--- Starting file processing ---")
            self.status_var.set("Processing...")
            self.progress_var.set(20)
            self.root.update_idletasks()
            
            # Create output path
            output_path = os.path.join(output_dir, output_filename)
            print(f"Output path: {output_path}")
            
            # Process the file
            if operation_mode == "simple":
                success = self.process_simple_mode(
                    input_file=input_file,
                    output_file=output_path,
                    repetitions=repetitions,
                    is_multicolor=is_multicolor
                )
            else:
                success = self.process_advanced_mode(
                    input_file=input_file,
                    output_file=output_path,
                    repetitions=repetitions,
                    is_multicolor=is_multicolor
                )
            
            if success:
                self.status_var.set("Processing complete")
                self.progress_var.set(100)
                print("Processing complete!")
                messagebox.showinfo("Success", f"File processed successfully.\nOutput: {output_path}")
                
                # Open output folder if requested
                if self.open_after_var.get():
                    self.open_output_folder(output_dir)
            else:
                self.status_var.set("Processing failed")
                self.progress_var.set(0)
                print("Processing failed!")
                messagebox.showerror("Error", "Failed to process file")
        
        except Exception as e:
            self.status_var.set("Error processing file")
            self.progress_var.set(0)
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")
    
    def process_simple_mode(self, input_file, output_file, repetitions, is_multicolor=False):
        """
        Process the file in simple mode.
        
        Args:
            input_file: Path to the input .gcode.3mf file
            output_file: Path to the output .gcode.3mf file
            repetitions: Number of repetitions
            is_multicolor: Whether to process in multicolor mode
        
        Returns:
            True if successful, False otherwise
        """
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory: {temp_dir}")
        
        try:
            # Extract the .gcode.3mf file
            print("Extracting input file...")
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find plate files
            metadata_dir = os.path.join(temp_dir, "Metadata")
            if not os.path.exists(metadata_dir):
                print("Error: Metadata directory not found")
                return False
            
            # Get all plate_*.gcode files
            plate_files = []
            for file in os.listdir(metadata_dir):
                if file.startswith("plate_") and file.endswith(".gcode"):
                    plate_files.append(os.path.join(metadata_dir, file))
            
            # Sort by plate number
            plate_files.sort(key=lambda x: int(re.search(r'plate_(\d+)', os.path.basename(x)).group(1)))
            
            if not plate_files:
                print("Error: No plate files found")
                return False
            
            print(f"Found {len(plate_files)} plate files: {[os.path.basename(p) for p in plate_files]}")
            
            # Get the first plate file (plate_1.gcode)
            plate_1_file = os.path.join(metadata_dir, "plate_1.gcode")
            if not os.path.exists(plate_1_file):
                print("Error: plate_1.gcode not found")
                return False
            
            # Read the start and end G-code
            script_dir = os.path.dirname(os.path.abspath(__file__))
            start_gcode_path = os.path.join(script_dir, "Start_A1_PrintLoop.txt")
            end_gcode_path = os.path.join(script_dir, "End_A1_PrintLoop.txt")
            
            start_gcode = ""
            end_gcode = ""
            
            if os.path.exists(start_gcode_path):
                print(f"Reading start G-code from: {start_gcode_path}")
                with open(start_gcode_path, 'r') as f:
                    start_gcode = f.read()
            else:
                print("Warning: Start G-code file not found, using empty string")
            
            if os.path.exists(end_gcode_path):
                print(f"Reading end G-code from: {end_gcode_path}")
                with open(end_gcode_path, 'r') as f:
                    end_gcode = f.read()
            else:
                print("Warning: End G-code file not found, using empty string")
            
            # Process the plates
            if is_multicolor:
                print("Processing in multicolor mode...")
                # Multicolor mode: Clear plate_1.gcode and add content from other plates
                with open(plate_1_file, 'w') as f:
                    # Add a header comment
                    f.write(";===== PrintLoop V4 - Multicolor Simple Mode =====\n")
                    f.write(";===== Generated by PrintLoop V4 =====\n\n")
                    
                    # Process each plate based on repetitions
                    for plate_file in plate_files[1:]:  # Skip plate_1.gcode
                        # Read the plate content
                        with open(plate_file, 'r') as plate_f:
                            plate_content = plate_f.read()
                        
                        # Add the plate content multiple times
                        for i in range(repetitions):
                            f.write(f";===== Start of {os.path.basename(plate_file)} (Copy {i+1}/{repetitions}) =====\n")
                            f.write(start_gcode)
                            f.write("\n")
                            f.write(plate_content)
                            f.write("\n")
                            f.write(end_gcode)
                            f.write(f";===== End of {os.path.basename(plate_file)} (Copy {i+1}/{repetitions}) =====\n\n")
                
                # Remove other plate files in multicolor mode
                for file in plate_files[1:]:
                    print(f"Removing plate file: {os.path.basename(file)}")
                    os.remove(file)
            else:
                print("Processing in single color mode...")
                # Single color mode: Add content to plate_1.gcode
                with open(plate_1_file, 'r') as f:
                    original_content = f.read()
                
                with open(plate_1_file, 'w') as f:
                    # Add a header comment
                    f.write(";===== PrintLoop V4 - Single Color Simple Mode =====\n")
                    f.write(";===== Generated by PrintLoop V4 =====\n\n")
                    
                    # Add the plate content multiple times
                    for i in range(repetitions):
                        f.write(f";===== Start of plate_1.gcode (Copy {i+1}/{repetitions}) =====\n")
                        f.write(start_gcode)
                        f.write("\n")
                        f.write(original_content)
                        f.write("\n")
                        f.write(end_gcode)
                        f.write(f";===== End of plate_1.gcode (Copy {i+1}/{repetitions}) =====\n\n")
            
            # Create the output directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                print(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)
            
            # Create the output .gcode.3mf file
            print(f"Creating output file: {output_file}")
            with zipfile.ZipFile(output_file, 'w') as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        print(f"Adding to zip: {arcname}")
                        zip_out.write(file_path, arcname)
            
            print("File processing completed successfully")
            return True
        
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            return False
        
        finally:
            # Clean up temporary directory
            if temp_dir and os.path.exists(temp_dir):
                print(f"Cleaning up temporary directory: {temp_dir}")
                shutil.rmtree(temp_dir)
    
    def process_advanced_mode(self, input_file, output_file, repetitions, is_multicolor=False):
        """
        Process the file in advanced mode.
        
        Args:
            input_file: Path to the input .gcode.3mf file
            output_file: Path to the output .gcode.3mf file
            repetitions: Dictionary mapping plate file names to repetition counts
            is_multicolor: Whether to process in multicolor mode
        
        Returns:
            True if successful, False otherwise
        """
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory: {temp_dir}")
        
        try:
            # Extract the .gcode.3mf file
            print("Extracting input file...")
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find plate files
            metadata_dir = os.path.join(temp_dir, "Metadata")
            if not os.path.exists(metadata_dir):
                print("Error: Metadata directory not found")
                return False
            
            # Get the first plate file (plate_1.gcode)
            plate_1_file = os.path.join(metadata_dir, "plate_1.gcode")
            if not os.path.exists(plate_1_file):
                print("Error: plate_1.gcode not found")
                return False
            
            # Read the start and end G-code
            script_dir = os.path.dirname(os.path.abspath(__file__))
            start_gcode_path = os.path.join(script_dir, "Start_A1_PrintLoop.txt")
            end_gcode_path = os.path.join(script_dir, "End_A1_PrintLoop.txt")
            
            start_gcode = ""
            end_gcode = ""
            
            if os.path.exists(start_gcode_path):
                print(f"Reading start G-code from: {start_gcode_path}")
                with open(start_gcode_path, 'r') as f:
                    start_gcode = f.read()
            else:
                print("Warning: Start G-code file not found, using empty string")
            
            if os.path.exists(end_gcode_path):
                print(f"Reading end G-code from: {end_gcode_path}")
                with open(end_gcode_path, 'r') as f:
                    end_gcode = f.read()
            else:
                print("Warning: End G-code file not found, using empty string")
            
            # Process the plates
            if is_multicolor:
                print("Processing in multicolor advanced mode...")
                # Multicolor mode: Clear plate_1.gcode and add content from other plates
                with open(plate_1_file, 'w') as f:
                    # Add a header comment
                    f.write(";===== PrintLoop V4 - Multicolor Advanced Mode =====\n")
                    f.write(";===== Generated by PrintLoop V4 =====\n\n")
                    
                    # Process each plate based on repetitions
                    for plate_file, count in repetitions.items():
                        # Skip plate_1.gcode
                        if plate_file == "plate_1.gcode":
                            continue
                        
                        # Read the plate content - FIX: Use proper path
                        plate_path = os.path.join(metadata_dir, plate_file)
                        if not os.path.exists(plate_path):
                            print(f"Warning: Plate file {plate_file} not found, skipping")
                            continue
                            
                        with open(plate_path, 'r') as plate_f:
                            plate_content = plate_f.read()
                        
                        # Add the plate content multiple times
                        for i in range(count):
                            f.write(f";===== Start of {plate_file} (Copy {i+1}/{count}) =====\n")
                            f.write(start_gcode)
                            f.write("\n")
                            f.write(plate_content)
                            f.write("\n")
                            f.write(end_gcode)
                            f.write(f";===== End of {plate_file} (Copy {i+1}/{count}) =====\n\n")
                
                # Remove other plate files in multicolor mode
                for plate_file in repetitions.keys():
                    if plate_file != "plate_1.gcode":
                        plate_path = os.path.join(metadata_dir, plate_file)
                        if os.path.exists(plate_path):
                            print(f"Removing plate file: {plate_file}")
                            os.remove(plate_path)
            else:
                print("Processing in single color advanced mode...")
                # Single color mode: Add content to plate_1.gcode
                with open(plate_1_file, 'w') as f:
                    # Add a header comment
                    f.write(";===== PrintLoop V4 - Single Color Advanced Mode =====\n")
                    f.write(";===== Generated by PrintLoop V4 =====\n\n")
                    
                    # Process each plate based on repetitions
                    for plate_file, count in repetitions.items():
                        # Read the plate content - FIX: Use proper path
                        plate_path = os.path.join(metadata_dir, plate_file)
                        if not os.path.exists(plate_path):
                            print(f"Warning: Plate file {plate_file} not found, skipping")
                            continue
                            
                        with open(plate_path, 'r') as plate_f:
                            plate_content = plate_f.read()
                        
                        # Add the plate content multiple times
                        for i in range(count):
                            f.write(f";===== Start of {plate_file} (Copy {i+1}/{count}) =====\n")
                            f.write(start_gcode)
                            f.write("\n")
                            f.write(plate_content)
                            f.write("\n")
                            f.write(end_gcode)
                            f.write(f";===== End of {plate_file} (Copy {i+1}/{count}) =====\n\n")
            
            # Create the output directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                print(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir)
            
            # Create the output .gcode.3mf file
            print(f"Creating output file: {output_file}")
            with zipfile.ZipFile(output_file, 'w') as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        print(f"Adding to zip: {arcname}")
                        zip_out.write(file_path, arcname)
            
            print("File processing completed successfully")
            return True
        
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            return False
        
        finally:
            # Clean up temporary directory
            if temp_dir and os.path.exists(temp_dir):
                print(f"Cleaning up temporary directory: {temp_dir}")
                shutil.rmtree(temp_dir)


    def on_exit(self):
        """Handle application exit."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PrintLoopHybrid(root)
    root.mainloop()

