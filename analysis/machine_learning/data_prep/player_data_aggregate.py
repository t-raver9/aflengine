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