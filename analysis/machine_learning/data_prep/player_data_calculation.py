import pandas as pd
from player_data_classes import Team_player_data, Season, Round_obj, History
from metadata import get_season_teams
from copy import deepcopy

def generate_team_player_data_objects(matches: pd.DataFrame, current_season: int = 1897) -> History:
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

def add_player_data_to_dataset(history: History, matches: pd.DataFrame) -> pd.DataFrame:
    """Takes the history object and adds all relevant player data information,
    aggregated to match level, to the matches dataset. Need to define these manually."""

    # Include all attributes we wish to add to the dataframe
    new_cols = ['AFLfantasy_h_ave', 'Supercoach_h_ave', 'behinds_h_ave',
    'bounces_h_ave', 'brownlow_h_ave', 'clangers_h_ave', 'clearances_h_ave',
    'contested_marks_h_ave', 'contested_poss_h_ave', 'disposals_h_ave',
    'frees_against_h_ave', 'frees_for_h_ave', 'fullkey_h_ave',
    'goal_assists_h_ave', 'goals_h_ave', 'handballs_h_ave', 'hitouts_h_ave',
    'homeAway_h_ave', 'inside50_h_ave', 'kicks_h_ave', 'marks_h_ave',
    'marks_in_50_h_ave', 'matchid_h_ave', 'one_percenters_h_ave',
    'rebound50_h_ave', 'tackles_h_ave', 'team_h_ave', 'uncontested_poss_h_ave',
    'centre_clearances_h_ave', 'disposal_efficiency_h_ave',
    'effective_disposals_h_ave', 'intercepts_h_ave', 'metres_gained_h_ave',
    'stoppage_clearances_h_ave', 'score_involvements_h_ave',
    'tackles_in_50_h_ave', 'turnovers_h_ave',
    'AFLfantasy_a_ave', 'Supercoach_a_ave', 'behinds_a_ave', 'bounces_a_ave',
    'brownlow_a_ave', 'clangers_a_ave', 'clearances_a_ave',
    'contested_marks_a_ave', 'contested_poss_a_ave', 'disposals_a_ave',
    'frees_against_a_ave', 'frees_for_a_ave', 'fullkey_a_ave',
    'goal_assists_a_ave', 'goals_a_ave', 'handballs_a_ave', 'hitouts_a_ave',
    'homeAway_a_ave', 'inside50_a_ave', 'kicks_a_ave', 'marks_a_ave',
    'marks_in_50_a_ave', 'matchid_a_ave', 'one_percenters_a_ave',
    'rebound50_a_ave', 'tackles_a_ave', 'team_a_ave', 'uncontested_poss_a_ave',
    'centre_clearances_a_ave', 'disposal_efficiency_a_ave',
    'effective_disposals_a_ave', 'intercepts_a_ave', 'metres_gained_a_ave',
    'stoppage_clearances_a_ave', 'score_involvements_a_ave',
    'tackles_in_50_a_ave', 'turnovers_a_ave']

    # Initialise
    for col in new_cols:
        matches[col] = None

    current_season = 0
    for idx,row in matches.iterrows():

        if current_season != row['season']:
            print('Writing aggregate player data from {} to dataset'.format(current_season))
            current_season = row['season']

        matches.at[idx,'AFLfantasy_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].AFLfantasy_ave
        matches.at[idx,'Supercoach_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].Supercoach_ave
        matches.at[idx,'behinds_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].behinds_ave
        matches.at[idx,'bounces_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].bounces_ave
        matches.at[idx,'brownlow_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].brownlow_ave
        matches.at[idx,'clangers_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].clangers_ave
        matches.at[idx,'clearances_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].clearances_ave
        matches.at[idx,'contested_marks_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].contested_marks_ave
        matches.at[idx,'contested_poss_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].contested_poss_ave
        matches.at[idx,'disposals_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].disposals_ave
        matches.at[idx,'frees_against_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].frees_against_ave
        matches.at[idx,'frees_for_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].frees_for_ave
        matches.at[idx,'goal_assists_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].goal_assists_ave
        matches.at[idx,'goals_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].goals_ave
        matches.at[idx,'handballs_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].handballs_ave
        matches.at[idx,'hitouts_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].hitouts_ave
        matches.at[idx,'inside50_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].inside50_ave
        matches.at[idx,'kicks_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].kicks_ave
        matches.at[idx,'marks_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].marks_ave
        matches.at[idx,'marks_in_50_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].marks_in_50_ave
        matches.at[idx,'one_percenters_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].one_percenters_ave
        matches.at[idx,'rebound50_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].rebound50_ave
        matches.at[idx,'tackles_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].tackles_ave
        matches.at[idx,'uncontested_poss_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].uncontested_poss_ave
        matches.at[idx,'centre_clearances_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].centre_clearances_ave
        matches.at[idx,'disposal_efficiency_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].disposal_efficiency_ave
        matches.at[idx,'effective_disposals_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].effective_disposals_ave
        matches.at[idx,'intercepts_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].intercepts_ave
        matches.at[idx,'metres_gained_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].metres_gained_ave
        matches.at[idx,'stoppage_clearances_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].stoppage_clearances_ave
        matches.at[idx,'score_involvements_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].score_involvements_ave
        matches.at[idx,'tackles_in_50_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].tackles_in_50_ave
        matches.at[idx,'turnovers_h_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].turnovers_ave

        matches.at[idx,'AFLfantasy_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].AFLfantasy_ave
        matches.at[idx,'Supercoach_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].Supercoach_ave
        matches.at[idx,'behinds_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].behinds_ave
        matches.at[idx,'bounces_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].bounces_ave
        matches.at[idx,'brownlow_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].brownlow_ave
        matches.at[idx,'clangers_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].clangers_ave
        matches.at[idx,'clearances_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].clearances_ave
        matches.at[idx,'contested_marks_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].contested_marks_ave
        matches.at[idx,'contested_poss_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].contested_poss_ave
        matches.at[idx,'disposals_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].disposals_ave
        matches.at[idx,'frees_against_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].frees_against_ave
        matches.at[idx,'frees_for_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].frees_for_ave
        matches.at[idx,'goal_assists_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].goal_assists_ave
        matches.at[idx,'goals_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].goals_ave
        matches.at[idx,'handballs_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].handballs_ave
        matches.at[idx,'hitouts_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].hitouts_ave
        matches.at[idx,'inside50_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].inside50_ave
        matches.at[idx,'kicks_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].kicks_ave
        matches.at[idx,'marks_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].marks_ave
        matches.at[idx,'marks_in_50_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].marks_in_50_ave
        matches.at[idx,'one_percenters_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].one_percenters_ave
        matches.at[idx,'rebound50_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].rebound50_ave
        matches.at[idx,'tackles_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].tackles_ave
        matches.at[idx,'uncontested_poss_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].uncontested_poss_ave
        matches.at[idx,'centre_clearances_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].centre_clearances_ave
        matches.at[idx,'disposal_efficiency_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].disposal_efficiency_ave
        matches.at[idx,'effective_disposals_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].effective_disposals_ave
        matches.at[idx,'intercepts_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].intercepts_ave
        matches.at[idx,'metres_gained_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].metres_gained_ave
        matches.at[idx,'stoppage_clearances_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].stoppage_clearances_ave
        matches.at[idx,'score_involvements_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].score_involvements_ave
        matches.at[idx,'tackles_in_50_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].tackles_in_50_ave
        matches.at[idx,'turnovers_a_ave'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].turnovers_ave

    # Reset the index, which is now jumbled and meaningless
    matches.reset_index(drop=True,inplace=True)
    return matches