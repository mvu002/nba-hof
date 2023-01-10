#### Extract stats of HOF players

# Libraries (pip install nba_api in terminal)
import nba_api
import pandas as pd

# Import table of HOF players
hof_players = pd.read_csv("../data/hof_players.csv")
print(hof_players)