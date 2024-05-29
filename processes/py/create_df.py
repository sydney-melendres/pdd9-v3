import pandas as pd

# Define input path for the log file
input_path = 'processes\logs\start_again.log'

# Initialize lists to store data for DataFrame
timestamps = []
games = []
latencies = []
maps = []
killers = []
victims = []
points = []

current_map = ''
current_latency = 0
game_counter = 0

# Read the input file
with open(input_path, 'r') as file:
    lines = file.readlines()

# Read the input file and process each line
for line in lines:
    if 'Network egress latency:' in line:
        # Extract timestamp and latency value
        parts = line.split(': ', 1)
        if len(parts) > 1:
            timestamp = parts[0]
            latency_value = parts[1].split(' ')[3]  # Get the latency value in ms
            current_latency = int(latency_value)
            game_counter += 1
    elif 'loaded maps' in line:  # Adjusted to match the map loading line format
        # Extract timestamp and map name
        parts = line.split(': ', 1)
        if len(parts) > 1:
            timestamp = parts[0]
            map_parts = parts[1].split('/')
            if len(map_parts) > 1:
                map_name = map_parts[-1].split('.')[0]  # Extract map name correctly
                current_map = map_name.strip()  # Ensure no leading/trailing whitespace
    elif 'kill:' in line.lower():  # Make case insensitive
        # Extract timestamp, killer, victim, and points
        parts = line.split(': ', 1)
        if len(parts) > 1:
            timestamp = parts[0]
            killer_part = parts[1].split(' ')
            try:
                if 'killed' in killer_part:
                    killer_index = killer_part.index('killed') - 1
                    killer = killer_part[killer_index]
                    victim_index = killer_index + 2
                    victim = killer_part[victim_index]
                    # Find the points value in the line
                    for i, part in enumerate(killer_part):
                        if part.isdigit() and 'points' in killer_part[i + 1]:
                            point_value = part
                            break
                    else:
                        point_value = 0  # Default value if points not found

                    # Append collected data to lists
                    timestamps.append(timestamp)
                    games.append(game_counter)
                    latencies.append(current_latency)
                    maps.append(current_map)
                    killers.append(killer)
                    victims.append(victim)
                    points.append(int(point_value))
            except (ValueError, IndexError) as e:
                print(f"Error processing line: {line}, error: {e}")  # Debug print

# Create DataFrame with the collected data
df = pd.DataFrame({
    'timestamp': timestamps,
    'game': games,
    'latency': latencies,
    'map': maps,
    'killer': killers,
    'victim': victims,
    'points': points
})

# Debug print of the DataFrame
print(df.head())  # Print first few rows to check content

# Save the DataFrame to a CSV file
output_csv_path = 'processes\csv\create_df.csv'
df.to_csv(output_csv_path, index=False)

# Display the DataFrame and the number of entries
df_info = df.info()
df_head = df.head()

output_csv_path, df_info, df_head