import pandas as pd
from datetime import datetime
from typing import List, Dict
from os.path import dirname,abspath
from .columns import (
    player_cols,
    player_cols_to_agg,
    player_cols_to_pg
)
from copy import deepcopy
from progress.bar import ShadyBar

class Player:
    def __init__(self):
        for column in player_cols:
            setattr(self, column, None)

def get_round(matchid: str) -> str:
    rnd = matchid[4:6]
    return rnd

def read_data() -> pd.DataFrame:
    """
    Read in players.csv
    Returns a pandas dataframe
    """
    d = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
    players = pd.read_csv(d + "/bench/players.csv")
    # Use below for testing
    # players = pd.read_csv('src/player_data/data/players_with_player_stat_totals.csv')
    players['round'] = players.apply(lambda row: get_round(row['matchid']), axis = 1)
    return players

def define_aggregate_columns(player_cols_to_agg: List) -> List:
    """
    Defines which columns we'd like to aggregate to the team level
    """
    # Check that our grouping columns are in the player column list
    cols_to_check = ['matchid','next_matchid','team']
    for col in cols_to_check:
        if col not in player_cols_to_agg:
            player_cols_to_agg.append(col)
    # Define aggregate columns
    player_cols_to_agg_temp = list(filter(
        lambda x: x not in ['matchid','next_matchid','team'],player_cols_to_agg))
    player_cols_to_agg.extend(
        ['career_' + col for col in player_cols_to_agg_temp])
    player_cols_to_agg.extend(
        ['season_' + col for col in player_cols_to_agg_temp])
    player_cols_to_agg.extend(['career_games_played','season_games_played'])
    return player_cols_to_agg

def get_next_matchid(players: pd.DataFrame) -> pd.DataFrame:
    """
    For each row of the players df, find out what the next game is for each
    player. If there's no other games, set the next_matchid to None
    """
    players.sort_values(by=['playerid','season','round_num'], ascending = False, inplace = True)
    players['next_matchid'] = None # Initalise the column
    curr_player = None

    with ShadyBar('Getting next_matchid for each player', max=len(players)) as bar:
        for idx, row in players.iterrows():
            bar.next()
            if row['playerid'] == curr_player:
                players.at[idx, 'next_matchid'] = next_matchid
            else:
                players.at[idx, 'next_matchid'] = None
            next_matchid = row['matchid']
            curr_player = row['playerid']

    # Reset order for further processing
    players.sort_values(by=['playerid','season','round_num'], ascending = True, inplace = True) 
    players.to_csv('src/player_data/data/players_with_player_stat_totals.csv')
    return players

def get_diff_cols(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Function to take the columns and separate between home and away teams. Each
    metric will have a "diff" column which tells the difference between home
    and away for this metric. i.e. there's a diff_percentage column which tells
    the difference between home and away for the percentage
    """
    print('Creating differential columns')
    for col in matches.columns:
        if col[0:2] == 'h_':
            try:
                h_col = col
                a_col = 'a_' + col[2:]
                diff_col = 'diff_' + col[2:]
                matches[diff_col] = matches[h_col] - matches[a_col]
            except TypeError:
                pass
    return matches

def aggregate_player_data(players: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates the stats for individual players for each team to the match
    level, and adds this to the matches dataframe
    """
    # Get the next_matchid for each player
    players = get_next_matchid(players)
    # Get the list of columns you require
    player_cols = define_aggregate_columns(player_cols_to_agg)
    for col in player_cols:
        print(col)
    # Group by matchid and team, and get the sum of the player data
    aggregate = players[player_cols].groupby(['next_matchid','team']).agg('mean')
    # Join these stats onto the matches dataframe
    aggs_h = deepcopy(aggregate)
    aggs_a = deepcopy(aggregate)
    aggs_h.columns = aggregate.columns.map(lambda x: 'h_' + str(x))
    aggs_a.columns = aggregate.columns.map(lambda x: 'a_' + str(x))
    matches = matches.merge(aggs_h,how='left',left_on=['hteam','matchid'],right_on=['team','next_matchid'])
    matches = matches.merge(aggs_a,how='left',left_on=['ateam','matchid'],right_on=['team','next_matchid'])
    # Get the differential columns
    matches = get_diff_cols(matches)
    # Save data to file
    matches.to_csv('src/player_data/data/matches_with_player_agg.csv')
    return matches