import pandas as pd

# Load PCA results (player scores and ranks)
pca_data = pd.read_csv('player_scores_with_rank.csv')

# Load team data (team stats and player information)
team_data = pd.read_csv('team_average_stats.csv')

# Check the column names of both datasets to ensure they match
print("PCA Data Columns:", pca_data.columns)
print("Team Data Columns:", team_data.columns)

# Clean column names by stripping extra spaces
pca_data.columns = pca_data.columns.str.strip()
team_data.columns = team_data.columns.str.strip()

# Merge the data based on team name ('Tm')
merged_data = pd.merge(pca_data, team_data, on='Tm')

# Check the first few rows of the merged data to ensure it combined correctly
print(merged_data.head())

# Optionally, save the merged data to a new CSV file
merged_data.to_csv('merged_player_team_data.csv', index=False)
