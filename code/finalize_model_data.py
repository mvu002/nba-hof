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

# Aggregate median of each non-HOF players' stats
non_hof_players_median_stats = non_hof_players_stats.drop(columns = ['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION',
																	 'PLAYER_AGE'])
non_hof_players_median_stats = non_hof_players_median_stats.groupby(by = "PLAYER_ID").median()
#print(non_hof_players_median_stats)

# Aggregate median of each HOF players' stats
hof_players_stats = pd.read_csv("../data/hof_player_stats.csv")
hof_players_median_stats = hof_players_stats.drop(columns = ['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION',
															 'PLAYER_AGE'])
hof_players_median_stats = hof_players_median_stats.groupby(by = "PLAYER_ID").median()
#print(hof_players_median_stats)

# Add "isHOF" variable to dataframe of HOF stats, set every value = 1
hof_players_median_stats['isHOF'] = 1

# Add "isHOF" variable to dataframe of non-HOF stats, set every value = 0 
non_hof_players_median_stats['isHOF'] = 0 

# Combine HOF and non-HOF stats dataframes together
combined_data = hof_players_median_stats.append(non_hof_players_median_stats)
combined_data.to_csv("../data/all_players_median_stats.csv")
print(combined_data)