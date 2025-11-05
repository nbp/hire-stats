#!/usr/bin/env python
#
# NOTE: The result of this script can be piped into `xclip -i` to paste the result somewhere else..

from collections import Counter
import argparse

# Mapping of flags to geographic longitudes
flag_longitude = {
    ':flag-ca:': -106.35,
    ':us:': -98.35,
    ':uk:': -0.12,
    ':flag-es:': 2.00,
    ':fr:': 2.35,
    ':de:': 10.45,
    ':flag-se:': 18.4,
    ':flag-au:': 106.35,
}

def read_hire_log(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    entries = data.split('\n')
    entries = [e for e in entries if e != ""]
    return entries

def last_entry_of(data):
    return data[-1]

def flags_of(entry):
    # Split by spaces.
    flags = entry.split()
    # Extract everything which starts and ends with a colon.
    flags = [ f for f in flags if f.startswith(':') and f.endswith(':')]
    return flags

def year_of(entry):
    date = entry.split(':')[0]
    (year, month, day) = date.split('-')
    return year

def this_year(data):
    return year_of(last_entry_of(data))

def filter_by_year(data, year):
    for line in data:
        if year_of(line) == year:
            yield line

def filter_this_year(data):
    last = data[-1]
    year = year_of(last)
    return filter_by_year(data, this_year(data))

def count_flags(data):
    # Extract all flags
    flags = []
    for line in data:
        flags.extend(flags_of(line))

    # Count the occurrences of each flag
    return Counter(flags)

def calculate_flag_percentages(data):
    # Count the occurrences of each flag
    flag_counts = count_flags(data)
    total_flags = sum(flag_counts.values())

    # Calculate the percentage for each flag
    flag_percentages = {flag: (count / total_flags) * 100 for flag, count in flag_counts.items()}
    return flag_percentages

def contrast_by_flag(dec_data, inc_data):
    dec_counts = count_flags(dec_data)
    inc_counts = count_flags(inc_data)
    total_counts = inc_counts + dec_counts
    diff_counts = inc_counts - dec_counts

    # Calculate the difference over the sum for each flag
    flag_percentages = {flag: ((inc_counts[flag] - dec_counts[flag])  / count) * 100 for flag, count in total_counts.items()}
    return flag_percentages

def display_flags_by_longitude(header, flag_percentages):
    # Sort flags by their geographic longitude
    sorted_flags = sorted(flag_percentages.items(), key=lambda item: flag_longitude.get(item[0], 0))

    s = ""
    for flag, percentage in sorted_flags:
        if s:
            s += ", "
        s += f"{flag} {percentage:.1f}%"
    s = f"{header}: {s}"
    print(s)

def display_stats(file_path):
    entries = read_hire_log(file_path)
    month_percentages = calculate_flag_percentages(entries[-1:])
    ytd_percentages = calculate_flag_percentages(filter_this_year(entries[-12:]))
    year_percentages = calculate_flag_percentages(entries[-12:])
    # all_percentages = calculate_flag_percentages(entries)
    yoy_span = -12
    yoy_stride = -12
    yoy_contrast = contrast_by_flag(entries[yoy_span + yoy_stride:yoy_stride], entries[yoy_span:])
    last_line = ' '.join(flags_of(last_entry_of(entries)))

    print(f"New Mozillian Flags: {last_line}")
    display_flags_by_longitude("New Mozillian Flag Stats", month_percentages)
    display_flags_by_longitude("New Mozillian Flag Stats (YTD)", ytd_percentages)
    display_flags_by_longitude("New Mozillian Flag Stats (over the past year)", year_percentages)
    # display_flags_by_longitude("New Mozillian Flag Stats since data collection started", all_percentages)
    display_flags_by_longitude("New Mozillian Flag Stats (YoY constrast)", yoy_contrast)

def main():
    parser = argparse.ArgumentParser(description="Process a file path argument.")
    parser.add_argument(
        "file",
        nargs="?",  # makes the argument optional
        default="hire_log.txt",
        help="Path to the file to process (default: hire_log.txt)"
    )
    args = parser.parse_args()

    display_stats(args.file)

if __name__ == "__main__":
    main()
