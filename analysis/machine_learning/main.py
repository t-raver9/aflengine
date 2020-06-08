from src.match_data import generate_history
import sys
from src.match_data import (
    prepare_dataframe,
    generate_history
)
from src.ladder_data.resources.columns import ladder_columns
from src.ladder_data import generate_ladders
from src.ladder_data.add_ladders_to_dataframe import (
    add_ladders,
    extract_ladder_data
)
from src.ladder_form import ladder_form
from src.player_data import (
    player_aggregator,
    player_stat_totals
)
import time
import pandas as pd

def main():
    start_time = time.time()
    # Create the dataframe
    # matches = prepare_dataframe.prepare_dataframe()

    # Use the below line if you need to recalculate the history object
    # The history object contains a hierarchy for traversing data. 
    # This is, loosely, history -> season -> round -> match, with round objects
    # Also holding ladders for each team for that round
    # history = generate_history.generate_history_obj()

    # Add ladder information to each round
    # ladder_history = generate_ladders.add_ladders_to_history()

    # Add the ladders from ladder_history to the dataframe as an object
    # matches = add_ladders(ladder_history,matches)

    # Get the information out of the ladder objects, and turn them into columns
    # matches = extract_ladder_data(matches, save_to_file=True)

    # Get the team form for each team
    # matches = ladder_form.get_ladder_form(ladder_history, matches, 5)

    # For testing purposes
    matches = pd.read_csv('/Users/t_raver9/Desktop/projects/aflengine/analysis/machine_learning/src/ladder_form/data/matches_with_form.csv')
    
    # Read player data
    players = player_aggregator.read_data()

    # Add player individual statistic totals for season and career
    # players = player_stat_totals.add_player_totals(matches, players)

    # Aggregate the individual player data to the team level
    matches = player_aggregator.aggregate_player_data(players, matches)

    time_passed = time.time() - start_time
    print(time_passed)

if __name__ == "__main__":
    main()