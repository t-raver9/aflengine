import pandas as pd

def days_break(matches: pd.DataFrame) -> pd.DataFrame:
    
    # Prepopulate the columns we're looking to fill
    matches['h_break'] = 0
    matches['h_played'] = matches['h_played']
    season = matches['season'].iloc[0] - 1 # For logging
    
    # HOME TEAM
    for idx,row in matches.iterrows():
        if (season != row['season']):
            print('Collecting home team days break data from season {}'.format(row['season']))
        season = row['season']
        played = row['h_played']
        hteam = row['hteam']
        
        # If the first game of the season, use a 7, which is the average break
        if played == 1:
            matches.at[idx,'h_break'] = 7
            
        # Else, find the last game and subtract the date differences
        else:
            last_game_dt = matches[(matches['season']==season)
                                   &(((matches['hteam']==hteam)&(matches['h_played']==(played-1)))
                                     |((matches['ateam']==hteam)&(matches['a_played']==(played-1))))]['date'].iloc[0]

            matches.at[idx,'h_break'] = (row['date'] - last_game_dt).days
            
    # Prepopulate the columns we're looking to fill
    matches['a_break'] = 0
    matches['a_played'] = matches['a_played']
    season = matches['season'].iloc[0] - 1 # For logging
    
    # AWAY TEAM
    for idx,row in matches.iterrows():
        if (season != row['season']):
            print('Collecting away team days break data from season {}'.format(row['season']))
        season = row['season']
        played = row['a_played']
        ateam = row['ateam']
        
        # If the first game of the season, use a 7, which is the average break
        if played == 1:
            matches.at[idx,'a_break'] = 7
            
        # Else, find the last game and subtract the date differences
        else:
            last_game_dt = matches[(matches['season']==season)
                                   &(((matches['ateam']==ateam)&(matches['a_played']==(played-1)))
                                     |((matches['hteam']==ateam)&(matches['h_played']==(played-1))))]['date'].iloc[0]

            matches.at[idx,'a_break'] = (row['date'] - last_game_dt).days
    
    return matches

def x_game_average_break(matches: pd.DataFrame, num_games: int) -> pd.DataFrame:
    h_field_header = 'h_ave_break_' + str(num_games)
    a_field_header = 'a_ave_break_' + str(num_games)

    # Prepopulate fields
    matches[h_field_header] = 0.0
    matches[a_field_header] = 0.0
    season = matches['season'].iloc[0] - 1 # For logging

    # HOME TEAM
    for idx,row in matches.iterrows():
        if (season != row['season']):
            print('Collecting home team average break data from season {}'.format(row['season'])) # Logging
        num_games_tmp = num_games # Required for later equivalence
        hteam = row['hteam']
        played = row['h_played']
        season = row['season']
        # Case 1: the team has played x number of games in the season already
        if played <= num_games:
            total_break = 0
            num_games_tmp = played
            for games in range(num_games_tmp):
                total_break += matches[(matches['season']==season) & 
                (((matches['hteam'] == hteam) & (matches['h_played'] == (played-games))) |
                (((matches['ateam'] == hteam) & (matches['a_played'] == (played-games)))))]['h_break'].iloc[0]
                
            ave_break = total_break/num_games_tmp
            matches.at[idx,h_field_header] = ave_break

        # Case 2: the team has played less than x number of games in the season already
        else:
            total_break = 0
            num_games_tmp = played
            for games in range(num_games_tmp):
                total_break += matches[(matches['season']==season) & 
                (((matches['hteam'] == hteam) & (matches['h_played'] == (played-games))) |
                (((matches['ateam'] == hteam) & (matches['a_played'] == (played-games)))))]['h_break'].iloc[0]
            ave_break = total_break/num_games_tmp
            matches.at[idx,h_field_header] = ave_break

    season = matches['season'].iloc[0] - 1 # For logging

    # AWAY TEAM
    for idx,row in matches.iterrows():
        if (season != row['season']):
            print('Collecting away team average break data from season {}'.format(row['season'])) # Logging
        num_games_tmp = num_games
        ateam = row['ateam']
        played = row['a_played']
        season = row['season']
        # Case 1: the team has played x number of games in the season already
        if played <= num_games:
            total_break = 0
            num_games_tmp = played
            for games in range(num_games_tmp):
                total_break += matches[(matches['season']==season) & 
                (((matches['hteam'] == ateam) & (matches['h_played'] == (played-games))) |
                (((matches['ateam'] == ateam) & (matches['a_played'] == (played-games)))))]['a_break'].iloc[0]
                
            ave_break = total_break/num_games_tmp
            matches.at[idx,a_field_header] = ave_break

        # Case 2: the team has played less than x number of games in the season already
        else:
            total_break = 0
            num_games_tmp = played
            for games in range(num_games_tmp):
                total_break += matches[(matches['season']==season) & 
                (((matches['hteam'] == ateam) & (matches['h_played'] == (played-games))) |
                (((matches['ateam'] == ateam) & (matches['a_played'] == (played-games)))))]['a_break'].iloc[0]
            ave_break = total_break/num_games_tmp
            matches.at[idx,a_field_header] = ave_break

    return matches