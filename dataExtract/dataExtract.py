import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import patoolib
import os
import json


# ------------------------------------------------
# This method authenticates with the Kaggle API, 
# downloads the competition data and extract
# the archive
# ------------------------------------------------
def downloadData():

    # Construct the relative path to the JSON config file
    configPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

    # Read the JSON config file
    with open(configPath, 'r') as file:
        configText = file.read()
    config = json.loads(configText)
    competitionName = config["Competition"]
    path = config["ExtractionPath"]

    # Authenticate to the kaggle api and extract data
    print("Kaggle API authentication")
    api = KaggleApi()
    api.authenticate()
    print("Extract Data From API")
    kaggle.api.competition_download_files(competitionName, path=path)
    patoolib.extract_archive(f"{path}{competitionName}.zip", outdir="datasets")

if __name__ == '__main__':
    downloadData()
