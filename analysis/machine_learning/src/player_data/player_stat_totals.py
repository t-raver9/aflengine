import pandas as pd
from datetime import datetime
from typing import List, Dict
from os.path import dirname,abspath
from .columns import (
    player_cols,
    player_cols_to_agg,
    player_cols_to_pg
)
from progress.bar import ShadyBar
from collections import defaultdict

def get_rounds_per_year(matches: pd.DataFrame):
    """
    Note that this function returns the number of games played, not the number
    of rounds
    """
    get_rounds_per_year = matches[['season','round']].groupby('season').max()
    return get_rounds_per_year

def final_to_num(season, round_num, rounds_per_year):
    """
    Adds a round field to allow games to be sorted. Required for future logic.
    """
    finals_list = ['EF','QF','QR','SF','SR','PF','PR','GF','GR']
    if round_num.isdigit() == False:
        return rounds_per_year.loc[int(season)].item() + finals_list.index(round_num) + 1
    else:
        return int(round_num)

def get_col_per_game(col_value: float, games: int) -> float:
    per_game = col_value / games
    return per_game

def add_player_totals(matches: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    # Get rounds per year so we know how to handle finals rounds
    rounds_per_year = get_rounds_per_year(matches)

    # Add numeric round numbers to handle the finals rounds
    players['round_num'] = None
    players['round_num'] = players.apply(lambda x: final_to_num(
        x['season'], x['round'], rounds_per_year),axis=1)

    # Drop the columns we don't need from players_col_to_agg
    player_cols_to_agg.remove('matchid')
    player_cols_to_agg.remove('team')

    # Organise the df, then go down, implementing both the logic for the overall stats and the season stats
    players.sort_values(by=['playerid','season','round_num'], inplace=True)

    # Initialise the columns that we want to use
    for col in player_cols_to_agg:
        players['season_' + col] = None
        players['career_' + col] = None

    # Track the games played
    players['career_games_played'] = None
    players['season_games_played'] = None

    # Initialise
    curr_player = players.iloc[0]['playerid']
    curr_season = players.iloc[0]['season']
    career_games_played = 0
    season_games_played = 0
    season_metrics = defaultdict(lambda: 0)
    career_metrics = defaultdict(lambda: 0)

    # Start loop
    with ShadyBar('Processing', max=len(players)) as bar:
        for idx, row in players.iterrows():

            bar.next() # Logging

            if row['playerid'] != curr_player: # Start again for a new player
                season_metrics = defaultdict(lambda: 0)
                career_metrics = defaultdict(lambda: 0)
                for col in player_cols_to_agg:
                    season_metrics[col] += row[col]
                    career_metrics[col] += row[col]
                    players.at[idx, 'season_' + col] = season_metrics[col]
                    players.at[idx, 'career_' + col] = career_metrics[col]
                curr_player = row['playerid']
                curr_season = row['season']
                career_games_played = 1
                season_games_played = 1
                players.at[idx, 'career_games_played'] = career_games_played
                players.at[idx, 'season_games_played'] = season_games_played
                continue
                
            elif row['season'] == curr_season: # Same season, continue counting for this
                for col in player_cols_to_agg:
                    season_metrics[col] += row[col]
                    career_metrics[col] += row[col]
                    players.at[idx, 'season_' + col] = season_metrics[col]
                    players.at[idx, 'career_' + col] = career_metrics[col]
                career_games_played += 1
                season_games_played += 1
                players.at[idx, 'career_games_played'] = career_games_played
                players.at[idx, 'season_games_played'] = season_games_played
                continue
                
            elif row['season'] != curr_season: # Different season, restart the season metrics
                season_metrics = defaultdict(lambda: 0)
                for col in player_cols_to_agg:
                    season_metrics[col] += row[col]
                    career_metrics[col] += row[col]
                    players.at[idx, 'season_' + col] = season_metrics[col]
                    players.at[idx, 'career_' + col] = career_metrics[col]
                curr_season = row['season']
                career_games_played += 1
                season_games_played = 1
                players.at[idx, 'career_games_played'] = career_games_played
                players.at[idx, 'season_games_played'] = season_games_played
                continue
                
            else:
                raise Exception('Unknown case')

        # Change columns to per-game, instead of raw amount
        for col in players.columns:
            if (col[0:7] == 'career_') & (col != 'career_games_played'):
                players[col] = get_col_per_game(players[col], players['career_games_played'])
            elif (col[0:7] == 'season_') & (col != 'season_games_played'): 
                players[col] = get_col_per_game(players[col], players['season_games_played'])
            else:
                pass
                
        # Save data to file
        players.to_csv('src/player_data/data/players_with_player_stat_totals.csv')

        return players