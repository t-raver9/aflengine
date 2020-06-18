import pandas as pd
from datetime import datetime
from typing import List, Dict
from os.path import dirname,abspath

def read_data() -> pd.DataFrame:
    """
    Read in matches.csv
    Returns a pandas dataframe
    """
    d = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))
    matches = pd.read_csv(d + "/bench/matches.csv")
    return matches

def change_date_type(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Change date data to be type datetime
    """
    try:
        matches['date'] = pd.to_datetime(matches['date'],format="%d-%b-%Y")
    except ValueError:
        # Usually occurs because the years after 1899 got cut to two decimal
        # places, so fix this by re-adding the year in
        for idx, row in matches.iterrows():
            if len(row['date'].split('-')[-1]) == 2:
                # Has been abbreviated. Fix the year with the matchid
                full_year = row['matchid'][0:4]
                matches.at[idx,'date'] = row['date'][:-2] + full_year
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

def change_round_type(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Change round type from string to int
    """
    matches['round'] = matches['round'].astype(int)
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
    return matches

def get_winner(hscore: int, ascore: int):
    """
    Takes in a home score and an away score, and determines the winner
    """
    if hscore > ascore:
        winner = 'home'
    elif hscore < ascore:
        winner = 'away'
    else:
        winner = 'draw'
    return winner

def prepare_dataframe() -> pd.DataFrame:
    """
    Applies all of the above functions and returns the prepared dataframe
    """
    # Read in data
    matches = read_data()
    # Remove finals games from the dataset
    matches = remove_finals(matches)
    # Change data type for round, time and date
    matches = change_time_type(matches)
    matches = change_date_type(matches)
    matches = change_round_type(matches)
    # Parse quarterly score strings (e.g. 1.2.8) into goals, behinds and scores
    matches = parse_quarters_dataframe(matches)
    # Sort df by rounds and seasons
    matches.sort_values(by=['season', 'round'], ascending=True, inplace=True)
    # Determine winner
    matches['winner'] = matches.apply(
        lambda row: get_winner(row['hscore'],row['ascore']),axis=1
        )
    return matches