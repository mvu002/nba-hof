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
#print(combined_data)

# Add "numAllStarsAppearances" feature
# Unfortunately, we could not find a way to get # of all-star appearances through the API, so we had to find
# a different source of the information (https://www.basketball-reference.com/awards/all_star_by_player.html) 
# and merge it afterwards. 

# Import and clean CSV of NBA all-stars (from basketball-reference.com)
allstars = pd.read_csv("../data/allstars.csv")
allstars = allstars[allstars['NBA'] != '0']
allstars = allstars[["Player", "NBA"]]
allstars = allstars[allstars["Player"] != 'Player']
#print(allstars)

# Identify names of all-stars from basketball-reference that are NOT recognized by the API
from nba_api.stats.static import players
nba_players = players.get_players()
for name in allstars['Player']:
	if (pd.DataFrame(nba_players)['full_name'] == name).any() == False:
		print(name)

# Create list of names of all-stars with aliases recognized by the API
allstars_aliases = pd.Series(["Jojo White", "Nate Archibald", "Nikola Jokic", "Luka Doncic", "Johnny Kerr",
							  "Peja Stojakovic", "Frank Brian", "Thomas Eddleman", "Manu Ginobili", "Rod Hundley",
							  "Lafayette Lever", "Freddie Scolari", "Ken Sears", "Nikola Vucevic", "Goran Dragic",
							  "World Free", "Billy Gabor", "Kristaps Porzingis", "Steven Smith"])

# Change names in basketball-reference all-stars table to aliases recognized by the API
basketball_reference_allstar_names = []
for name in allstars['Player']:
	if (pd.DataFrame(nba_players)['full_name'] == name).any() == False:
		basketball_reference_allstar_names.append(name)

i = 0 
while i < len(basketball_reference_allstar_names):
	allstars = allstars.replace(basketball_reference_allstar_names[i], allstars_aliases[i])
	i += 1

allstars_profiles = [player for player in nba_players
					        if (allstars['Player'] == (player['full_name'])).any()
					        or (allstars_aliases == (player['full_name'])).any()]

allstars_profiles = pd.DataFrame(allstars_profiles)
#print(allstars_profiles)

# Check for duplicates in all-stars dataframe
allstar_duplicates = allstars_profiles[allstars_profiles['full_name'].duplicated(keep = False)]
#print(allstar_duplicates)

# Remove duplicates from all-stars dataframe
allstars_profiles = allstars_profiles[allstars_profiles["id"].isin([201607, 77144, 77156, 200784, 77818, 203318, 200848]) == False]
allstars_profiles = allstars_profiles.sort_values(by = "full_name").reset_index(drop = True)
#print(allstars_profiles)

# Create table of NBA all-stars
allstars_profiles['numAllStarAppearances'] = allstars.sort_values("Player")['NBA'].reset_index(drop = True)
allstars_profiles = allstars_profiles[['id', 'full_name', 'numAllStarAppearances']]
print(allstars_profiles)

# Add "numAllStarAppearances" to HOF stats dataframe
hof_stats_with_allstar = pd.merge(allstars_profiles, hof_players_median_stats, left_on = "id", right_on = "PLAYER_ID", how = "inner")
hof_stats_with_allstar = hof_stats_with_allstar.rename(columns = {"id" : "PLAYER_ID"})
hof_stats_with_allstar = hof_stats_with_allstar.set_index("PLAYER_ID")
#print(hof_stats_with_allstar)

# Identify HOF players who have 0 all-star appearances
for name in hof_player_profiles['full_name'].unique():
	if (name in hof_stats_with_allstar['full_name'].unique()) == False:
		print(name)

# Extract profiles of HOF players who have 0 all-star appearances
hof_names_without_allstar = ['K.C. Jones', 'Don Nelson', 'Frank Ramsey', 'Thomas Sanders']
hof_stats_without_allstar = hof_player_profiles[hof_player_profiles['full_name'].isin(hof_names_without_allstar)]
hof_stats_without_allstar = hof_players_stats[hof_players_stats['PLAYER_ID'].isin(hof_stats_without_allstar['id'])]

hof_stats_without_allstar = hof_stats_without_allstar.drop(columns = ['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION',
																	  'PLAYER_AGE'])
hof_stats_without_allstar = hof_stats_without_allstar.groupby(by = "PLAYER_ID").median()
hof_stats_without_allstar['numAllStarAppearances'] = 0
hof_stats_without_allstar['isHOF'] = 1

# Create combined dataframe of all HOF players and their # of all-star appearances
hof_stats_all = hof_stats_with_allstar.append(hof_stats_without_allstar)
final_data = hof_stats_all.append(non_hof_players_median_stats)
final_data['numAllStarAppearances'] = final_data['numAllStarAppearances'].fillna(0)
final_data = final_data.drop(columns = ['full_name'])
final_data['numAllStarAppearances'] = final_data['numAllStarAppearances'].astype(float)
print(final_data)

final_data.to_csv("../data/final_data.csv")