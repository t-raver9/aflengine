import pandas as pd
from ladder_classes import Team_ladder_info, Season, Round_obj, History
from metadata import get_season_rounds,get_season_teams

def last_x_games_stats_hteam(matches: pd.DataFrame, history: History, num_games: int) -> pd.DataFrame:
    """
    Function to create form data for teams by collecting stats on their previous five games.
    The function splits into two branches - one branch handles instances where the team has already
    played the desired number of games in a season. The other branch handles the other case - when
    we need to cycle back a season to complete the form line.
    
    Also need to ensure any stats we wish to populate in the dataset have columns pre-allocated for
    it already. 
    """
    # Get necessary metadata
    teams_in_season = get_season_teams(matches)
    rounds_in_season = get_season_rounds(matches)

    # Pre-populate the columns we're creating
    matches['h_last_5_wins'] = 0
    matches['h_last_5_pct'] = 0
    matches['h_last_5_pts_for'] = 0
    matches['h_last_5_pts_against'] = 0

    # Flip the match dataframe so we can work from latest to oldest
    matches_flipped = matches[::-1]
    for idx,row in matches_flipped.iterrows():
        # Logging
        print(row['season'],row['round'])
        games_back = num_games # Reset for every row
        wins_last_x = 0
        points_for_last_x = 0
        points_against_last_x = 0
        percentage_last_x = 0
        
        # Check how many games the team has played that season
        h_games_played = row['h_played']
        
        # If played equal to or more than the amount of games we want to go back, we don't need to cross a season
        if h_games_played >= games_back:
            # Then we check games until we've checked the games_back amount. Can't just use range, as there may
            # be byes
            i = 0
            while i <= (games_back-1):
                # Not bye
                if (row['round']-i) not in history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['hteam']].bye_rounds:
                    wins_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['hteam']].won_game
                    points_for_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['hteam']].points_for_game
                    points_against_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['hteam']].points_against_game
                    try:
                        percentage_last_x = 100*(points_for_last_x/points_against_last_x)
                    except ZeroDivisionError:
                        percentage_last_x = 100
                    
                # For byes, add an extra game to cycle through
                else:
                    games_back += 1
                i += 1
                
        # If played less than the amount we want to go back, and the team participated in the previous season, then
        # we need to cross a season
        # First, check that we haven't run out of seasons
        if ((h_games_played < games_back) and (row['season'] != min(matches['season']))):
            
            # Then, check that the team in question played in the previous season
            if ((h_games_played < games_back) and (row['hteam'] in teams_in_season[row['season']-1])):
                # Implement the same loop as the happy case, but with an extra condition for checking if we need to
                # iterate the season
                i = 0
                season = row['season']
                round_num = row['round']

                while i <= (games_back-1):
                    # Check for season condition, and dial back by one if necessary
                    if (round_num - i == 0):
                        round_num = rounds_in_season[season-1]
                        season = season-1
                    # Now the loop should work the same as before
                    # Not bye
                    if (round_num-i) not in history.seasons[season].rounds[round_num-i].teams_ladder_info[row['hteam']].bye_rounds:
                        wins_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['hteam']].won_game
                        points_for_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['hteam']].points_for_game
                        points_against_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['hteam']].points_against_game
                        try:
                            percentage_last_x = 100*(points_for_last_x/points_against_last_x)
                        except ZeroDivisionError:
                            percentage_last_x = 100
                    # For byes, add an extra game to cycle through
                    else:
                        games_back += 1
                    i += 1
                
        matches_flipped.at[idx,'h_last_5_wins'] = wins_last_x
        matches_flipped.at[idx,'h_last_5_pts_for'] = points_for_last_x
        matches_flipped.at[idx,'h_last_5_pts_against'] = points_against_last_x
        matches_flipped.at[idx,'h_last_5_pct'] = percentage_last_x
        
    matches = matches_flipped[::-1]
    return matches
        
def last_x_games_stats_ateam(matches: pd.DataFrame, history: History, num_games: int) -> pd.DataFrame:
    """
    Function to create form data for teams by collecting stats on their previous five games.
    The function splits into two branches - one branch handles instances where the team has already
    played the desired number of games in a season. The other branch handles the other case - when
    we need to cycle back a season to complete the form line.
    
    Also need to ensure any stats we wish to populate in the dataset have columns pre-allocated for
    it already. 
    """
    # Get necessary metadata
    teams_in_season = get_season_teams(matches)
    rounds_in_season = get_season_rounds(matches)

    # Pre-populate the columns we're creating
    matches['a_last_5_wins'] = 0
    matches['a_last_5_pct'] = 0
    matches['a_last_5_pts_for'] = 0
    matches['a_last_5_pts_against'] = 0

    # Flip the match dataframe so we can work from latest to oldest
    matches_flipped = matches[::-1]
    for idx,row in matches_flipped.iterrows():
        # Logging
        print(row['season'],row['round'])
        games_back = num_games # Reset for every row
        wins_last_x = 0
        points_for_last_x = 0
        points_against_last_x = 0
        percentage_last_x = 0
        
        # Check how many games the team has played that season
        a_games_played = row['a_played']
        
        # If played equal to or more than the amount of games we want to go back, we don't need to cross a season
        if a_games_played >= games_back:
            # Then we check games until we've checked the games_back amount. Can't just use range, as there may
            # be byes
            i = 0
            while i <= (games_back-1):
                # Not bye
                if (row['round']-i) not in history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['ateam']].bye_rounds:
                    wins_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['ateam']].won_game
                    points_for_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['ateam']].points_for_game
                    points_against_last_x += history.seasons[row['season']].rounds[row['round']-i].teams_ladder_info[row['ateam']].points_against_game
                    try:
                        percentage_last_x = 100*(points_for_last_x/points_against_last_x)
                    except ZeroDivisionError:
                        percentage_last_x = 100
                    
                # For byes, add an extra game to cycle through
                else:
                    games_back += 1
                i += 1
                
        # If played less than the amount we want to go back, and the team participated in the previous season, then
        # we need to cross a season
        # First, check that we haven't run out of seasons
        if ((a_games_played < games_back) and (row['season'] != min(matches['season']))):
            
            # Then, check that the team in question played in the previous season
            if ((a_games_played < games_back) and (row['ateam'] in teams_in_season[row['season']-1])):
                # Implement the same loop as the happy case, but with an extra condition for checking if we need to
                # iterate the season
                i = 0
                season = row['season']
                round_num = row['round']

                while i <= (games_back-1):
                    # Check for season condition, and dial back by one if necessary
                    if (round_num - i == 0):
                        round_num = rounds_in_season[season-1]
                        season = season-1
                    # Now the loop should work the same as before
                    # Not bye
                    if (round_num-i) not in history.seasons[season].rounds[round_num-i].teams_ladder_info[row['ateam']].bye_rounds:
                        wins_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['ateam']].won_game
                        points_for_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['ateam']].points_for_game
                        points_against_last_x += history.seasons[season].rounds[round_num-i].teams_ladder_info[row['ateam']].points_against_game
                        try:
                            percentage_last_x = 100*(points_for_last_x/points_against_last_x)
                        except ZeroDivisionError:
                            percentage_last_x = 100
                    # For byes, add an extra game to cycle through
                    else:
                        games_back += 1
                    i += 1
                
        matches_flipped.at[idx,'a_last_5_wins'] = wins_last_x
        matches_flipped.at[idx,'a_last_5_pts_for'] = points_for_last_x
        matches_flipped.at[idx,'a_last_5_pts_against'] = points_against_last_x
        matches_flipped.at[idx,'a_last_5_pct'] = percentage_last_x
        
    matches = matches_flipped[::-1]
    return matches