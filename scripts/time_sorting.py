"""
Sorting the data by time and save it as a new data set

Sample usage from terminal:
    python time_sorting.py train.csv train_sorted.csv


Args:
    input(str): Path to the original data set
    logging_level(int): Default=3. 1-5 scale determining the logging messages to save.
                        5 is only CRITICAL, 1 is all message
    logging_path(dir): Default=logs/{scipt_name}_{unix_time}.log
                        Path to the desired location to store logs

Returns:
    output(str): Path to output file with sorted click time
"""


import time
import argparse
import pandas as pd
from src.utils import logging_wrapper
from src.preprocessing import order_by_time


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Path to input data", type=str)
    parser.add_argument("output", help="Path to output data", type=str)

    # Optional Args
    parser.add_argument("-ll", "--logging_level", help="Level of logging desired", type=int, default=3)
    parser.add_argument("-lp", "--logging_path", help="Path to save log file", type=str,
                        default="./logs/time_sorting_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments().__dict__
    logger = logging_wrapper(args['logging_level'], args['logging_path'])

    print("Read in the original data")
    logger.info("Read in the original data")
    df = pd.read_csv(args["input"])

    df = order_by_time(df, time_col='click_date', logger=logger)

    print("Saving new sorted data set...")
    logger.info("Saving new sorted data set...")
    df.to_csv(args['output'], index=False)
