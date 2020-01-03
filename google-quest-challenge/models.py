from utils import root_path
import pandas as pd
import numpy as np
import scipy as scp


def randomize(test: pd.DataFrame):
    """ Take a dataframe and randomize the result """
    sample_submission = pd.read_csv(root_path / 'data' / 'google-quest-challenge' / 'sample_submission.csv')
    required_output_cols = sample_submission.columns

    n_output_rows, n_output_cols = test.shape[0], 30

    # Retrieve columns to predict
    predict_cols = required_output_cols[-n_output_cols:]

    # Get the result
    randomized_res = np.random.rand(n_output_rows, n_output_cols)
    randomized_res = pd.DataFrame(randomized_res, columns=predict_cols)
    randomized_res = pd.concat([test, randomized_res], axis=1, sort=False)
    randomized_res = randomized_res.reindex(columns=required_output_cols)

    return randomized_res


if __name__ == '__main__':
    test = pd.read_csv(root_path / 'data' / 'google-quest-challenge' / 'test.csv')
    res = randomize(test)
