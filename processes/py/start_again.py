import re
from datetime import datetime

def format_timestamp(timestamp):
    try:
        # Try to parse as a float Unix timestamp
        datetime_obj = datetime.fromtimestamp(float(timestamp))
    except ValueError:
        # If it fails, assume the timestamp is already formatted
        return timestamp
    date_str = datetime_obj.strftime('%Y-%m-%d')
    time_str = datetime_obj.strftime('%H:%M:%S')
    return f"{date_str} {time_str}"

input_path = 'processes\logs\start.log'
output_path = 'processes\logs\start_again.log'

# Read the input file
with open(input_path, 'r') as file:
    lines = file.readlines()

# Process the file and write to the output file
with open(output_path, 'w') as output_file:
    for line in lines:
        if '\\x08 \\x08Kill:' in line:
            parts = line.split(': ', 1)
            timestamp = parts[0]
            formatted_timestamp = format_timestamp(timestamp)
            # Match Kill, PlayerScore, and Challenge events
            occurrences = re.findall(r'(\\x08 \\x08Kill:.*?)(?=(\\x08 \\x08Kill:|\\n))', parts[1])
            for occurrence in occurrences:
                event_line = occurrence[0]
                player_score_matches = re.findall(r'(\\x08 \\x08PlayerScore:.*?)(?=(\\x08 \\x08Kill:|\\n|$))', parts[1])
                for player_score in player_score_matches:
                    event_line += player_score[0]
                challenge_matches = re.findall(r'(\\x08 \\x08Challenge:.*?)(?=(\\x08 \\x08Kill:|\\n|$))', parts[1])
                for challenge in challenge_matches:
                    event_line += challenge[0]
                output_file.write(f"{formatted_timestamp}: {event_line}\n")
        elif 'Network egress latency:' in line or '\\x08loaded maps' in line:
            parts = line.split(': ', 1)
            timestamp = parts[0]
            formatted_timestamp = format_timestamp(timestamp)
            output_file.write(f"{formatted_timestamp}: {parts[1].strip()}\n")
        else:
            output_file.write(line)