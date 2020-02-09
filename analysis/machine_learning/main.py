import prepare_data
from ladders import generate_ladder_objects, add_ladders_to_dataset
from os.path import dirname, abspath

d = dirname(dirname(dirname(abspath(__file__))))
save_data_path = d + '/bench/'

def main():
    # Load and prep existing data. This changes some data types, and splits up 
    # quarterly scores into their own columns, e.g. 1.2.8 -> 1 goal, 2 behinds,
    # 8 points. This will also remove finals matches from the dataset.
    matches = prepare_data.prepare_data()

    # Generate ladder information for each row in the dataset, and include
    # it in the relevant row
    ladder_objects = generate_ladder_objects(matches)
    matches = add_ladders_to_dataset(ladder_objects,matches)

    # Write out the new dataset
    matches.to_csv(save_data_path + 'matches_with_ladders.csv')

    print("Ladder file successfully written")


if __name__=="__main__":
    main()