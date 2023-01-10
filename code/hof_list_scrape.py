#### Get clean list of NBA Hall of Famers

# Libraries
import pandas as pd 

# Import table from basketball-reference.com
hof_table = pd.read_csv("../data/basketball_reference_hof_table.csv")
print(hof_table)

# Filter HOF inductees (* means already inducted into HOF)
hof_players = hof_table[hof_table['Player'].str.contains("\*")]
print(hof_players)

# Remove * from player names
hof_players = hof_players['Player'].str[:-1]
print(hof_players)

# Save cleaned list as CSV
hof_players.to_csv("../data/hof_players.csv", index = False)

# Check list of HOF players
hof_players = pd.read_csv("../data/hof_players.csv")
print(hof_players)