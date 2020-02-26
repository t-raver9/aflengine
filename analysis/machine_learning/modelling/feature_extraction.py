import pandas as pd
from typing import List
from metadata import get_season_rounds, get_season_teams
from columns import home_cols, away_cols, home_cols_this_game, away_cols_this_game, home_cols_prev_games, away_cols_prev_games

def per_game_stats(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Function to take existing game statistics and return additional columns
    with their per-game equivalents
    """
    matches['h_points_for_pg'] = matches['h_points_for']/matches['h_played']
    matches['a_points_for_pg'] = matches['a_points_for']/matches['a_played']
    matches['h_points_against_pg'] = matches['h_points_for']/matches['h_played']
    matches['a_points_against_pg'] = matches['a_points_for']/matches['a_played']
    matches['h_wins_pg'] = matches['h_wins']/matches['h_played']
    matches['a_wins_pg'] = matches['a_wins']/matches['a_played']
    matches['h_losses_pg'] = matches['h_losses']/matches['h_played']
    matches['a_losses_pg'] = matches['a_losses']/matches['a_played']
    matches['h_draws_pg'] = matches['h_draws']/matches['h_played']
    matches['a_draws_pg'] = matches['a_draws']/matches['a_played']
    
    return matches

def determine_winner(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Adding a 'winner' column to the dataframe. A value of 1 means the home
    team won, 0 means the away team won, and 0.5 indicates a draw.
    """
    matches['winner'] = 0
    for idx,row in matches.iterrows():
        if row['hscore'] > row['ascore']:
            matches.at[idx,'winner'] = 1
        elif row['hscore'] < row['ascore']:
            matches.at[idx,'winner'] = 0
        else:
            matches.at[idx,'winner'] = 0.5
    return matches

def initialise_df() -> pd.DataFrame:
    """
    Initialise the dataframe of features we'll be filling out. This will hold
    only the features we've determined to be relevant for modelling.
    """
    df = pd.DataFrame(columns = 
                      home_cols_this_game + 
                      home_cols_prev_games + 
                      away_cols_this_game + 
                      away_cols_prev_games)
    return df

def home_away_features(matches: pd.DataFrame) -> pd.DataFrame:
    """
    Populate the new dataframe with the relevant features from the matches 
    dataframe. The reason we need to do this is because the current dataframe
    has a mix of data from before the game, and data from after the game. For
    example: the ladder positions and per-game averages are after the game in 
    the row has been completed, but the odds, days break and home-ground
    advantage are informative before the game starts.

    Thus, for ladder positions and per-game averages, we need to find the last
    time the team played and use this data to predict the outcome of the current
    game.
    """
    # Get required data about rounds and teams per season
    season_rounds = get_season_rounds(matches)
    season_teams = get_season_teams(matches)

    # Initialise the dataframe we'll be filling out
    home_away_df = initialise_df()
    
    # Firstly, add the "current game" features.
    for idx,row in matches.iterrows():
        for col in (home_cols_this_game + away_cols_this_game):
            home_away_df.at[idx,col] = row[col]
        print('Adding current game for row {}'.format(idx))
            
    # Then, add the "previous game" features
    for idx,row in matches.iterrows():
        print('Adding previous games for row {}'.format(idx))
        
        # If game played > 1, no need to go back a season
        # Home team
        if row['h_played'] > 1:
            hteam_prev = matches[((matches['h_played'] == (row['h_played'] - 1)) & (matches['hteam'] == row['hteam']) & (matches['season'] == row['season'])) | 
                                ((matches['a_played'] == (row['h_played'] - 1)) & (matches['ateam'] == row['hteam'])& (matches['season'] == row['season']))].iloc[0]
            for col in (home_cols_prev_games):
                home_away_df.at[idx,col] = hteam_prev[col]
                
        # Away team
        if row['a_played'] > 1:
            ateam_prev = matches[((matches['h_played'] == (row['a_played'] - 1)) & (matches['hteam'] == row['ateam']) & (matches['season'] == row['season'])) | 
                                ((matches['a_played'] == (row['a_played'] - 1)) & (matches['ateam'] == row['ateam']) & (matches['season'] == row['season']))].iloc[0]
            for col in (away_cols_prev_games):
                home_away_df.at[idx,col] = ateam_prev[col]
                
        # If game played == 1 and team played in the previous season, get the data from the final round
        # of the previous season. Otherwise, set it to zero

        # Home team
            
        if (row['h_played']==1):
            
            if (row['season']==min(season_rounds.keys())):
                home_away_df.at[idx,col] = 0
                
            elif (row['hteam'] not in season_teams[row['season']-1]):
                for col in (home_cols_prev_games):
                    home_away_df.at[idx,col] = 0
                    
            elif (row['hteam'] in season_teams[row['season']-1]):
                played_prev_year = max(max(matches[(matches['hteam']==row['hteam']) & (matches['season']==row['season']-1)]['h_played']),max(matches[(matches['ateam']==row['hteam']) & (matches['season']==row['season']-1)]['a_played']))
                print('played in the previous year:',played_prev_year)
                hteam_prev = matches[(matches['season']==(row['season']-1)) &
                                     (matches['h_played']==played_prev_year)].iloc[0]
                for col in (home_cols_prev_games):
                    home_away_df.at[idx,col] = hteam_prev[col]

        # Away team
                    
        if (row['a_played']==1):
            
            if (row['season']==min(season_rounds.keys())):
                home_away_df.at[idx,col] = 0
                
            elif (row['ateam'] not in season_teams[row['season']-1]):
                for col in (away_cols_prev_games):
                    home_away_df.at[idx,col] = 0
                    
            elif (row['ateam'] in season_teams[row['season']-1]):
                played_prev_year = max(max(matches[(matches['hteam']==row['ateam']) & (matches['season']==row['season']-1)]['h_played']),max(matches[(matches['ateam']==row['ateam']) & (matches['season']==row['season']-1)]['a_played']))
                ateam_prev = matches[(matches['season']==(row['season']-1)) &
                                     (matches['a_played']==played_prev_year)].iloc[0]
                for col in (away_cols_prev_games):
                    home_away_df.at[idx,col] = ateam_prev[col]
                
    return home_away_df

def create_diff_cols() -> List:
    """
    Create the list of columns we'll be using in our features dataframe
    """
    home_away_pairs = list(zip(home_cols,away_cols))
    diff_cols = []
    for pair in home_away_pairs:
        if pair[0][:4] == 'home':
            colname = pair[0][4:] + '_diff'
        elif pair[0][:2] == 'h_':
            colname = pair[0][2:] + '_diff'
        elif pair[0][-6:] == '_h_ave':
            colname = pair[0][:-6] + '_ave_diff'
        else:
            pass

        diff_cols.append(colname)

    return diff_cols

def create_diff_features(diff_cols: List, home_away_df: pd.DataFrame) -> pd.DataFrame:

    diff_df = pd.DataFrame(columns = diff_cols)

    home_away_pairs = list(zip(home_cols,away_cols))
    for idx,pair in enumerate(home_away_pairs):
        diff_df[diff_cols[idx]] = home_away_df[pair[0]] - home_away_df[pair[1]]

    diff_df.fillna(0,inplace=True)

    return diff_df