import pandas as pd
from datetime import datetime
from typing import List, Dict

default_data_path = 'https://github.com/chrisstrods/aflengine/raw/master/bench/matches.csv'

def read_data(match_data_path: str) -> pd.DataFrame:
    matches = pd.read_csv(match_data_path)
    return matches

def change_date_type(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Change date data to be type datetime
    """
    matches['date'] = pd.to_datetime(matches['date'],format="%d-%b-%Y")
    return matches

def change_time_type(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Change time data to be type time. This there's a couple of games in the early days of
    footy which started in the AM, so this conversion isn't 100% accurate
    """
    matches['time'] = matches['time'] + ' PM'
    matches['time'] = pd.to_datetime(matches['time'],format="%I:%M %p").dt.time
    return matches

def parse_quarters_dataframe(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Splits the goals, behinds and score format of the incoming quarterly scores into their
    own columns.
    """
    columns_to_parse = ['hteam_q1','hteam_q2', 'hteam_q3', 'hteam_q4','ateam_q1', 'ateam_q2','ateam_q3', 'ateam_q4']
    column_suffixes = ['_goals','_behinds','_score']
    for column in columns_to_parse:
        column_headers = [(column + suffix) for suffix in column_suffixes]
        matches[column_headers[0]] = matches[column].apply(get_goals)
        matches[column_headers[1]] = matches[column].apply(get_behinds)
        matches[column_headers[2]] = matches[column].apply(get_score)
    return matches

def get_goals(quarter_score: str) -> List:
    """
    Extract goals from score string
    """
    return quarter_score.split('.')[0]

def get_behinds(quarter_score: str) -> List:
    """
    Extract behinds from score string
    """
    return quarter_score.split('.')[1]

def get_score(quarter_score: str) -> List:
    """
    Extract score from score string
    """
    return quarter_score.split('.')[2]

def remove_finals(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Remove finals games from matches dataset. Keep only home-and-away games. Also, change
    rounds to type int.
    """
    matches = matches[matches['round'].apply(lambda x: x.isdigit())]
    matches['round'] = matches['round'].astype(int)
    return matches

def prepare_data(match_data_path: str = default_data_path) -> pd.DataFrame:
    """
    Apply transformations to dataset, and return
    """
    # Read in data
    matches = read_data(match_data_path)

    # Change data type for time and data
    matches = change_time_type(matches)
    matches = change_date_type(matches)

    # Parse quarterly score strings (e.g. 1.2.8) into goals, behinds and scores
    matches = parse_quarters_dataframe(matches)

    # Remove finals games from the dataset, and change the rounds to type int
    matches = remove_finals(matches)

    # Sort df by rounds and seasons
    matches.sort_values(by=['season','round'],ascending=True,inplace=True)

    return matches