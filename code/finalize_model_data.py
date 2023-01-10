#### Create dataframe of stats of HOFs and non-HOFs

# Libraries
import pandas as pd

# Extract stats of all players from API 
all_players_stats = pd.read_csv("../data/all_players_stats.csv")
#print(all_players_stats)

# Create separate table for stats of non-HOF players
hof_player_profiles = pd.read_csv("../data/hof_players_profiles.csv")
non_hof_players_stats = all_players_stats[all_players_stats['PLAYER_ID'].isin(hof_player_profiles["id"]) == False]
#print(non_hof_players_stats)