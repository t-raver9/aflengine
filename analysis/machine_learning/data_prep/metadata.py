import pandas as pd
import numpy as np
from typing import List, Dict

def get_season_rounds(matches: pd.DataFrame) -> Dict:
    """
    Return a dictionary with seasons as keys and number of games
    in season as values
    """
    seasons = matches['season'].unique()
    rounds_in_season = dict.fromkeys(seasons,0)
    
    for season in seasons:
        rounds_in_season[season] = max(matches[matches['season']==season]['round'])
    
    return rounds_in_season

# What teams participated in each season?
def get_season_teams(matches: pd.DataFrame) -> Dict:
    """
    Return a dictionary with seasons as keys and a list of teams who played
    in that season as values
    """
    seasons = matches['season'].unique()
    teams_in_season = {}

    for season in seasons:
        teams = list(matches[matches['season']==season]['hteam'].unique())
        teams.extend(list(matches[matches['season']==season]['ateam'].unique()))
        teams = np.unique(teams)
        teams_in_season[season] = list(teams)
        
    return teams_in_season

# What are the home grounds of each team for each season?
"""
Dictionary with teams as keys and a list of home
grounds as values. Historically there are far more grounds -
will include this later. For now, use this only for after
2000.
"""
home_grounds = {
    'St Kilda':['Docklands'],
    'Carlton': ['M.C.G.','Docklands','Princes Park'],
    'Hawthorn': ['M.C.G.','York Park'],
    'Footscray': ['Docklands','Eureka Stadium'],
    'Fitzroy': [],
    'Geelong': ['Kardinia Park'],
    'Essendon': ['M.C.G.','Docklands'],
    'Richmond': ['M.C.G.'],
    'Melbourne': ['M.C.G.','Traeger Park'],
    'Collingwood': ['M.C.G.'],
    'West Coast': ['Perth Stadium','Subiaco','W.A.C.A'],
    'North Melbourne': ['Docklands','Bellerive Oval'],
    'Sydney': ['S.C.G.'],
    'Port Adelaide': ['Adelaide Oval','Football Park'],
    'Adelaide': ['Adelaide Oval','Jiangwan Stadium','Football Park'],
    'Brisbane Lions': ['Gabba'],
    'Greater Western Sydney': ['Sydney Showground'],
    'South Melbourne': [],
    'University': [],
    'Fremantle': ['Perth Stadium','Subiaco','W.A.C.A'],
    'Gold Coast': ['Carrara'],
    'Brisbane Bears': []
}