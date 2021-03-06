import pandas as pd
import pickle
from typing import Dict
from os.path import (
    dirname,
    abspath
)
from ..ladder_data.resources.columns import (
    ladder_cols,
    h_ladder_form_cols,
    a_ladder_form_cols,
    h_ladder_form_cols_mapping,
    a_ladder_form_cols_mapping
)
from ..ladder_data.generate_ladders import (
    Ladder,
    TeamLadder
)
from ..match_data.generate_match_objects import (
    History,
    Season,
    Round
)

src_d = dirname(dirname(__file__))
ladder_obj_path = src_d + '/ladder_data/data/history_object.pk1'

def get_games_played_per_year(matches: pd.DataFrame):
    """
    Note that this function returns the number of games played, not the number
    of rounds
    """
    games_played_per_year = matches[['season','h_played']].groupby('season').max()
    return games_played_per_year

def get_season_num_games(matches: pd.DataFrame) -> Dict:
    """
    Return a dictionary with seasons as keys and number of games
    in season as values. Does the same thing as above but in a dictionary.
    """
    seasons = matches['season'].unique()
    rounds_in_season = dict.fromkeys(seasons,0)
    
    for season in seasons:
        rounds_in_season[season] = max(matches[matches['season']==season]['h_played']) + 1
    return rounds_in_season

def get_rounds_per_year(matches: pd.DataFrame):
    """
    Returns the number of rounds played in each season
    """
    rounds_per_year = matches[['season','round']].groupby('season').max()
    return rounds_per_year

def get_teams_per_year(matches: pd.DataFrame):
    """
    Returns a dictionary of seasons with the teams that played in each season
    """
    teams_per_year = {}
    for _,row in matches.iterrows():
        if row['season'] not in teams_per_year:
            teams_per_year[row['season']] = []
        if row['hteam'] not in teams_per_year[row['season']]:
            teams_per_year[row['season']].append(row['hteam'])
    return teams_per_year

def fill_columns(curr_ladder, ladder_x_games_ago, matches, idx, h_a):
    if h_a == 'home':
        for col in ladder_cols:
            col_diff = curr_ladder.__dict__[col] \
            - ladder_x_games_ago.__dict__[col]
            matches.at[idx,h_ladder_form_cols_mapping[col]] = col_diff
    else:
        for col in ladder_cols:
            col_diff = curr_ladder.__dict__[col] \
            - ladder_x_games_ago.__dict__[col]
            matches.at[idx,a_ladder_form_cols_mapping[col]] = col_diff
    return matches

def form_across_seasons(matches: pd.DataFrame, num_games_back):
    """
    This function considers form across seasons. For example, if a team won 15
    games last season and is playing their first game this season, they will
    have a winning form of -15 for this game. This function looks back at the
    previous year and fixes this to reflect how the team went last year.
    """
    pickle_in = open(ladder_obj_path,'rb')
    ladders = pickle.load(pickle_in)

    season_num_games = get_season_num_games(matches)

    for idx, row in matches.iterrows():
        if row['h_played'] <= num_games_back:
            try:
                # Get the ladder for the home and away team from the last game last year
                h_last_year_ladder = ladders.__dict__['seasons'][row['season']-1].__dict__[
                    'rounds'][season_num_games[row['season']-1]].__dict__['ladder'].__dict__[
                    'team_ladders'][row['hteam']].__dict__
                a_last_year_ladder = ladders.__dict__['seasons'][row['season']-1].__dict__[
                    'rounds'][season_num_games[row['season']-1]].__dict__['ladder'].__dict__[
                    'team_ladders'][row['ateam']].__dict__
                
                # Use this to fix up the relevant form metrics
                for k,v in h_last_year_ladder.items():
                    print(k)
                    col = 'h_' + k + '_form'
                    if col in matches.columns:
                        print(col)
                        current = matches.at[idx,col]
                        matches.at[idx,col] = current + v
                for k,v in a_last_year_ladder.items():
                    col = 'a_' + k + '_form'
                    if col in matches.columns:
                        current = matches.at[idx,col]
                        matches.at[idx,col] = current + v

                # Compute percentage again
                try:
                    matches.at[idx,'h_percentage_form'] = (matches.at[idx,'h_points_for_form']/matches.at[idx,'h_points_against_form']) * 100
                except ZeroDivisionError:
                    matches.at[idx,'h_percentage_form'] = 100
                try:
                    matches.at[idx,'a_percentage_form'] = (matches.at[idx,'a_points_for_form']/matches.at[idx,'a_points_against_form']) * 100
                except ZeroDivisionError:
                    matches.at[idx,'a_percentage_form'] = 100

            except KeyError:
                pass 

    return matches


def get_ladder_form(history, matches, num_games_back):
    """
    This function adds form columns to the dataframe. We feed in a dataframe
    with ladder data for each team, then use this to compute the form of that
    team over the past x games.
    """
    # Get the max games played per year, for later use
    max_played_per_season = get_games_played_per_year(matches)
    rounds_per_year = get_rounds_per_year(matches)
    teams_per_year = get_teams_per_year(matches)
    first_season = min(teams_per_year.keys())
    # Firstly, initialise the dataframe with the new columns
    for col in h_ladder_form_cols + a_ladder_form_cols:
        matches[col] = None
    # Begin iteration
    for idx,row in matches.iterrows():
        print(row['season'],row['round'])
        #print(row['season'],row['round'])
        # Get the ladder object for the home and away teams
        h_ladder = row['h_ladder_obj']
        a_ladder = row['a_ladder_obj']

        # Home team SCN1: don't need to go to the previous season
        if (row['h_played'] > num_games_back):
            # Find the corresponding ladder from the history object
            required_round_num = row['round'] - num_games_back
            while True:
                ladder_x_games_ago = history.seasons[row['season']] \
                .rounds[required_round_num] \
                .ladder.team_ladders[row['hteam']]
                if ladder_x_games_ago.played == row['h_played'] - num_games_back:
                    break
                else:
                    required_round_num -= 1
                    continue
            # Fill out the columns
            matches = fill_columns(h_ladder, ladder_x_games_ago, matches, idx, 'home')

        # Home team SCN3: we're in the first ever season of the league, and we
        # can't go back a season to get the full amount of games
        elif (row['h_played'] <= num_games_back) & (row['season'] == first_season):
            # Create a default ladder object, since it's round 1
            ladder_x_games_ago = TeamLadder(row['hteam'])
            # Fill out the columns
            matches = fill_columns(h_ladder, ladder_x_games_ago, matches, idx, 'home')
        
        # Home team SCN4: need to go back a season, and the team played in the
        # previous season
        elif (row['h_played'] <= num_games_back) & (row['hteam'] in teams_per_year[row['season'] - 1]):
            # Find how many games the team played in the previous year
            played_prev_year = max_played_per_season.loc[row['season'] - 1].values[0]
            rounds_prev_year = rounds_per_year.loc[row['season'] - 1].values[0]
            # Find the required round from the previous year
            required_round_num = rounds_prev_year + row['h_played'] - num_games_back
            # Exception for St Kilda
            if (row['hteam'] == 'St Kilda') & (row['season'] == 1944):
                played_prev_year = 10
            while True:
                ladder_x_games_ago = history.seasons[row['season'] - 1] \
                .rounds[required_round_num] \
                .ladder.team_ladders[row['hteam']]
                if ladder_x_games_ago.played == played_prev_year \
                    + row['h_played'] - num_games_back:
                    break
                else:
                    required_round_num -= 1
                    continue
            # Fill out the columns
            matches = fill_columns(h_ladder, ladder_x_games_ago, matches, idx, 'home')

        # Home team SCN5: need to go back a season, but the team didn't play
        # in the previous season
        elif (row['h_played'] <= num_games_back) & (row['hteam'] not in teams_per_year[row['season'] - 1]):
            # The required round number will be the first round
            required_round_num = 1
            ladder_x_games_ago = history.seasons[row['season']] \
            .rounds[required_round_num] \
            .ladder.team_ladders[row['hteam']]
            # Fill out the columns
            matches = fill_columns(h_ladder, ladder_x_games_ago, matches, idx, 'home')

        # Away team SCN1: don't need to go to the previous season
        if (row['a_played'] > num_games_back):
            # Find the corresponding ladder from the history object
            required_round_num = row['round'] - num_games_back
            while True:
                ladder_x_games_ago = history.seasons[row['season']] \
                .rounds[required_round_num] \
                .ladder.team_ladders[row['ateam']]
                if ladder_x_games_ago.played == row['a_played'] - num_games_back:
                    break
                else:
                    required_round_num -= 1
                    continue
            # Fill out the columns
            matches = fill_columns(a_ladder, ladder_x_games_ago, matches, idx, 'away')

        # Home team SCN2: we're in the first ever season of the league, and we
        # can't go back a season to get the full amount of games
        elif (row['a_played'] <= num_games_back) & (row['season'] == first_season):
            # Create a default ladder object, since it's round 1
            ladder_x_games_ago = TeamLadder(row['hteam'])
            # Fill out the columns
            matches = fill_columns(a_ladder, ladder_x_games_ago, matches, idx, 'away')
        
        # Home team SCN3: need to go back a season, and the team played in the
        # previous season
        elif (row['a_played'] <= num_games_back) & (row['ateam'] in teams_per_year[row['season'] - 1]):
            # Find how many games the team played in the previous year
            played_prev_year = max_played_per_season.loc[row['season'] - 1].values[0]
            rounds_prev_year = rounds_per_year.loc[row['season'] - 1].values[0]
            # Find the required round from the previous year
            required_round_num = rounds_prev_year + row['a_played'] - num_games_back
            # Exception for St Kilda
            if (row['ateam'] == 'St Kilda') & (row['season'] == 1944):
                played_prev_year = 10
            while True:
                ladder_x_games_ago = history.seasons[row['season'] - 1] \
                .rounds[required_round_num] \
                .ladder.team_ladders[row['ateam']]
                if ladder_x_games_ago.played == played_prev_year \
                    + row['a_played'] - num_games_back:
                    break
                else:
                    required_round_num -= 1
                    continue
            # Fill out the columns
            matches = fill_columns(a_ladder, ladder_x_games_ago, matches, idx, 'away')

        # Home team SCN4: need to go back a season, but the team didn't play
        # in the previous season
        elif (row['a_played'] <= num_games_back) & (row['ateam'] not in teams_per_year[row['season'] - 1]):
            # The required round number will be the first round
            required_round_num = 1
            ladder_x_games_ago = history.seasons[row['season']] \
            .rounds[required_round_num] \
            .ladder.team_ladders[row['ateam']]
            # Fill out the columns
            matches = fill_columns(a_ladder, ladder_x_games_ago, matches, idx, 'away')

    # We want to change the percentage form to be the net percentage over the
    # past five games, not the difference. If we use the difference, a team
    # that dominates all season will not be recognised above a team who
    # is dominated all season.
    matches['h_percentage_form'] = matches.apply(
        lambda row: (row['h_points_for_form'] * 100)/ row['h_points_against_form'] \
            if row['h_points_against_form'] != 0 else 100, axis = 1)
    matches['a_percentage_form'] = matches.apply(
        lambda row: (row['a_points_for_form'] * 100)/ row['a_points_against_form'] \
            if row['a_points_against_form'] != 0 else 100, axis = 1)

    # Use form across seasons logic
    matches = form_across_seasons(matches, num_games_back=num_games_back)

    # Write the dataframe out to file
    matches.to_csv('src/ladder_form/data/matches_with_form.csv')

    return matches