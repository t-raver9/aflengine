# pylint: disable=no-member
import pickle
import os
import sys
import operator
from typing import (
    Type,
    List
)
from os.path import (
    dirname,
    abspath
)
from .resources.columns import ladder_columns
from ..match_data.generate_match_objects import (
    Team,
    Match,
    History
)
from ..match_data.resources.columns import generic_team_columns
from copy import deepcopy

src_path = dirname(dirname(abspath(__file__)))
history_path = src_path + "/match_data/data/history_object.pk1"

class TeamLadder:
    def __init__(self, team: str):
        self.team = team
        for column, init_val in ladder_columns:
            setattr(self, column, init_val)

    def add_prev_round_team_ladder(self, prev_round_team_ladder):
        for col,val in prev_round_team_ladder.items():
            self.__dict__[col] = val

    def update_home_team(self, match: Type[Match]):
        self.played += 1
        if match.hscore > match.ascore:
            self.wins += 1
            self.prem_points += 4
        elif match.hscore == match.ascore:
            self.draws += 1
            self.prem_points += 2
        else:
            self.losses += 1    
        self.points_for += match.hscore
        self.points_against += match.ascore
        self.percentage = 100 * (self.points_for / self.points_against)

    def update_away_team(self, match: Type[Match]):
        self.played += 1
        if match.hscore < match.ascore:
            self.wins += 1
            self.prem_points += 4
        elif match.hscore == match.ascore:
            self.draws += 1
            self.prem_points += 2
        else:
            self.losses += 1    
        self.points_for += match.ascore
        self.points_against += match.hscore
        self.percentage = 100 * (self.points_for / self.points_against)

    def update_ladder(self, match: Type[Match]):
        """
        Update the ladder for the team based on the outcome of the game. There
        will be two possibilites - the team can be the home or the away team
        in the provided match.
        """
        if self.team == match.teams['home']:
            self.update_home_team(match)
        else:
            self.update_away_team(match)

class Ladder:
    """
    Each round object holds the ladder details for that round for each team
    """
    def __init__(self, teams_in_season: List):
        self.teams_in_season = teams_in_season
        self.team_ladders = {}

    def add_team_ladder(self, team_ladder: Type[TeamLadder]):
        self.team_ladders[team_ladder.team.team] = team_ladder


def import_history():
    with open(history_path, 'rb') as f:
        history = pickle.load(f)
    return history

def sort_ladder(ladder: Type[Ladder]):
    """
    Takes an unordered ladder object and sorts each team by position
    """
    # Read each team ladder object into a list
    team_ladders = [team_ladder for team_ladder in ladder.team_ladders.values()]
    # Sort these by points, then percentage, then points for
    team_ladders.sort(key=operator.attrgetter(
        'prem_points','percentage','points_for'),reverse=True)
    # Assign positions accordingly
    i = 1
    while i <= len(team_ladders):
        team_ladders[i-1].position = i
        i += 1
    # Reassign these to the ladder object
    ladder.team_ladders = {}
    for team_ladder in team_ladders:
        ladder.add_team_ladder(team_ladder)
    return ladder

def create_ladders(history: Type[History]):
    for season in history.seasons.values():
        for round_obj in season.rounds.values():
            ladder = Ladder(season.teams)
            round_obj.add_ladder(ladder)
            # Track which teams we've seen, in case there's a bye round
            not_seen = season.teams[:]
            for match in round_obj.matches:
                for team in match.teams.values():
                    # Remove team from not_seen
                    not_seen.remove(team.team)
                    # Get ladder
                    if round_obj.round_num != 1:
                        team_ladder = deepcopy(history.seasons[season.year].rounds[
                            round_obj.round_num - 1].ladder.team_ladders[team.team])
                    else:
                        team_ladder = TeamLadder(team)
                    # Update ladder for this round
                    if match.teams['home'] == team:
                        team_ladder.update_home_team(match)
                    else:
                        team_ladder.update_away_team(match)
                    # Add team ladder to the ladder object
                    ladder.add_team_ladder(team_ladder)
            # If there was a bye for a team, set the ladder to the previous
            # round. If the bye was in round one, initialise the ladder first
            for team_name in not_seen:
                team = Team(generic_team_columns,'home')
                team.team = team_name
                if round_obj.round_num == 1:
                    team_ladder = TeamLadder(team)
                else:
                    team_ladder = deepcopy(history.seasons[season.year].rounds[
                        round_obj.round_num - 1].ladder.team_ladders[team.team])
                ladder.add_team_ladder(team_ladder)
            # Sort the ladder for the round
            ladder = sort_ladder(ladder)
    return history

def save_history_with_ladders(history: Type[History]):
    d = os.path.dirname(os.path.abspath(__file__))
    with open(d + '/data/history_object.pk1','wb') as output:
        pickle.dump(history, output)
    return None

def add_ladders_to_history():
    history = import_history()
    history_with_ladders = create_ladders(history)
    save_history_with_ladders(history)
    return history_with_ladders