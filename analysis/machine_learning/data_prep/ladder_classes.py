class Team_ladder_info():
    """
    Class that holds all ladder data for teams, and methods to update this data
    """
    def __init__(self,team):
        self.team = team
        self.prem_points = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.points_for = 0
        self.points_against = 0
        self.percentage = 100
        self.ladder_position = 1
        self.played = 0
        self.byes = 0
        self.bye_rounds = []
        self.won_game = 0
        self.points_for_game = 0
        self.points_against_game = 0
        
    def update_ladder_info(self,match_data):
        if self.team == match_data['hteam']:
            self.update_home_team(match_data)
        elif self.team == match_data['ateam']:
            self.update_away_team(match_data)
            
    def update_home_team(self,match_data):
        if match_data['hscore'] > match_data['ascore']:
            self.prem_points += 4
            self.wins += 1
            self.won_game = 1
        elif match_data['hscore'] == match_data['ascore']:
            self.prem_points += 2
            self.draws += 1
            self.won_game = .5
        else:
            self.losses += 1
            self.won_game = 0

        self.points_for += match_data['hscore']
        self.points_against += match_data['ascore']
        self.played += 1

        self.points_for_game = match_data['hscore']
        self.points_against_game = match_data['ascore']

        self.update_percentage()
    
    def update_away_team(self,match_data):
        if match_data['hscore'] < match_data['ascore']:
            self.prem_points += 4
            self.wins += 1
            self.won_game = 1
        elif match_data['hscore'] == match_data['ascore']:
            self.prem_points += 2
            self.draws += 1
            self.won_game = .5
        else:
            self.losses += 1
            self.won_game = 0
        
        self.points_for += match_data['ascore']
        self.points_against += match_data['hscore']
        self.played += 1

        self.points_for_game = match_data['ascore']
        self.points_against_game = match_data['hscore']
        
        self.update_percentage()
    
    def update_percentage(self):
        try:
            self.percentage = 100*(self.points_for/self.points_against)
        except ZeroDivisionError:
            pass
        
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
    Class for storing all ladder information for each team in a round. "teams"
    holds the names of teams playing in the relevant season. "teams_ladder_info"
    holds the ladder objects for each team as values, and team names as keys
    """
    def __init__(self,round_num,teams):
        self.round_num = round_num
        self.teams = teams
        self.teams_ladder_info = {}
        
    def add_ladder_info(self,team,team_ladder_info_obj):
        self.teams_ladder_info[team] = team_ladder_info_obj

class History():
    """
    Holds every season year as key, and season objects as values.
    """
    def __init__(self):
        self.seasons = {}
        
    def add_season(self,season_obj):
        self.seasons[season_obj.season] = season_obj