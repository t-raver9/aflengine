from copy import deepcopy
import pandas as pd
from ladder_classes import Team_ladder_info, Season, Round_obj, History
from metadata import get_season_teams

def generate_ladder_objects(matches: pd.DataFrame, current_season: int = 2000) -> History:
    """
    Takes the matches dataframe and generates a "history" object containing
    all ladder information. The heirachy of objects is 
    history -> season -> round -> teams_ladder_info. For example, if you wanted
    to access Melbourne's ladder up to round 7 in the year 2000, you would
    access history.seasons[2000].rounds[7].teams_ladder_info['Melbourne'].

    A "Round 0" ladder is also created with all teams starting on equal points
    and percentage before games start. This data will be required for features
    of round 1 games.
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
            
            # Add the "ladder round zero" objects, i.e. the default ladder before the season starts
            for team in teams_in_season[current_season]:
                team_ladder_info = Team_ladder_info(team)
                current_round_obj.add_ladder_info(team,team_ladder_info)
                
            # Start with empty teams not seen for initialisation
            teams_not_seen = []
                
        # Create round object when we start a new round
        if (row['round'] != current_round):

            # Before creating a new round object, add ladder objects for the previous round for any bye teams
            for bye_team in teams_not_seen:
                bye_team_ladder_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].teams_ladder_info[bye_team])
                bye_team_ladder_info.add_bye_round(current_round)
                current_round_obj.add_ladder_info(bye_team,bye_team_ladder_info)
                
            # Then, order the ladder positions based on prem points and percentage
            current_round_obj= update_ladder_positions(current_round_obj) #CHECK THIS
            current_round = row['round']
            current_round_obj = Round_obj(round_num=current_round,teams=teams_in_season[current_season])
            
            # Add this round object to the season object
            season_obj.add_round(current_round_obj,current_round)
            
            #Track which teams have played this round so we know when a bye has occured
            teams_not_seen = [team for team in season_obj.teams]
            
        # For the teams in the match, inherit the previous round's ladder object and update it
        home_team_ladder_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].teams_ladder_info[row['hteam']])
        away_team_ladder_info = deepcopy(history.seasons[current_season].rounds[current_round - 1].teams_ladder_info[row['ateam']])
        home_team_ladder_info.update_ladder_info(match_data=row)
        away_team_ladder_info.update_ladder_info(match_data=row)
        current_round_obj.add_ladder_info(row['hteam'],home_team_ladder_info)
        current_round_obj.add_ladder_info(row['ateam'],away_team_ladder_info)
        
        # Append teams to the teams seen list so we know when byes are occuring
        teams_not_seen.remove(row['hteam'])
        teams_not_seen.remove(row['ateam'])
        
        # Track the round so we know when to create a new round object
        current_round = row['round']

    return history

def update_ladder_positions(current_round_obj: Round_obj) -> Round_obj:
    """
    Function that takes in a round object, containing the ladder information for
    each team in that round, and updates the ladder position of each team
    """
    # Create a dataframe where the columns are team, prem points and percentage
    ladder_list = []
    for team_obj in current_round_obj.teams_ladder_info.values():
        ladder_list.append([team_obj.team,team_obj.prem_points,team_obj.percentage])
    round_ladder_df = pd.DataFrame(ladder_list,columns=['team','prem_points','percentage'])
    round_ladder_df.sort_values(by=['prem_points','percentage','team'],inplace=True,ascending=False)
    
    # Update the ladder positions of each team inside the round object
    pos = 1
    for _,row in round_ladder_df.iterrows():
        team = row[0]
        current_round_obj.teams_ladder_info[team].ladder_position = pos
        pos += 1
    
    return current_round_obj

def add_ladders_to_dataset(history: History, matches: pd.DataFrame) -> pd.DataFrame:
    """Takes the history object and adds all relevant ladder information
    to the matches dataset. Need to define these manually."""
    # Include all new attributes for the dataframe
    new_cols = ['h_wins','h_losses','h_draws','h_points_for','h_points_against',
    'h_percentage','h_ladder_position','h_played','a_wins','a_losses','a_draws',
    'a_points_for','a_points_against','a_percentage','a_ladder_position','a_played']

    for col in new_cols:
        matches[col] = None

    current_season = 0
    for idx,row in matches.iterrows():

        if current_season != row['season']:
            print('Writing ladders from {} to dataset'.format(current_season))
            current_season = row['season']
        
        matches.at[idx,'h_wins'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].wins
        matches.at[idx,'h_losses'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].losses
        matches.at[idx,'h_draws'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].draws
        matches.at[idx,'h_points_for'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].points_for
        matches.at[idx,'h_points_against'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].points_against
        matches.at[idx,'h_percentage'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].percentage
        matches.at[idx,'h_ladder_position'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].ladder_position
        matches.at[idx,'h_played'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['hteam']].played
        matches.at[idx,'a_wins'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].wins
        matches.at[idx,'a_losses'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].losses
        matches.at[idx,'a_draws'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].draws
        matches.at[idx,'a_points_for'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].points_for
        matches.at[idx,'a_points_against'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].points_against
        matches.at[idx,'a_percentage'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].percentage
        matches.at[idx,'a_ladder_position'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].ladder_position
        matches.at[idx,'a_played'] = history.seasons[row['season']].rounds[row['round']].teams_ladder_info[row['ateam']].played

    # Reset the index, which is now jumbled and meaningless
    matches.reset_index(drop=True,inplace=True)
    return matches