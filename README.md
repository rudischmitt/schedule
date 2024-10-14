# Schedule Generator Script

This Python script generates a time schedule based on a specified start time, slot length, and ending time. It allows you to choose between a 12-hour or 24-hour format and offers both condensed and spaced output options.

It is nothing anyone couldn't write themselves; hopefully, it saves you some time.

## Features
- Generate a schedule with customizable time slots.
- Choose between 12-hour and 24-hour clock formats.
- Provide custom start and end times.
- Select between condensed (default) and spaced output formats.
- Default settings are provided for convenience but can be overridden via command line arguments.

## Requirements
- **Python 3.x** is required to run the script.

## Installation
1. Clone this repository or download the `schedule.py` file.
2. Ensure that the script has executable permissions by running:
   ```bash
   chmod +x schedule.py
   ```

## Usage
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

### Custom Options:
You can customize the output by providing command line arguments.

#### Command Line Arguments:
- `--12`, `-12`: Use the 12-hour clock format (default).
- `--24`, `-24`: Use the 24-hour clock format.
- `--StartingTime`, `-st`: Specify the starting time in `HH:MM` format (default: `09:00` AM).
- `--SlotLength`, `-sl`: Specify the slot length in `hours` and/or `minutes` (default: `1h`). Examples: `15m`, `1h`, `1h15m`.
- `--EndingTime`, `-et`: Specify the ending time in `HH:MM` format (default: `17:00` or 5:00 PM).
- `--CondensedOutput`, `-co`: Output without spaces between times (default). Example: `09:00-10:00`.
- `--SpacedOutput`, `-so`: Output with spaces between times. Example: `09:00 - 10:00`.

#### Example with Custom Options:
```bash
./schedule.py --24 --StartingTime 08:00 --SlotLength 30m --EndingTime 18:00 --SpacedOutput
```

This will generate:
```
08:00 - 08:30
08:30 - 09:00
09:00 - 09:30
...
17:30 - 18:00
```

## Troubleshooting
If you encounter issues running the script directly, ensure that Python 3 is installed and that the script has the proper executable permissions (`chmod +x schedule.py`). If you're on Windows, you may need to run the script with `python schedule.py` instead of `./schedule.py`.


## Author
[Rudolf Schmitt]

## Basic Example
 ```./schedule.py
