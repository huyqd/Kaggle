import os
import configparser


def data_exists(competition):
    return os.path.isdir("/data/" + competition)


def setup_api_locally():
    parser = configparser.ConfigParser()
    parser.read('KAGGLE_CONFIG.ini')
    os.environ["KAGGLE_USERNAME"] = parser["KAGGLE_API"]["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = parser["KAGGLE_API"]["KAGGLE_KEY"]


def load(competition):
    assert competition.count(" ") == 0
    if not data_exists(competition):
        os.system("kaggle competitions download {}".format(competition))

setup_api_locally()
load('test')