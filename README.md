# Merge G-code for Mid-Print Nozzle Swap

This repository contains a Python script designed to merge two G-code files, allowing for a mid-print nozzle swap. This is ideal for printing objects that require different levels of detail in different sections, such as starting with a 0.4mm nozzle for faster base printing and switching to a 0.25mm nozzle for finer top-layer details.

## Features

- **Automatic Nozzle Swap:** Retracts filament, lifts the nozzle, and cools it before pausing for a safe nozzle swap.
- **Customizable Transition:** Choose the layer at which to switch from one nozzle to another.
- **Flexible Reheat Temperature:** Specify the reheat temperature to match different filament requirements.
- **Safe Resumption:** Automatically lowers the nozzle and resumes printing with precise positioning.

## Prerequisites

- Python 3 installed on your machine.
- Two G-code files sliced for the same object:
  - One for a **0.4mm nozzle**.
  - One for a **0.25mm nozzle**.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pedrocandeias/merge-gcode-nozzle-swap.git
   cd merge-gcode-nozzle-swap
   ```

2. Ensure you have Python 3 installed:
   ```bash
   python3 --version
   ```

## Usage

### Basic Command

```bash
python3 merge_gcode_nozzle_swap.py <0.4mm_gcode_file> <0.25mm_gcode_file> <output_file> [--transition <layer_number>] [--reheat_temp <temperature>]
```

### Example Commands

1. **Default Midpoint Transition:**
   ```bash
   python3 merge_gcode.py 3DBenchy_040n_020mm.gcode 3DBenchy_025n_015mm.gcode merged_output.gcode
   ```

2. **Specify Transition Layer (e.g., at layer 60):**
   ```bash
   python3 merge_gcode.py 3DBenchy_040n_020mm.gcode 3DBenchy_025n_015mm.gcode merged_output.gcode --transition 60
   ```

3. **Specify Transition Layer and Reheat Temperature:**
   ```bash
   python3 merge_gcode.py 3DBenchy_040n_020mm.gcode 3DBenchy_025n_015mm.gcode merged_output.gcode --transition 60 --reheat_temp 200
   ```

## How It Works

- **Setup Handling:**
  - The script includes setup commands from both G-code files.

- **Nozzle Swap Process:**
  1. Retracts 5mm of filament to prevent oozing.
  2. Lifts the nozzle by 20mm for safe access.
  3. Turns off the extruder heater (`M104 S0`) to avoid burns.
  4. Pauses the printer (`M0`) for manual nozzle swap.
  5. After resuming, reheats the nozzle to the specified temperature (`M109 S210` by default).
  6. Lowers the nozzle back by 20mm to continue printing.

## Output

After running the script, you will see a message similar to:

```
Merged G-code successfully saved to merged_output.gcode with 60 layers from the 0.4mm file and 40 layers from the 0.25mm file.
```

You can then preview the merged G-code in your preferred G-code viewer to ensure correctness before printing.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or new features!

## License

This project is licensed under the MIT License.

## Author

Pedro Candeias

---

Happy Printing! 🛠️💃

