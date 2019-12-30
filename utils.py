import os
import configparser


def setup_api_locally():
    parser = configparser.ConfigParser()
    parser.read('KAGGLE_CONFIG.ini')
    os.environ["KAGGLE_USERNAME"] = parser["KAGGLE_API"]["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = parser["KAGGLE_API"]["KAGGLE_KEY"]


def load(competition):
    folder = "/data/{}".format(competition)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.system("kaggle competitions download -c {} -path {}".format(competition, folder))


setup_api_locally()
load('google-quest-challenge')
