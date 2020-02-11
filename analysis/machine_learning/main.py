import prepare_data
from ladders import generate_ladder_objects, add_ladders_to_dataset
from os.path import dirname, abspath
from team_form import last_x_games_stats_hteam, last_x_games_stats_ateam

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
    matches = last_x_games_stats_hteam(matches=matches,history=history_object,num_games=5)
    matches = last_x_games_stats_ateam(matches=matches,history=history_object,num_games=5)

    # Write out the new dataset
    matches.to_csv(save_data_path + 'matches_with_ladders.csv')
    print("Ladder file successfully written")
    print(matches.head(10))


if __name__=="__main__":
    main()