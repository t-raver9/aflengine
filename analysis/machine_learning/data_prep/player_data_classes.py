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
        self.behinds = 0
        self.bounces = 0
        self.brownlow = 0
        self.clangers = 0
        self.clearances = 0
        self.contested_marks = 0
        self.contested_poss = 0
        self.disposals = 0
        self.frees_against = 0
        self.frees_for = 0
        self.fullkey = 0
        self.goal_assists = 0
        self.goals = 0
        self.handballs = 0
        self.hitouts = 0
        self.homeAway = 0
        self.inside50 = 0
        self.kicks = 0
        self.marks = 0
        self.marks_in_50 = 0
        self.matchid = 0
        self.one_percenters = 0
        self.rebound50 = 0
        self.tackles = 0
        self.team = 0
        self.uncontested_poss = 0
        self.centre_clearances = 0
        self.disposal_efficiency = 0
        self.effective_disposals = 0
        self.intercepts = 0
        self.metres_gained = 0
        self.stoppage_clearances = 0
        self.score_involvements = 0
        self.tackles_in_50 = 0
        self.turnovers = 0
        self.AFLfantasy_ave = 0
        self.Supercoach_ave = 0
        self.behinds_ave = 0
        self.bounces_ave = 0
        self.brownlow_ave = 0
        self.clangers_ave = 0
        self.clearances_ave = 0
        self.contested_marks_ave = 0
        self.contested_poss_ave = 0
        self.disposals_ave = 0
        self.frees_against_ave = 0
        self.frees_for_ave = 0
        self.goal_assists_ave = 0
        self.goals_ave = 0
        self.handballs_ave = 0
        self.hitouts_ave = 0
        self.inside50_ave = 0
        self.kicks_ave = 0
        self.marks_ave = 0
        self.marks_in_50_ave = 0
        self.one_percenters_ave = 0
        self.rebound50_ave = 0
        self.tackles_ave = 0
        self.uncontested_poss_ave = 0
        self.centre_clearances_ave = 0
        self.disposal_efficiency_ave = 0
        self.effective_disposals_ave = 0
        self.intercepts_ave = 0
        self.metres_gained_ave = 0
        self.stoppage_clearances_ave = 0
        self.score_involvements_ave = 0
        self.tackles_in_50_ave = 0
        self.turnovers_ave = 0

    def update_h_team_player_data(self,match_data: pd.DataFrame) -> None:
        self.played += 1
        self.AFLfantasy += match_data['AFLfantasy_h']
        self.Supercoach += match_data['Supercoach_h']
        self.behinds += match_data['behinds_h']
        self.bounces += match_data['bounces_h']
        self.brownlow += match_data['brownlow_h']
        self.clangers += match_data['clangers_h']
        self.clearances += match_data['clearances_h']
        self.contested_marks += match_data['contested_marks_h']
        self.contested_poss += match_data['contested_poss_h']
        self.disposals += match_data['disposals_h']
        self.frees_against += match_data['frees_against_h']
        self.frees_for += match_data['frees_for_h']
        self.goal_assists += match_data['goal_assists_h']
        self.goals += match_data['goals_h']
        self.handballs += match_data['handballs_h']
        self.hitouts += match_data['hitouts_h']
        self.inside50 += match_data['inside50_h']
        self.kicks += match_data['kicks_h']
        self.marks += match_data['marks_h']
        self.marks_in_50 += match_data['marks_in_50_h']
        self.one_percenters += match_data['one_percenters_h']
        self.rebound50 += match_data['rebound50_h']
        self.tackles += match_data['tackles_h']
        self.uncontested_poss += match_data['uncontested_poss_h']
        self.centre_clearances += match_data['centre_clearances_h']
        self.disposal_efficiency += match_data['disposal_efficiency_h']
        self.effective_disposals += match_data['effective_disposals_h']
        self.intercepts += match_data['intercepts_h']
        self.metres_gained += match_data['metres_gained_h']
        self.stoppage_clearances += match_data['stoppage_clearances_h']
        self.score_involvements += match_data['score_involvements_h']
        self.tackles_in_50 += match_data['tackles_in_50_h']
        self.turnovers += match_data['turnovers_h']
        self.update_averages()

    def update_a_team_player_data(self,match_data: pd.DataFrame) -> None:
        self.played += 1
        self.AFLfantasy += match_data['AFLfantasy_a']
        self.Supercoach += match_data['Supercoach_a']
        self.behinds += match_data['behinds_a']
        self.bounces += match_data['bounces_a']
        self.brownlow += match_data['brownlow_a']
        self.clangers += match_data['clangers_a']
        self.clearances += match_data['clearances_a']
        self.contested_marks += match_data['contested_marks_a']
        self.contested_poss += match_data['contested_poss_a']
        self.disposals += match_data['disposals_a']
        self.frees_against += match_data['frees_against_a']
        self.frees_for += match_data['frees_for_a']
        self.goal_assists += match_data['goal_assists_a']
        self.goals += match_data['goals_a']
        self.handballs += match_data['handballs_a']
        self.hitouts += match_data['hitouts_a']
        self.inside50 += match_data['inside50_a']
        self.kicks += match_data['kicks_a']
        self.marks += match_data['marks_a']
        self.marks_in_50 += match_data['marks_in_50_a']
        self.one_percenters += match_data['one_percenters_a']
        self.rebound50 += match_data['rebound50_a']
        self.tackles += match_data['tackles_a']
        self.uncontested_poss += match_data['uncontested_poss_a']
        self.centre_clearances += match_data['centre_clearances_a']
        self.disposal_efficiency += match_data['disposal_efficiency_a']
        self.effective_disposals += match_data['effective_disposals_a']
        self.intercepts += match_data['intercepts_a']
        self.metres_gained += match_data['metres_gained_a']
        self.stoppage_clearances += match_data['stoppage_clearances_a']
        self.score_involvements += match_data['score_involvements_a']
        self.tackles_in_50 += match_data['tackles_in_50_a']
        self.turnovers += match_data['turnovers_a']
        self.update_averages()

    def update_averages(self):
        self.AFLfantasy_ave = self.AFLfantasy/self.played
        self.Supercoach_ave = self.Supercoach/self.played
        self.behinds_ave = self.behinds/self.played
        self.bounces_ave = self.bounces/self.played
        self.brownlow_ave = self.brownlow/self.played
        self.clangers_ave = self.clangers/self.played
        self.clearances_ave = self.clearances/self.played
        self.contested_marks_ave = self.contested_marks/self.played
        self.contested_poss_ave = self.contested_poss/self.played
        self.disposals_ave = self.disposals/self.played
        self.frees_against_ave = self.frees_against/self.played
        self.frees_for_ave = self.frees_for/self.played
        self.goal_assists_ave = self.goal_assists/self.played
        self.goals_ave = self.goals/self.played
        self.handballs_ave = self.handballs/self.played
        self.hitouts_ave = self.hitouts/self.played
        self.inside50_ave = self.inside50/self.played
        self.kicks_ave = self.kicks/self.played
        self.marks_ave = self.marks/self.played
        self.marks_in_50_ave = self.marks_in_50/self.played
        self.one_percenters_ave = self.one_percenters/self.played
        self.rebound50_ave = self.rebound50/self.played
        self.tackles_ave = self.tackles/self.played
        self.uncontested_poss_ave = self.uncontested_poss/self.played
        self.centre_clearances_ave = self.centre_clearances/self.played
        self.disposal_efficiency_ave = self.disposal_efficiency/self.played
        self.effective_disposals_ave = self.effective_disposals/self.played
        self.intercepts_ave = self.intercepts/self.played
        self.metres_gained_ave = self.metres_gained/self.played
        self.stoppage_clearances_ave = self.stoppage_clearances/self.played
        self.score_involvements_ave = self.score_involvements/self.played
        self.tackles_in_50_ave = self.tackles_in_50/self.played
        self.turnovers_ave = self.turnovers/self.played

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