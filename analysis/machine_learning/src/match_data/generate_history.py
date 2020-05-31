from .prepare_dataframe import prepare_dataframe
from .generate_match_objects import (
    initialise_history, 
    generate_match_object,
    add_match_to_history
)
import pickle
import os

def generate_history_obj():
    # Create and populate the history object
    matches = prepare_dataframe()
    history = initialise_history(matches)
    matches['match_obj'] = matches.apply(
        lambda row: generate_match_object(row), axis=1) # Generate match objs
    for _,row in matches.iterrows():
        history = add_match_to_history(history, row)

    # Store it
    d = os.path.dirname(os.path.abspath(__file__))
    with open(d + '/data/history_object.pk1','wb') as output:
        pickle.dump(history, output)

    return history

if __name__ == "__main__":
    generate_history_obj()