import pandas as pd
from player_data_classes import Team_player_data, Season, Round_obj, History
from metadata import get_season_teams
from copy import deepcopy

def generate_team_player_data_objects(matches: pd.DataFrame, current_season: int = 2000) -> History:
    """
    Takes the matches dataframe and creates a "History" object that contains
    all of the aggregated individual stats throughout a season. The heirachy
    of objects is history -> season -> round -> team_player_data.

    A "Round 0" ladder is also created with all teams starting on equal stats. 
    This data will be required for features of round 1 games.
    """

    teams_in_season = get_season_teams(matches)
    history = History()
    current_season = current_season - 1 # Need to take it back one year to trigger the first clause

    for _,row in matches.iterrows():
        # Conditions for a new season beginning. Need to populate ladder for before season, i.e. Round Zero
        if current_season != row['season']:
            current_season = row['season']
            current_round = 0

            # Create the initial round object with the list of teams for that season
            current_round_obj = Round_obj(round_num=current_round,teams=teams_in_season[current_season])
            
            # Insert this into a new season object created for the start of the season
            season_obj = Season(season=current_season,teams=teams_in_season[current_season])
            season_obj.add_round(current_round_obj,current_round)
            print("Created Season Object {}".format(current_season))

            # Add this season to the history
            history.add_season(season_obj)

            # Add the "team player data round zero" objects, i.e. the default data
            # before the season starts
            for team in teams_in_season[current_season]:
                team_player_data_info = Team_player_data(team)
                current_round_obj.add_team_player_info(team,team_player_data_info)

            # Start with empty teams not seen for initialisation
            teams_not_seen = []

            # Create round object when we start a new round
        if (row['round'] != current_round):

            # Before creating a new round object, add objects for the previous round for any bye teams
            for bye_team in teams_not_seen:
                bye_team_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].team_player_data[bye_team])
                bye_team_info.add_bye_round(current_round)
                current_round_obj.add_team_player_info(bye_team,bye_team_info)
            
            # Add this round object to the season object
            current_round = row['round']
            current_round_obj = Round_obj(round_num=current_round,teams=teams_in_season[current_season])
            season_obj.add_round(current_round_obj,current_round)
            
            #Track which teams have played this round so we know when a bye has occured
            teams_not_seen = [team for team in season_obj.teams]

        # For the teams in the match, inherit the previous round's team data
        # and update it
        home_team_player_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].team_player_data[row['hteam']])
        away_team_player_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].team_player_data[row['ateam']])
        home_team_player_info.update_h_team_player_data(match_data=row)
        away_team_player_info.update_a_team_player_data(match_data=row)
        current_round_obj.add_team_player_info(row['hteam'],home_team_player_info)
        current_round_obj.add_team_player_info(row['ateam'],away_team_player_info)

        # Append teams to the teams seen list so we know when byes are occuring
        teams_not_seen.remove(row['hteam'])
        teams_not_seen.remove(row['ateam'])

        # Track the round so we know when to create a new round object
        current_round = row['round']

    return history