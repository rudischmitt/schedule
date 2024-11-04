#!/usr/bin/env python3

# Rudis Schedule Generator Script
# Repository: https://github.com/rudischmitt/schedule
# Assumes Python 3.0 or higher

import argparse
from datetime import datetime, timedelta
import unittest
import re

# Helper function to parse slot length
def parse_slot_length(slot_length):
    """
    Parses a slot length string into a timedelta object.

    Args:
        slot_length (str): The slot length string in format [hours]h[minutes]m (e.g., '1h15m', '30m').

    Returns:
        timedelta: A timedelta object representing the parsed slot length.

    Raises:
        ValueError: If the input string is improperly formatted or contains invalid characters.
    """
    try:
        # Check if slot_length is empty or contains only whitespace
        if not slot_length or slot_length.strip() == "":
            raise ValueError("Slot length cannot be empty or whitespace only.")
        
        hours = 0
        minutes = 0
        if 'h' in slot_length:
            parts = slot_length.split('h')
            if len(parts) != 2 or not parts[0].isdigit():
                raise ValueError("Invalid hours format in slot length. Expected format is [hours]h[minutes]m, e.g., '1h15m'.")
            hours = int(parts[0])
            remaining = parts[1]
            if 'm' in remaining:
                if remaining.count('m') > 1 or not remaining.replace('m', '').isdigit():
                    raise ValueError("Invalid minutes format in slot length. Expected format is [hours]h[minutes]m, e.g., '1h15m'.")
                minutes = int(remaining.replace('m', ''))
            elif remaining:
                raise ValueError("Invalid format after hours in slot length. Expected format is [hours]h[minutes]m, e.g., '1h15m'.")
        elif 'm' in slot_length:
            if slot_length.count('m') > 1 or not slot_length.replace('m', '').isdigit():
                raise ValueError("Invalid minutes format in slot length. Expected format is [minutes]m, e.g., '15m'.")
            minutes = int(slot_length.replace('m', ''))
        else:
            if not slot_length.isdigit():
                raise ValueError("Invalid slot length format. Must be a number or include 'h'/'m'.")
            minutes = int(slot_length)
        
        return timedelta(hours=hours, minutes=minutes)
    except ValueError as e:
        raise ValueError(f"Error parsing slot length '{slot_length}': {e}")

# Helper function to format time
def format_time(dt, format_12, show_ampm):
    """
    Formats a datetime object into a string representation based on 12-hour or 24-hour format.

    Args:
        dt (datetime): The datetime object to format.
        format_12 (bool): Whether to use 12-hour clock format.
        show_ampm (bool): Whether to show AM/PM labels (applicable for 12-hour format).

    Returns:
        str: The formatted time string.
    """
    if format_12:
        if show_ampm:
            return dt.strftime("%I:%M %p")  # Include AM/PM
        else:
            return dt.strftime("%I:%M")     # Exclude AM/PM
    else:
        return dt.strftime("%H:%M")

# Function to normalize time input
def normalize_time_input(time_str, is_start_time, format_12):
    """
    Normalizes a time input string to ensure consistent format, applying default assumptions for AM/PM.

    Args:
        time_str (str): The input time string (e.g., '11', '11:45am').
        is_start_time (bool): Indicates if the input is a start time (used for default AM/PM assumptions).
        format_12 (bool): Whether the time format is 12-hour or 24-hour.

    Returns:
        str: The normalized time string in HH:MM AM/PM format (for 12-hour) or HH:MM format (for 24-hour).
    """
    # Remove whitespace and convert to lowercase
    time_str = time_str.strip().lower()
    
    if format_12:
        # Handle default AM/PM assumptions for 12-hour format
        if 'am' not in time_str and 'pm' not in time_str:
            if is_start_time:
                time_str += ' am'
            else:
                time_str += ' pm'
        
        # Add :00 if only hours are provided
        if re.match(r'^\d{1,2}(am|pm)$', time_str):
            time_str = time_str[:-2] + ':00 ' + time_str[-2:]
        
        # Ensure there is a space between the time and AM/PM
        time_str = re.sub(r'(\d{1,2}:\d{2})(am|pm)', r'\1 \2', time_str)
        
        # Capitalize AM/PM
        time_str = time_str.replace('am', 'AM').replace('pm', 'PM')
    else:
        # Add :00 if only hours are provided for 24-hour format
        if re.match(r'^\d{1,2}$', time_str):
            time_str += ':00'
    
    return time_str

# Main function to generate the schedule
def generate_schedule(start_time, slot_length, end_time, format_12, condensed_output, show_ampm):
    """
    Generates a schedule of time slots based on the given start time, slot length, and end time.

    Args:
        start_time (str): The starting time in HH:MM format, with optional AM/PM for 12-hour format.
        slot_length (str): The length of each time slot in format [hours]h[minutes]m.
        end_time (str): The ending time in HH:MM format, with optional AM/PM for 12-hour format.
        format_12 (bool): Whether to use 12-hour clock format.
        condensed_output (bool): Whether to use condensed output format (e.g., '09:00-10:00').
        show_ampm (bool): Whether to show AM/PM labels in the output (applicable for 12-hour format).

    Returns:
        list: A list of formatted time slots or an explanatory message if no slots could be generated.
    """
    try:
        start_time = normalize_time_input(start_time, is_start_time=True, format_12=format_12)
        end_time = normalize_time_input(end_time, is_start_time=False, format_12=format_12)
        
        if format_12:
            start = datetime.strptime(start_time, "%I:%M %p")
            end = datetime.strptime(end_time, "%I:%M %p")
        else:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
    except ValueError:
        raise ValueError(f"Error parsing start time '{start_time}' or end time '{end_time}'. Please use HH:MM format, and include AM/PM for 12-hour format.")
    
    # Check if end time is after start time
    if end <= start:
        raise ValueError(f"End time '{end_time}' must be after start time '{start_time}'.")
    
    try:
        slot_delta = parse_slot_length(slot_length)
    except ValueError as e:
        raise ValueError(f"Invalid slot length '{slot_length}': {e}")
    
    current_time = start
    schedule = []
    
    # Iterate to generate times until as close as possible to the end time
    while current_time + slot_delta <= end:
        end_slot_time = current_time + slot_delta
        if condensed_output:
            schedule.append(f"{format_time(current_time, format_12, show_ampm)}-{format_time(end_slot_time, format_12, show_ampm)}")
        else:
            schedule.append(f"{format_time(current_time, format_12, show_ampm)} - {format_time(end_slot_time, format_12, show_ampm)}")
        current_time = end_slot_time
    
    # If no slots are generated, provide a meaningful message
    if not schedule:
        return ["No slots could be generated. Please check your start time, end time, and slot length to ensure they allow for at least one time slot."]
    
    return schedule

# Command line argument processing function
def process_command_line_arguments():
    parser = argparse.ArgumentParser(description="Generate a time schedule from a specified start time, slot length, and ending time.")
    
    # Argument for 12-hour or 24-hour clock
    parser.add_argument('--12', '-12', action='store_true', help="Use 12-hour clock format (default).")
    parser.add_argument('--24', '-24', action='store_true', help="Use 24-hour clock format.")
    
    # Argument for starting time
    parser.add_argument('--StartingTime', '-st', nargs='+', default=["09:00", "AM"], help="Starting time in HH:MM AM/PM format for 12-hour or HH:MM for 24-hour format (default: 09:00 AM).")
    
    # Argument for slot length
    parser.add_argument('--SlotLength', '-sl', default="1h", help="Slot length in format [hours]h[minutes]m (e.g., 15m, 1h, 1h15m; default: 1h).")
    
    # Argument for ending time
    parser.add_argument('--EndingTime', '-et', nargs='+', default=["5:00", "PM"], help="Ending time in HH:MM AM/PM format for 12-hour or HH:MM for 24-hour format (default: 05:00 PM).")
    
    # Argument for condensed or spaced output
    parser.add_argument('--CondensedOutput', '-co', action='store_true', help="Use condensed output format (e.g., 09:00-09:15). This is the default.")
    
    # Argument for spaced output
    parser.add_argument('--SpacedOutput', '-so', action='store_true', help="Use spaced output format (e.g., 09:00 - 09:15).")

    # Argument for showing AM/PM labels in 12-hour clock
    parser.add_argument('--ShowAMPM', '-ampm', action='store_true', help="Show AM/PM labels in 12-hour format (default: no AM/PM).")

    args = parser.parse_args()

    # Join start and end time components if nargs is used
    if isinstance(args.StartingTime, list):
        args.StartingTime = " ".join(args.StartingTime)
    if isinstance(args.EndingTime, list):
        args.EndingTime = " ".join(args.EndingTime)

    return args

# Main function to run the script
def main():
    args = process_command_line_arguments()

    # Determine clock format (default to 12-hour)
    format_12 = not args.__dict__['24']  # If --24 is not specified, we default to 12-hour format

    # Determine if condensed or spaced output is used (default is condensed)
    condensed_output = not args.SpacedOutput

    # Determine if AM/PM should be shown (default is false)
    show_ampm = args.ShowAMPM

    start_time = args.StartingTime
    slot_length = args.SlotLength
    end_time = args.EndingTime

    # Generate the schedule
    try:
        schedule = generate_schedule(start_time, slot_length, end_time, format_12, condensed_output, show_ampm)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Output the schedule
    for slot in schedule:
        print(slot)

# Unit Tests
class TestScheduleScript(unittest.TestCase):
    
    def test_parse_slot_length_minutes(self):
        self.assertEqual(parse_slot_length("10"), timedelta(minutes=10))
        self.assertEqual(parse_slot_length("15m"), timedelta(minutes=15))

    def test_parse_slot_length_hours(self):
        self.assertEqual(parse_slot_length("1h"), timedelta(hours=1))
        self.assertEqual(parse_slot_length("1h15m"), timedelta(hours=1, minutes=15))

    def test_generate_schedule_condensed(self):
        schedule = generate_schedule("09:00", "1h", "12:00", format_12=True, condensed_output=True, show_ampm=False)
        expected = ["09:00-10:00", "10:00-11:00", "11:00-12:00"]
        self.assertEqual(schedule, expected)

    def test_generate_schedule_spaced_with_ampm(self):
        schedule = generate_schedule("09:00", "1h", "12:00", format_12=True, condensed_output=False, show_ampm=True)
        expected = ["09:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM"]
        self.assertEqual(schedule, expected)

    def test_generate_schedule_24_hour(self):
        schedule = generate_schedule("09:00", "1h", "12:00", format_12=False, condensed_output=True, show_ampm=False)
        expected = ["09:00-10:00", "10:00-11:00", "11:00-12:00"]
        self.assertEqual(schedule, expected)

    def test_invalid_slot_length(self):
        with self.assertRaises(ValueError):
            parse_slot_length("invalid")

    def test_invalid_start_time_format(self):
        with self.assertRaises(ValueError):
            generate_schedule("25:00", "1h", "12:00", format_12=False, condensed_output=True, show_ampm=False)

    def test_end_time_before_start_time(self):
        with self.assertRaises(ValueError):
            generate_schedule("10:00", "1h", "09:00", format_12=False, condensed_output=True, show_ampm=False)

if __name__ == "__main__":
    main()
    # Uncomment the following line to run unit tests
    # unittest.main()
