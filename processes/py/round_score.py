import pandas as pd

# Load the uploaded file
file_path = 'final_data\complete.csv'
data = pd.read_csv(file_path)

# Grouping by 'game' and 'killer' to select the last kill entry for each combination
last_kill_df = data.groupby(['game', 'killer']).tail(1).reset_index(drop=True)

# Renaming columns for clarity
last_kill_df = last_kill_df.rename(columns={'points': 'final_score'})

# Display the results
print(last_kill_df.head())

# Save to a CSV file with all columns
last_kill_df.to_csv('final_data\round_score.csv', index=False)