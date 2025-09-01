# Improved G-code Documentation for PrintLoop

## Start G-code (Start_A1_PrintLoop.txt)

### Overview
The Start G-code file has been modified to optimize the printing process for repeated prints. The key modifications include:

1. **Disabled Bed Leveling**: The automatic bed leveling process has been disabled to save time between prints. This is particularly useful for automation as it prevents unnecessary leveling when the bed is already properly calibrated.

2. **Optimized Heating Sequence**: The heating sequence has been adjusted to minimize oozing and ensure proper temperature management during the startup process.

3. **Enhanced Nozzle Cleaning**: The nozzle cleaning routine has been improved to ensure a clean start for each print, reducing the chance of first-layer issues.

4. **Branded Headers and Comments**: Clear headers and comments have been added to make the G-code more understandable and to indicate which sections have been modified.

### Detailed Modifications

#### Bed Leveling Section
```gcode
;===== BED LEVELING DISABLED =========================
; The following section has been modified by PrintLoop
; to disable automatic bed leveling between prints.
; Original commands are commented out.
; If you need to level your bed, please do so manually.

G29.2 S0 ; turn off ABL
; G29.2 S1 ; turn on ABL - DISABLED
; M622 J1
;     M1002 gcode_claim_action : 1
;     G29 A1 X{first_layer_print_min[0]} Y{first_layer_print_min[1]} I{first_layer_print_size[0]} J{first_layer_print_size[1]}
;     M400
;     M500 ; save cali data
; M623
;===== BED LEVELING DISABLED END =====================
```

This modification:
- Turns off Auto Bed Leveling (ABL) with `G29.2 S0`
- Comments out the commands that would normally perform bed leveling
- Maintains the original code (commented out) for reference
- Adds clear explanatory comments

#### Nozzle Temperature Management
The G-code carefully manages nozzle temperature to:
- Prevent oozing during startup
- Ensure proper temperature for first layer adhesion
- Optimize the transition between preparation and printing

#### Nozzle Cleaning Routine
The nozzle cleaning routine:
- Performs a series of wipes against the printer's cleaning pad
- Uses precise movements to remove any residual filament
- Ensures a clean nozzle before starting the print

## End G-code (End_A1_PrintLoop.txt)

### Overview
The End G-code file has been modified to ensure proper print completion and facilitate automatic object removal. Key modifications include:

1. **Controlled Cooling**: The bed is set to cool to exactly 20°C, which is the optimal temperature for print release on the Bambu A1.

2. **Automatic Object Removal**: The bed is moved forward to help objects fall off when the printer is tilted as per your setup.

3. **Complete Shutdown Sequence**: All motors, heating elements, and fans are properly turned off to ensure the printer is ready for the next print.

4. **Branded Headers and Comments**: Clear headers and comments have been added to make the G-code more understandable.

### Detailed Modifications

#### Cooling and Object Removal
```gcode
;===== Wait for bed to cool to 20°C ===================
; This ensures the print will release from the bed
; When using a tilted printer setup, objects will fall off
M190 R20 ; wait for bed to cool to 20°C

;===== Move bed forward to help objects fall off =======
G1 Y250 F3000 ; move bed all the way forward
```

This modification:
- Uses `M190 R20` to wait for the bed to cool to exactly 20°C (not higher, not lower)
- Moves the bed fully forward with `G1 Y250 F3000` to help objects fall off when the printer is tilted
- Adds clear explanatory comments

#### Complete Shutdown Sequence
The shutdown sequence:
- Disables all motors with `M84`
- Turns off all fans and heating elements
- Displays a completion message

## Using the Modified G-code Files

To use these modified G-code files:
1. In Bambu Studio, go to Printer Settings
2. Select the Custom G-code tab
3. Replace the Start G-code with the content of Start_A1_PrintLoop.txt
4. Replace the End G-code with the content of End_A1_PrintLoop.txt
5. Save your printer profile

These modifications will significantly improve the automation workflow by:
- Reducing time between prints by skipping bed leveling
- Ensuring prints release automatically when the bed cools
- Providing a reliable and consistent printing experience for repeated jobs
