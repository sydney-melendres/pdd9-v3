import pandas as pd

# Load the CSV file
df = pd.read_csv('processes\csv\create_df.csv')

# Initialize a dictionary to keep track of each player's score
player_scores = {}

# Iterate over the DataFrame rows to recalculate the points
player_scores = {}
current_game = None

# Iterate over the DataFrame rows to recalculate the points
for index, row in df.iterrows():
    game = row['game']
    killer = row['killer']
    victim = row['victim']
    
    # Check if we are in a new game round
    if game != current_game:
        # Reset player scores for the new game round
        player_scores = {}
        current_game = game
    
    # Initialize players in the dictionary if not already present
    if killer not in player_scores:
        player_scores[killer] = 0
    if victim not in player_scores:
        player_scores[victim] = 0
    
    # Check if the killer is '<world>' or if it's a suicide
    if killer == '<world>' or killer == victim:
        # Do not change the points for the victim
        continue
    else:
        # Increase the killer's points
        player_scores[killer] += 1
        # Ensure points are not negative for the victim
        player_scores[victim] = max(player_scores[victim], 0)

    # Update the points in the DataFrame
    df.at[index, 'points'] = player_scores[killer]

# Save the adjusted DataFrame to a new CSV file
output_csv_path = 'processes\csv\offset_points.csv'
df.to_csv(output_csv_path, index=False)

# Display the updated DataFrame and its info
df_info = df.info()
df_head = df.head()

output_csv_path, df_info, df_head