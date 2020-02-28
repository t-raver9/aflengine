import pandas as pd
from os.path import dirname,abspath
from copy import deepcopy

def read_player_data() -> pd.DataFrame:
    """
    Read in individual player data for each game
    """
    d = dirname(dirname(dirname(dirname(abspath(__file__)))))
    players = pd.read_csv(d + "/bench/players.csv")
    return players

def aggregate_player_data(matches: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the player data to the match/team level, then join it back to our
    matches dataframe. Each player row has a match key, and the team for
    which he plays.
    """
    # Define the columns that will be involved in the aggregation
    cols_required = ['AFLfantasy', 'Supercoach', 'behinds', 'bounces', 'brownlow',
       'clangers', 'clearances', 'contested_marks', 'contested_poss',
       'disposals','frees_against', 'frees_for',
       'goal_assists', 'goals', 'handballs', 'hitouts', 'homeAway',
       'inside50', 'kicks', 'marks', 'marks_in_50',
       'one_percenters', 'rebound50',
       'tackles',  'uncontested_poss', 'centre_clearances',
       'disposal_efficiency', 'effective_disposals', 'intercepts',
       'metres_gained', 'stoppage_clearances', 'score_involvements',
       'tackles_in_50', 'turnovers', 'matchid','team'] # Match key

    # Group by the matchid and team, and get the aggregate of all other stats
    aggs = players[cols_required].groupby(['matchid','team']).agg(sum)

    # Join these stats onto the matches dataframe
    aggs_h = deepcopy(aggs)
    aggs_a = deepcopy(aggs)
    aggs_h.columns = aggs.columns.map(lambda x: str(x) + '_h')
    aggs_a.columns = aggs.columns.map(lambda x: str(x) + '_a')
    matches = matches.merge(aggs_h,how='left',left_on=['hteam','matchid'],right_on=['team','matchid'])
    matches = matches.merge(aggs_a,how='left',left_on=['ateam','matchid'],right_on=['team','matchid'])

    return matches

def games_played_per_player(players: pd.DataFrame) -> pd.DataFrame:
    games_played_player_dict = {}
    for idx,row in players.iterrows():
        if row['playerid'] not in games_played_player_dict:
            games_played_player_dict[row['playerid']] = 1
            players.at[idx,'player_gp'] = 1
        else:
            games_played_player_dict[row['playerid']] += 1
            players.at[idx,'player_gp'] = games_played_player_dict[row['playerid']]
            
    return players

def games_played_per_team(matches: pd.DataFrame, players: pd.DataFrame):
    # Join the players and matches dataframes on the matchid
    merged = players.merge(matches,on='matchid',how='inner',suffixes=('_x','_y'))
    # Initialise games played columns for both teams
    matches['h_games_played'] = 0
    matches['a_games_played'] = 0
    # Create the grouped dataframe with the aggregate of games played
    aggregation = merged[['matchid','team','player_gp']].groupby(['matchid','team']).sum()
    aggregation.reset_index(inplace=True)
    # Find the relevant row to places the games played
    current_season = min(matches['season'])
    for idx,row in matches.iterrows():
        # Logging
        if row['season'] != current_season:
            print('Collecting games played data for season {}'.format(row['season'])) # Logging
        current_season = row['season'] # Logging
        matches.at[idx,'h_games_played'] = aggregation[(aggregation['matchid'] == row['matchid']) &
                                                      (aggregation['team'] == row['hteam'])]['player_gp']
        matches.at[idx,'a_games_played'] = aggregation[(aggregation['matchid'] == row['matchid']) &
                                                      (aggregation['team'] == row['ateam'])]['player_gp']

    return matches

def games_played(matches: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    players = games_played_per_player(players)
    matches = games_played_per_team(matches,players)
    return matches