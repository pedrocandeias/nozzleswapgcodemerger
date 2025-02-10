import argparse


def parse_gcode_layers(filepath):
    layers = []
    current_layer = []
    setup_lines = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith(';LAYER:'):
                if current_layer:
                    layers.append(current_layer)
                    current_layer = []
            if not layers and not line.startswith(';LAYER:'):
                setup_lines.append(line)
            else:
                current_layer.append(line)
        if current_layer:
            layers.append(current_layer)
    return setup_lines, layers


def merge_gcode(setup_04, layers_04, setup_025, layers_025, transition_layer, reheat_temp):
    merged_gcode = []

    # Add setup lines from the 0.4mm file
    merged_gcode.extend(setup_04)

    # Add layers from the 0.4mm file up to the transition layer
    merged_gcode.extend([line for layer in layers_04[:transition_layer] for line in layer])

    # Insert commands for safe nozzle change
    merged_gcode.append("\n; --- NOZZLE CHANGE: Swap from 0.4mm to 0.25mm ---\n")
    merged_gcode.append("G1 E-5 F300 ; Retract 5mm of filament\n")
    merged_gcode.append("G91 ; Set to relative positioning\n")
    merged_gcode.append("G1 Z20 F600 ; Move nozzle up by 20mm\n")
    merged_gcode.append("G90 ; Set back to absolute positioning\n")
    merged_gcode.append("M104 S0 ; Turn off extruder heater to prevent burns\n")
    merged_gcode.append("M0 ; Pause for nozzle change. Resume after swapping the nozzle.\n")
    merged_gcode.append(f"M109 S{reheat_temp} ; Reheat nozzle to {reheat_temp}°C and wait\n")
    merged_gcode.append("G91 ; Set to relative positioning\n")
    merged_gcode.append("G1 Z-20 F600 ; Move nozzle back down by 20mm\n")
    merged_gcode.append("G90 ; Set back to absolute positioning\n\n")

    # Add setup lines from the 0.25mm file after nozzle change
    merged_gcode.extend(setup_025)

    # Add layers from the 0.25mm file starting from the transition layer
    merged_gcode.extend([line for layer in layers_025[transition_layer:] for line in layer])

    return merged_gcode


def main():
    parser = argparse.ArgumentParser(description="Merge two G-code files at a specified transition layer.")
    parser.add_argument('gcode_04', help='Path to the G-code file for the 0.4mm nozzle')
    parser.add_argument('gcode_025', help='Path to the G-code file for the 0.25mm nozzle')
    parser.add_argument('output', help='Path for the output merged G-code file')
    parser.add_argument('--transition', type=int, default=None, 
                        help='Layer number at which to switch from 0.4mm to 0.25mm G-code (must be within available layers)')
    parser.add_argument('--reheat_temp', type=int, default=210, help='Reheat temperature for the nozzle after swap (default: 210°C)')

    args = parser.parse_args()

    # Parse G-code layers and setup lines
    setup_04, layers_04 = parse_gcode_layers(args.gcode_04)
    setup_025, layers_025 = parse_gcode_layers(args.gcode_025)

    # Determine transition layer if not provided
    total_layers = min(len(layers_04), len(layers_025))
    transition_layer = args.transition if args.transition is not None else total_layers // 2

    # Validate transition layer
    if not 0 <= transition_layer <= total_layers:
        print(f"Error: Transition layer {transition_layer} is out of valid range (0 to {total_layers}).")
        return

    # Merge G-code
    merged_gcode = merge_gcode(setup_04, layers_04, setup_025, layers_025, transition_layer, args.reheat_temp)

    # Write the merged G-code to the output file
    with open(args.output, 'w') as output_file:
        output_file.writelines(merged_gcode)

    print(f"Merged G-code successfully saved to {args.output} with {len(layers_04[:transition_layer])} layers from the 0.4mm file and {len(layers_025[transition_layer:])} layers from the 0.25mm file.")


if __name__ == '__main__':
    main()
