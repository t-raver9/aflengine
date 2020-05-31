from typing import (
    List,
    Dict,
    Type
)
from .resources.columns import (
    match_columns,
    home_team_columns,
    away_team_columns,
    generic_team_columns,
    home_cols_mapped,
    away_cols_mapped
)
import pandas as pd
import numpy as np

class Team:
    """
    Holds team-level data for a particular match
    """
    def __init__(self, generic_team_columns: List, home_or_away: str):
        self.home_or_away = home_or_away
        for column in generic_team_columns:
            setattr(self, column, None)

    def add_data(self, data: pd.DataFrame):
        if self.home_or_away == 'home':
            for home_col, generic_col in home_cols_mapped.items():
                self.__dict__[generic_col] = data[home_col]
        if self.home_or_away == 'away':
            for away_col, generic_col in away_cols_mapped.items():
                self.__dict__[generic_col] = data[away_col]

class Match:
    """
    Holds data about a match, as well as an object for each team
    """
    def __init__(self, match_columns: List):
        self.teams = {
            'home': None,
            'away': None
        }
        for column in match_columns:
            setattr(self, column, None)

    def add_data(self, data: pd.DataFrame):
        for column in self.__dict__.keys():
            try:
                self.__dict__[column] = data[column]
            except KeyError:
                continue
    
    def add_home_team(self, team: Type[Team]):
        self.teams['home'] = team
    
    def add_away_team(self, team: Type[Team]):
        self.teams['away'] = team

class Round:
    """
    Contains match and ladder data for each round
    """
    def __init__(self, round_num: int):
        self.round_num = round_num
        self.matches = []
        self.bye_teams = []
        self.ladder = None

    def add_match(self, match: Type[Match]):
        self.matches.append(match)

    def add_ladder(self, ladder):
        self.ladder = ladder

class Season:
    """
    Contains the rounds for a season, and which teams competed
    """
    def __init__(self, year: int, teams: List):
        self.year = year
        self.teams = teams
        self.rounds = {}
        
    def add_round(self, round_obj: Type[Round]):
        self.rounds[round_obj.round_num] = round_obj

class History:
    """
    Holds all season objects
    """
    def __init__(self):
        self.seasons = {}
        
    def add_season(self, season: Type[Season]):
        self.seasons[season.year] = season


def get_rounds_per_season(matches: pd.DataFrame) -> Dict:
    """
    Creates a dictionary to look up the number of rounds in each season
    """
    seasons = matches['season'].unique()
    rounds_per_season = dict.fromkeys(seasons,0)
    for season in seasons:
        rounds_per_season[season] = max(
            matches[matches['season']==season]['round'])
    return rounds_per_season

def get_teams_in_season(matches: pd.DataFrame) -> Dict:
    """
    Return a dictionary with seasons as keys and a list of teams who played
    in that season as the value
    """
    seasons = matches['season'].unique()
    teams_in_season = {}
    for season in seasons:
        teams = list(matches[matches['season']==season]['hteam'].unique())
        teams.extend(list(matches[matches['season']==season]['ateam'].unique()))
        teams = np.unique(teams)
        teams_in_season[season] = list(teams)
    return teams_in_season

def initialise_history(matches: pd.DataFrame):
    """
    Creates the history object, and initialises it with seasons and rounds
    """
    history = History()
    rounds_per_season = get_rounds_per_season(matches)
    teams_in_season = get_teams_in_season(matches)
    for year in rounds_per_season:
        season = Season(year, teams_in_season[year])
        history.add_season(season)
        for round_num in range(1,rounds_per_season[year]+1):
            round_obj = Round(round_num)
            season.add_round(round_obj)
    return history

def generate_match_object(row: pd.DataFrame):
    """
    Creates a match object (home and away) from a row from the matches dataframe
    """
    home_team = Team(generic_team_columns, 'home')
    away_team = Team(generic_team_columns, 'away')
    home_team.add_data(row)
    away_team.add_data(row)
    match = Match(match_columns)
    match.add_data(row)
    match.add_home_team(home_team)
    match.add_away_team(away_team)
    return match

def add_match_to_history(history: Type[History], row: pd.DataFrame):
    """
    Once every row of dataframe contains a match_obj, we add all match_obj's to
    the history object
    """
    history.seasons[
        row['season']].rounds[row['round']].add_match(row['match_obj'])
    return history