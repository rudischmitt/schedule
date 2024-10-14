#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import unittest

# Helper function to parse slot length
def parse_slot_length(slot_length):
    hours = 0
    minutes = 0
    if 'h' in slot_length:
        hours = int(slot_length.split('h')[0])
        remaining = slot_length.split('h')[1]
        if 'm' in remaining:
            minutes = int(remaining.replace('m', ''))
    elif 'm' in slot_length:
        minutes = int(slot_length.replace('m', ''))
    else:
        # If no unit is specified, assume it's in minutes
        minutes = int(slot_length)
    
    return timedelta(hours=hours, minutes=minutes)

# Helper function to format time
def format_time(dt, format_12, show_ampm):
    if format_12:
        if show_ampm:
            return dt.strftime("%I:%M %p")  # Include AM/PM
        else:
            return dt.strftime("%I:%M")     # Exclude AM/PM
    else:
        return dt.strftime("%H:%M")

# Main function to generate the schedule
def generate_schedule(start_time, slot_length, end_time, format_12, condensed_output, show_ampm):
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    slot_delta = parse_slot_length(slot_length)
    
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
    
    return schedule


# Test Cases
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


# Command line argument parser
def main():
    parser = argparse.ArgumentParser(description="Generate a time schedule from a specified start time, slot length, and ending time.")
    
    # Argument for 12-hour or 24-hour clock
    parser.add_argument('--12', '-12', action='store_true', help="Use 12-hour clock format (default).")
    parser.add_argument('--24', '-24', action='store_true', help="Use 24-hour clock format.")
    
    # Argument for starting time
    parser.add_argument('--StartingTime', '-st', default="09:00", help="Starting time in HH:MM format (default: 09:00 AM).")
    
    # Argument for slot length
    parser.add_argument('--SlotLength', '-sl', default="1h", help="Slot length in format [hours]h[minutes]m (e.g., 15m, 1h, 1h15m; default: 1h).")
    
    # Argument for ending time
    parser.add_argument('--EndingTime', '-et', default="17:00", help="Ending time in HH:MM format (default: 05:00 PM).")
    
    # Argument for condensed or spaced output
    parser.add_argument('--CondensedOutput', '-co', action='store_true', help="Use condensed output format (e.g., 09:00-09:15). This is the default.")
    parser.add_argument('--SpacedOutput', '-so', action='store_true', help="Use spaced output format (e.g., 09:00 - 09:15).")
    
    # Argument for showing AM/PM labels in 12-hour clock
    parser.add_argument('--ShowAMPM', '-ampm', action='store_true', help="Show AM/PM labels in 12-hour format (default: no AM/PM).")
    
    args = parser.parse_args()
    
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
    schedule = generate_schedule(start_time, slot_length, end_time, format_12, condensed_output, show_ampm)
    
    # Output the schedule
    for slot in schedule:
        print(slot)

if __name__ == "__main__":
    main()
