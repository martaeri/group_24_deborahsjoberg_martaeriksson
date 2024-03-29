# built-in imports
# standard library imports
import pickle
import uuid
from typing import Dict

import pandas as pd

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Movie


def get_data_list() -> list[Movie]:
    # Function responsible for downloading the dataset from the source, translating it
    # into a list of Python objects, and saving it to a Redis list.

    ##### check if dataset already exists, and if so, return the existing dataset  #####
    # db.delete("dataset_list")  # uncomment if you want to force deletion
    if db.exists("dataset_list") > 0:  # checks if the `dataset` key already exists
        current_app.logger.info("Dataset already downloaded.")
        dataset_stored: list[Movie] = []  # empty list to be returned
        raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)  # get list from DB
        for item in raw_dataset:
            dataset_stored.append(pickle.loads(item))  # load item from DB
        return dataset_stored

    ################# dataset has not been downloaded, downloading now #################
    current_app.logger.info("Downloading dataset.")
    original_dataset = pd.read_csv(
        "https://onu1.s2.chalmers.se/datasets/tmdb_5000_movies.csv"
    )

    ########################## saving dataset to the database ##########################
    dataset_base: list[Movie] = []  # list to store the items
    # for each item in the dataset...
    for _, row in original_dataset.iterrows():
        # Check if the score is numeric, if not set it to None
        score_str = row["score"]
        score = float(score_str) if score_str.replace(".", "", 1).isdigit() else None
        # create a new object
        new_movie = Movie(
            id=uuid.uuid4().hex,
            title=row["title"],
            genres=row["genres"],
            runtime=row["runtime"],
            release_date=row["release_date"],
            budget=row["budget"],
            score=score,
        )
        # push object to the database list
        db.rpush("dataset_list", pickle.dumps(new_movie))
        dataset_base.append(new_movie)  # append to the list

    return dataset_base


def calculate_statistics(dataset: list[Movie]) -> Dict[int, float]:
    # Create a dictionary to store the highest rating for each year
    highest_scores: Dict[int, float] = {}

    # Iterate through the dataset to find the highest rating for each year
    for movie in dataset:
        score_str = str(movie.score)
        if score_str.replace(".", "", 1).isdigit():
            release_year = int(movie.release_date.split("-")[0])
            if release_year >= 2000:
                score = float(score_str)
                if release_year not in highest_scores:
                    highest_scores[release_year] = score
                elif score > highest_scores[release_year]:
                    highest_scores[release_year] = score

    return highest_scores


def prepare_figure(input_figure: str) -> str:  # behöver inte ändras
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
