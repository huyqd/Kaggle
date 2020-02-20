import configparser
import os
import zipfile
from datetime import datetime
from pathlib import Path
import inspect

root_path = Path(__file__).parent
general_data_path = root_path / 'data'


def setup_api_locally():
    parser = configparser.ConfigParser()
    parser.read(root_path / 'KAGGLE_CONFIG.ini')
    os.environ["KAGGLE_USERNAME"] = parser["KAGGLE_API"]["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = parser["KAGGLE_API"]["KAGGLE_KEY"]


def load(competition):
    folder = root_path / "data/{}".format(competition)
    if not folder.is_dir():
        folder.mkdir()
    os.system("kaggle competitions download -c {} -p {}".format(competition, str(folder)))

    # Upzip download
    fname = folder / f"{competition}.zip"

    print("Extracting file...")
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(folder)

    print("Removing zip file...")
    os.remove(fname)

    print("Finished!")

    return


def submit(competition, fname='submission.csv', message=None):
    """ Submit to Kaggle """
    folder = root_path / "{}".format(competition)
    fname += '' if fname.endswith('.csv') else '.csv'
    fname = folder / fname
    message = message if message else f"""Submission at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""

    if not fname.exists():
        raise ValueError('Please save the output in "submit.csv" or point to a valid submit file.')

    os.system(f'kaggle competitions submit -c {competition} -f {str(fname)} -m "{message}"')

    return


def get_competition_data_path(competition=None):
    """ Return train, test, and sample submission data path """
    # Get the competition name from the directory
    if not competition:
        # Get the parent directory of the caller
        stack = inspect.stack()
        filename = stack[1].filename
        if 'ipython-input' in filename:
            raise ValueError("Competition name is required to run this function with jupyter notebook!")

        competition = Path(stack[1].filename).parent.name

    # Get the data folder and all files within
    competition_data_path = general_data_path / competition
    all_files = [f for f in competition_data_path.iterdir()]

    # Get file paths based on file names
    train_path = [f for f in all_files if 'train' in str(f)]
    test_path = [f for f in all_files if 'test' in str(f)]
    sample_submission_path = [f for f in all_files if 'submission' in str(f)]


    X_train_path = competition_data_path / 'X_train.csv'
    X_test_path = competition_data_path / 'X_test.csv'
    y_train_path = competition_data_path / 'y_train.csv'
    y_test_path = competition_data_path / 'y_test.csv'

    return dict(competition_path=competition_data_path,
                train_path=train_path[0] if train_path else None,
                test_path=test_path[0] if test_path else None,
                sample_submission_path=sample_submission_path[0] if sample_submission_path else None,
                X_train_path=X_train_path,
                y_train_path=y_train_path,
                X_test_path=X_test_path,
                y_test_path=y_test_path)


def print_caller_info():
    # Get the full stack
    stack = inspect.stack()

    # Get one level up from current
    previous_stack_frame = stack[1]
    print(previous_stack_frame.filename)  # Filename where caller lives

    # Get the module object of the caller
    calling_module = inspect.getmodule(stack[0])
    print(calling_module)
    print(calling_module.__file__)


if __name__ == '__main__':
    setup_api_locally()
    load('titanic')
