# PrintLoop
Automation for 3D Printing for Bambu Lab A1
# PrintLoop - 3D Print Automation Tool


## Overview

PrintLoop is a powerful automation tool for 3D printing that allows you to:

- Repeat a single STL multiple times automatically
- Combine multiple STLs with individual repetition counts
- Support both single color and multicolor printing
- Optimize your workflow with Bambu Lab printers

This application streamlines the process of creating repeated print jobs by automating the tedious manual steps of modifying G-code files.

## Installation

### Windows

1. Extract all files from the zip archive to a folder of your choice
2. Make sure to keep all files in the same directory structure
3. Double-click the `PrintLoop.exe` file to run the application
4. If Windows SmartScreen appears, click "More info" and then "Run anyway"

### Requirements

- Windows 10 or later
- No additional software required - all dependencies are included

## Using PrintLoop

### Getting Started

1. Launch PrintLoop by double-clicking the executable
2. You'll be greeted with a welcome screen
3. Select your printer model (currently Bambu A1 is supported)
4. Click "Continue" to proceed to the main application

### Main Interface

The main interface is divided into several sections:

1. **Header**: Shows your username and selected printer model
2. **Color Mode Selection**: Choose between Single Color and Multicolor printing
3. **Operation Mode Selection**: Choose between Simple and Advanced modes
4. **File Selection**: Select your .gcode.3mf file exported from Bambu Studio
5. **Repetition Settings**: Set how many times to repeat each plate
6. **Process Button**: Click to process your file

### Printing Modes

#### Single Color - Simple Mode
- For printing a single STL multiple times with the same color
- Select your .gcode.3mf file and specify how many times to repeat it

#### Single Color - Advanced Mode
- For printing multiple different STLs with the same color
- Allows setting individual repetition counts for each plate

#### Multicolor - Simple Mode
- For printing a single STL multiple times with different colors
- Requires setting up color primitives in Bambu Studio first

#### Multicolor - Advanced Mode
- For printing multiple different STLs with different colors
- Allows setting individual repetition counts for each plate

### Workflow Example

1. Design your model in your preferred 3D modeling software
2. Import the STL into Bambu Studio
3. Set up your print settings and slice the model
4. Export as .gcode.3mf file
5. Open PrintLoop and select the appropriate mode
6. Choose your exported .gcode.3mf file
7. Set the number of repetitions
8. Click "Process"
9. Import the resulting file back into Bambu Studio for printing

## G-code Modifications

PrintLoop makes specific modifications to the G-code files to optimize the automation process. For detailed information about these modifications, please refer to the `gcode_documentation.md` file included with this package.

Key modifications include:
- Disabling bed leveling between prints to save time
- Optimizing the cooling process for automatic part removal
- Ensuring proper shutdown sequence between prints

## Troubleshooting

### Common Issues

**Issue**: The application doesn't start
**Solution**: Make sure you have extracted all files from the zip archive and are running the application from the same folder.

**Issue**: The processed file doesn't work in Bambu Studio
**Solution**: Make sure you're using the correct mode for your specific workflow and that your original .gcode.3mf file is valid.

**Issue**: Parts don't release automatically between prints
**Solution**: Make sure your printer is slightly tilted as recommended and that the bed temperature is set to cool to exactly 20°C.

## License

PrintLoop is licensed for personal use only. Commercial use requires purchasing a license. See the License Agreement in the application for full details.

## Updates and Support

Visit [www.printloop.com](http://www.printloop.online) for updates, additional documentation, and support.

## Disclaimer

Using PrintLoop to automate multiple prints may cause damage to your 3D printer if not properly configured. The developers of PrintLoop are not responsible for any damage to 3D printers or other equipment that may result from using this software. Users assume all risks associated with automated printing.
