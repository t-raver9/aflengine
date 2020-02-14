import prepare_data
from ladders import generate_ladder_objects, add_ladders_to_dataset
from os.path import dirname, abspath
from team_form import last_x_games_stats_hteam, last_x_games_stats_ateam
from features import days_break, x_game_average_break
from aggregate_player_data import read_player_data,aggregate_player_data

d = dirname(dirname(dirname(abspath(__file__))))
save_data_path = d + '/bench/'

def main():
    # Load and prep existing data. This changes some data types, and splits up 
    # quarterly scores into their own columns, e.g. 1.2.8 -> 1 goal, 2 behinds,
    # 8 points. This will also remove finals matches from the dataset.
    matches = prepare_data.prepare_data()

    # Generate ladder information for each row in the dataset, and include
    # it in the relevant row
    history_object = generate_ladder_objects(matches)
    matches = add_ladders_to_dataset(history_object,matches)

    # Add form data to the dataset. This includes wins, percentage and points
    # for/against over the last x games (to be defined by user)
    # matches = last_x_games_stats_hteam(matches=matches,history=history_object,num_games=5)
    # matches = last_x_games_stats_ateam(matches=matches,history=history_object,num_games=5)

    # Add days break since last game, and average break over the past 3 games
    matches = days_break(matches)
    # matches = x_game_average_break(matches,num_games=3)

    # Read in player data and the aggregate individual stats to team level
    players = read_player_data()
    matches = aggregate_player_data(matches,players)

    # Write out the new dataset
    matches.to_csv(save_data_path + 'matches_with_player_data.csv')
    print("Ladder/form/breaks file successfully written")

if __name__=="__main__":
    main()