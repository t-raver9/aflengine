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

def add_player_data_to_dataset(history: History, matches: pd.DataFrame) -> pd.DataFrame:
    """Takes the history object and adds all relevant player data information,
    aggregated to match level, to the matches dataset. Need to define these manually."""

    # Include all attributes we wish to add to the dataframe
    new_cols = ['AFLfantasy_h', 'Supercoach_h', 'behinds_h', 'bounces_h',
    'brownlow_h', 'clangers_h', 'clearances_h', 'contested_marks_h',
    'contested_poss_h', 'disposals_h', 'frees_against_h', 'frees_for_h',
    'goal_assists_h', 'goals_h', 'handballs_h', 'hitouts_h',
    'homeAway_h', 'inside50_h', 'kicks_h', 'marks_h', 'marks_in_50_h',
    'matchid_h', 'one_percenters_h', 'rebound50_h', 'tackles_h', 'team_h',
    'uncontested_poss_h', 'centre_clearances_h', 'disposal_efficiency_h',
    'effective_disposals_h', 'intercepts_h', 'metres_gained_h',
    'stoppage_clearances_h', 'score_involvements_h', 'tackles_in_50_h',
    'turnovers_h','AFLfantasy_a', 'Supercoach_a', 'behinds_a', 'bounces_a',
    'brownlow_a', 'clangers_a', 'clearances_a', 'contested_marks_a',
    'contested_poss_a', 'disposals_a', 'frees_against_a', 'frees_for_a',
    'goal_assists_a', 'goals_a', 'handballs_a', 'hitouts_a',
    'homeAway_a', 'inside50_a', 'kicks_a', 'marks_a', 'marks_in_50_a',
    'matchid_a', 'one_percenters_a', 'rebound50_a', 'tackles_a', 'team_a',
    'uncontested_poss_a', 'centre_clearances_a', 'disposal_efficiency_a',
    'effective_disposals_a', 'intercepts_a', 'metres_gained_a',
    'stoppage_clearances_a', 'score_involvements_a', 'tackles_in_50_a',
    'turnovers_a']

    # Initialise
    for col in new_cols:
        matches[col] = None

    current_season = 0
    for idx,row in matches.iterrows():

        if current_season != row['season']:
            print('Writing aggregate player data from {} to dataset'.format(current_season))
            current_season = row['season']

    matches.at[idx,'AFLfantasy_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].AFLfantasy_ave
    matches.at[idx,'Supercoach_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].Supercoach_ave
    matches.at[idx,'behinds_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].behinds_ave
    matches.at[idx,'bounces_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].bounces_ave
    matches.at[idx,'brownlow_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].brownlow_ave
    matches.at[idx,'clangers_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].clangers_ave
    matches.at[idx,'clearances_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].clearances_ave
    matches.at[idx,'contested_marks_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].contested_marks_ave
    matches.at[idx,'contested_poss_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].contested_poss_ave
    matches.at[idx,'disposals_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].disposals_ave
    matches.at[idx,'frees_against_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].frees_against_ave
    matches.at[idx,'frees_for_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].frees_for_ave
    matches.at[idx,'goal_assists_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].goal_assists_ave
    matches.at[idx,'goals_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].goals_ave
    matches.at[idx,'handballs_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].handballs_ave
    matches.at[idx,'hitouts_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].hitouts_ave
    matches.at[idx,'inside50_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].inside50_ave
    matches.at[idx,'kicks_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].kicks_ave
    matches.at[idx,'marks_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].marks_ave
    matches.at[idx,'marks_in_50_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].marks_in_50_ave
    matches.at[idx,'one_percenters_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].one_percenters_ave
    matches.at[idx,'rebound50_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].rebound50_ave
    matches.at[idx,'tackles_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].tackles_ave
    matches.at[idx,'uncontested_poss_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].uncontested_poss_ave
    matches.at[idx,'centre_clearances_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].centre_clearances_ave
    matches.at[idx,'disposal_efficiency_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].disposal_efficiency_ave
    matches.at[idx,'effective_disposals_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].effective_disposals_ave
    matches.at[idx,'intercepts_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].intercepts_ave
    matches.at[idx,'metres_gained_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].metres_gained_ave
    matches.at[idx,'stoppage_clearances_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].stoppage_clearances_ave
    matches.at[idx,'score_involvements_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].score_involvements_ave
    matches.at[idx,'tackles_in_50_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].tackles_in_50_ave
    matches.at[idx,'turnovers_h'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['hteam']].turnovers_ave

    matches.at[idx,'AFLfantasy_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].AFLfantasy_ave
    matches.at[idx,'Supercoach_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].Supercoach_ave
    matches.at[idx,'behinds_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].behinds_ave
    matches.at[idx,'bounces_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].bounces_ave
    matches.at[idx,'brownlow_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].brownlow_ave
    matches.at[idx,'clangers_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].clangers_ave
    matches.at[idx,'clearances_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].clearances_ave
    matches.at[idx,'contested_marks_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].contested_marks_ave
    matches.at[idx,'contested_poss_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].contested_poss_ave
    matches.at[idx,'disposals_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].disposals_ave
    matches.at[idx,'frees_against_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].frees_against_ave
    matches.at[idx,'frees_for_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].frees_for_ave
    matches.at[idx,'goal_assists_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].goal_assists_ave
    matches.at[idx,'goals_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].goals_ave
    matches.at[idx,'handballs_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].handballs_ave
    matches.at[idx,'hitouts_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].hitouts_ave
    matches.at[idx,'inside50_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].inside50_ave
    matches.at[idx,'kicks_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].kicks_ave
    matches.at[idx,'marks_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].marks_ave
    matches.at[idx,'marks_in_50_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].marks_in_50_ave
    matches.at[idx,'one_percenters_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].one_percenters_ave
    matches.at[idx,'rebound50_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].rebound50_ave
    matches.at[idx,'tackles_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].tackles_ave
    matches.at[idx,'uncontested_poss_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].uncontested_poss_ave
    matches.at[idx,'centre_clearances_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].centre_clearances_ave
    matches.at[idx,'disposal_efficiency_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].disposal_efficiency_ave
    matches.at[idx,'effective_disposals_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].effective_disposals_ave
    matches.at[idx,'intercepts_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].intercepts_ave
    matches.at[idx,'metres_gained_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].metres_gained_ave
    matches.at[idx,'stoppage_clearances_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].stoppage_clearances_ave
    matches.at[idx,'score_involvements_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].score_involvements_ave
    matches.at[idx,'tackles_in_50_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].tackles_in_50_ave
    matches.at[idx,'turnovers_a'] = history.seasons[row['season']].rounds[row['round']].team_player_data[row['ateam']].turnovers_ave

    # Reset the index, which is now jumbled and meaningless
    matches.reset_index(drop=True,inplace=True)
    return matches