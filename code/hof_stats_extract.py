#### Extract stats of HOF players

# Libraries (pip install nba_api in terminal)
import nba_api
import pandas as pd

# Import table of HOF players
hof_players = pd.read_csv("../data/hof_players.csv")
#print(hof_players)

# Use API to get list of all NBA players (past & present)
from nba_api.stats.static import players
nba_players = players.get_players()
#print(nba_players[:3])

# Check for HOF players whose names are NOT recognized by the API
for name in hof_players['Player']:
	if (pd.DataFrame(nba_players)['full_name'] == name).any() == False:
		print(name)

# The players printed above have nicknames or names with accents that the NBA API does not recognize. 
# To account for this, we must create a list of their aliases that the API recognizes. 
hof_players_aliases = pd.Series(["Nate Archibald", "Jojo White", "Manu Ginobili", "Thomas Sanders"])
#print(hof_players_aliases)

# Extract list of HOF players from the API
hof_players_profiles = [player for player in nba_players
						if (hof_players['Player'] == (player['full_name'])).any()
						or (hof_players_aliases == (player['full_name'])).any()]
hof_players_profiles = pd.DataFrame(hof_players_profiles)
#print(hof_players_profiles)

# Check for duplicates
hof_duplicates = hof_players_profiles[hof_players_profiles['full_name'].duplicated(keep = False)]
#print(hof_duplicates)

# Determine the API IDs that correspond to HOF players
from nba_api.stats.endpoints import playercareerstats
patrick_ewing = playercareerstats.PlayerCareerStats(player_id = "121")
#print(patrick_ewing.get_data_frames()[0])

patrick_ewing_jr = playercareerstats.PlayerCareerStats(player_id = "201607")
#print(patrick_ewing_jr.get_data_frames()[0])

bobby_jones_hof = playercareerstats.PlayerCareerStats(player_id = "77193")
#print(bobby_jones_hof.get_data_frames()[0])

bobby_jones_not_hof = playercareerstats.PlayerCareerStats(player_id = "200784")
#print(bobby_jones_not_hof.get_data_frames()[0])

# Remove IDs that correspond with non-HOF players
hof_player_profiles = hof_players_profiles[hof_players_profiles["id"].isin([201607, 200784]) == False]
#print(hof_players_profiles)

# Use the "id" column to extract the stats of HOF players from the API 
# (Takes about 7 minutes to run, make sure to save to CSV after running)

# hof_players_stats = pd.DataFrame()
# for id in hof_players_profiles["id"].apply(str):
# 	stats = playercareerstats.PlayerCareerStats(player_id = id)
# 	hof_players_stats = hof_players_stats.append(stats.get_data_frames()[0])

# print(hof_players_stats)
# print(len(hof_players_stats["PLAYER_ID"].unique()))
# hof_players_stats.to_csv("../data/hof_player_stats.csv", index = False)

hof_players_stats = pd.read_csv("../data/hof_player_stats.csv")
print(hof_players_stats)