import pandas as pd
import numpy as np
from os.path import dirname, abspath
from feature_extraction import per_game_stats, determine_winner, home_away_features
from feature_extraction import create_diff_cols, create_diff_features

def read_data() -> pd.DataFrame:
    d = dirname(dirname(dirname(dirname(abspath(__file__)))))
    matches = pd.read_csv(d + "/bench/matches_plus.csv")
    return matches

def save_data(home_away_df: pd.DataFrame) -> None:
    d = dirname(dirname(dirname(dirname(abspath(__file__)))))
    save_data_path = d + '/bench/'
    home_away_df.to_csv(save_data_path + '/match_features.csv')

def main():
    # Read in data
    matches = read_data()

    # Create per-game statistics, and create a column indicating the winner
    matches = per_game_stats(matches)
    matches = determine_winner(matches)

    # Create a dataframe with the requisite stats for home and away teams
    home_away_df = home_away_features(matches)

    # Save this, for testing purposes

    # Create a dataframe that holds the difference between home and away teams
    # in the previous dataframe. Positive values indicate the home team wins
    # in that stat - i.e. if points_per_game_ave_diff = -10.5, then the away
    # team for that game averages 10.5 more points per game
    diff_cols = create_diff_cols()
    print('Creating the dataframe with differences between home and away')
    diff_df = create_diff_features(diff_cols, home_away_df)

    # Write the results to file
    save_data(diff_df)
    print('Feature dataframe successfully created')

if __name__ == "__main__":
    main()