# Schedule Generator Script README

## Overview
This is the **Rudis Schedule Generator Script**, which can be used to generate a schedule based on a given start time, slot length, and end time. The script allows flexibility in specifying the clock format (12-hour or 24-hour), slot length, and output format. It can be particularly useful for organizing time slots for meetings, appointments, or classes.

This Python script generates a time schedule based on a specified start time, slot length, and ending time. It allows you to choose between a 12-hour or 24-hour format and offers both condensed and spaced output options.

It is nothing anyone couldn't write themselves; hopefully, it saves you some time.

- **Repository**: [Rudis Schedule Generator](https://github.com/rudischmitt/schedule)
- **Assumes Python Version**: 3.0 or higher

## Requirements
The script has been tested on **WSL Bash 4.4** and requires Python 3 or higher to be installed.

## Features
- **12-Hour or 24-Hour Clock Format**: Supports generating schedules in either 12-hour or 24-hour format.
- **Customizable Slot Length**: Allows for slot lengths in formats such as `1h`, `30m`, or `1h15m`.
- **Condensed or Spaced Output**: Provides options to format the output as a condensed string (`e.g., 09:00-10:00`) or a spaced format (`e.g., 09:00 - 10:00`).
- **AM/PM Labels**: Options to include or exclude AM/PM labels in the 12-hour format.

## Installation
1. Clone this repository or download the `schedule.py` file.
2. Ensure that the script has executable permissions by running:
   ```bash
   chmod +x schedule.py
   ```

## Basic Usage
You can run the script directly from the command line with or without specifying arguments. By default, the script will generate a schedule starting at 9:00 AM, ending at 5:00 PM, using 1-hour slots, and with a 12-hour clock format.

### Basic Example:
```bash
./schedule.py
```

This will generate a schedule like this:
```
09:00-10:00
10:00-11:00
11:00-12:00
...
```

## Usage
The script can be used from the command line with various options to customize the output.

### Command Line Options
- `--12` or `-12`: Use the 12-hour clock format (default).
- `--24` or `-24`: Use the 24-hour clock format.
- `--StartingTime` or `-st`: Specify the starting time in `HH:MM` format (default: `09:00 AM`).
- `--SlotLength` or `-sl`: Specify the slot length in the format `[hours]h[minutes]m` (e.g., `15m`, `1h`, `1h15m`; default: `1h`).
- `--EndingTime` or `-et`: Specify the ending time in `HH:MM` format (default: `05:00 PM`).
- `--CondensedOutput` or `-co`: Use condensed output format (e.g., `09:00-09:15`). This is the default.
- `--SpacedOutput` or `-so`: Use spaced output format (e.g., `09:00 - 09:15`).
- `--ShowAMPM` or `-ampm`: Show AM/PM labels in the 12-hour format (default: no AM/PM).
- `--help` or `-h`: Show the help message and usage examples.

### Examples
1. **Generate a Schedule Using a 12-Hour Clock**
   ```bash
   python schedule_generator.py --StartingTime 9:00 AM --EndingTime 5:00 PM --SlotLength 1h --12
   ```
   This will generate a schedule from `9:00 AM` to `5:00 PM` with `1-hour` slots.

2. **Generate a Schedule Using a 24-Hour Clock**
   ```bash
   python schedule_generator.py --StartingTime 09:00 --EndingTime 17:00 --SlotLength 30m --24
   ```
   This will generate a schedule from `09:00` to `17:00` with `30-minute` slots.

3. **Generate a Schedule with Condensed Output**
   ```bash
   python schedule_generator.py --StartingTime 11 --EndingTime 2 --SlotLength 1h --ShowAMPM --CondensedOutput
   ```
   This assumes `11:00 AM` to `2:00 PM` with `1-hour` slots, showing AM/PM labels.

### Normalization Assumptions
- If the start time (`-st`) is provided without an `AM/PM` label, it is assumed to be **AM**.
- If the end time (`-et`) is provided without an `AM/PM` label, it is assumed to be **PM**.
- Input for `-st` and `-et` can be either **hours only** (`e.g., 11`) or **hours and minutes** (`e.g., 11:45`).

## Testing
The script includes unit tests to verify the functionality of different components. The unit tests cover:
- Slot length parsing for different formats (e.g., `1h`, `30m`, `1h15m`).
- Schedule generation in both **12-hour** and **24-hour** formats.
- Handling of invalid inputs for time formats and slot lengths.
- Edge cases like **crossing midnight**, **crossing noon**, and **mixed input formats** (e.g., `11 AM`, `2pm`).

### Running Tests
To run the unit tests, execute the script with `unittest`:
```bash
python -m unittest schedule_generator.py
```
Could always benefit from more test cases :).

## Error Handling
The script includes comprehensive error handling:
- **Improper Slot Length Format**: If the slot length is improperly formatted, a descriptive error message will be raised.
- **Invalid Time Format**: If start or end times are incorrectly formatted, an error message will indicate the problem.
- **End Time Before Start Time**: If the end time is earlier than or equal to the start time, an error message will be displayed.
- **Graceful Handling of No Slots**: If the provided times and slot length do not allow for any slots to be generated, a meaningful message is returned.

## License
This script is provided under the MIT License. Feel free to use, modify, and distribute it as needed.

## Troubleshooting
If you encounter issues running the script directly, ensure that Python 3 is installed and that the script has the proper executable permissions (`chmod +x schedule.py`). If you're on Windows, you may need to run the script with `python schedule.py` instead of `./schedule.py`.

## Contact
For any questions or suggestions, please contact **Rudi Schmitt** via the GitHub repository [Issues](https://github.com/rudischmitt/schedule/issues).

Happy Scheduling!

