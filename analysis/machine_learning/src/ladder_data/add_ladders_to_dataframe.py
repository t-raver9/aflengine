import pandas as pd
from typing import Type
from .generate_ladders import (
    TeamLadder,
    Ladder
)
from ..match_data import prepare_dataframe
from ..match_data.generate_match_objects import History
from ..match_data.resources.columns import generic_team_columns
from ..ladder_data.resources.columns import ladder_columns

def add_ladders(history: Type[History], matches: Type[pd.DataFrame]):
    # Add a tuple of ladder objects to each row, format (h_ladder,a_ladder)
    matches['ladders'] = matches.apply(
        lambda row: get_team_ladder_object(history,row), axis=1
    )
    # Split this list into it's own respective columns
    matches['h_ladder_obj'] = matches['ladders'].apply(lambda x: x[0])
    matches['a_ladder_obj'] = matches['ladders'].apply(lambda x: x[1])
    # Drop the original column with two ladders
    matches.drop('ladders', axis=1, inplace=True)
    return matches

def get_team_ladder_object(history: Type[History], data: pd.DataFrame):
    if data['round'] == 1:
        h_ladder = TeamLadder(data['hteam'])
        a_ladder = TeamLadder(data['ateam'])
    else:
        h_ladder = history.seasons[data['season']].rounds[
            data['round']-1].ladder.team_ladders[data['hteam']]
        a_ladder = history.seasons[data['season']].rounds[
            data['round']-1].ladder.team_ladders[data['ateam']]
    return [h_ladder, a_ladder]

def extract_ladder_data(matches: pd.DataFrame, save_to_file: bool = False):
    ladder_cols = [i for i,j in ladder_columns]
    # Loop through each row of the dataframe
    for idx,row in matches.iterrows():
        # Create home and away team columns
        for col in ladder_cols:
            h_col = 'h_' + col
            a_col = 'a_' + col
            matches.at[idx,h_col] = row['h_ladder_obj'].__dict__[col]
            matches.at[idx,a_col] = row['a_ladder_obj'].__dict__[col]
    # If appropriate, save the dataframe to a file
    if save_to_file:
        matches.to_csv('src/ladder_data/data/matches_with_ladders.csv')
    return matches