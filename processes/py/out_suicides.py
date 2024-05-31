import pandas as pd

# Load the CSV file
file_path = 'processes\csv\offset_points.csv'
df = pd.read_csv(file_path)

# Make sure the columns are trimmed of any extra spaces
df.columns = df.columns.str.strip()

df = df[(df['killer'] != '<world>') & (df['killer'] != df['victim'])]

# Save the adjusted dataframe back to a CSV file
output_file_path = 'final_data\complete.csv'
df.to_csv(output_file_path, index=False)

output_file_path
