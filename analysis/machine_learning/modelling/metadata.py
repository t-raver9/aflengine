import pandas as pd
import numpy as np
from typing import Dict

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