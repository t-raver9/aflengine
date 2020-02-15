import pandas as pd

class Team_player_data():
    """
    Class for storing player data for teams throughout seasons
    """
    def __init__(self,team: str):
        self.team = team
        self.played = 0
        self.byes = 0
        self.bye_rounds = []
        self.AFLfantasy = 0
        self.Supercoach = 0
        self.AFLfantasy_ave = 0
        self.Supercoach_ave = 0

    def update_h_team_player_data(self,match_data: pd.DataFrame) -> None:
        self.played += 1
        self.AFLfantasy += match_data['AFLfantasy_h']
        self.Supercoach += match_data['Supercoach_h']
        self.update_averages()

    def update_a_team_player_data(self,match_data: pd.DataFrame) -> None:
        self.played += 1
        self.AFLfantasy += match_data['AFLfantasy_h']
        self.Supercoach += match_data['Supercoach_h']
        self.update_averages()

    def update_averages(self):
        self.AFLfantasy_ave = self.AFLfantasy/self.played
        self.Supercoach_ave = self.Supercoach/self.played

    def add_bye_round(self,round_num):
        self.bye_rounds.append(round_num)
        self.byes += 1

class Season():
    """
    Class for storing all rounds and teams in a season
    """
    def __init__(self,season,teams):
        self.season = season
        self.teams = teams
        self.rounds = {}
        
    def add_round(self,round_obj,round_num):
        self.rounds[round_num] = round_obj

class Round_obj():
    """
    Class for storing all team player information for each team in a round. "teams"
    holds the names of teams playing in the relevant season. "team_player_data"
    holds the player data objects for each team as values, and team names as keys
    """
    def __init__(self,round_num,teams):
        self.round_num = round_num
        self.teams = teams
        self.team_player_data = {}
        
    def add_team_player_info(self,team,team_player_data_obj):
        self.team_player_data[team] = team_player_data_obj

class History():
    """
    Holds every season year as key, and season objects as values.
    """
    def __init__(self):
        self.seasons = {}
        
    def add_season(self,season_obj):
        self.seasons[season_obj.season] = season_obj