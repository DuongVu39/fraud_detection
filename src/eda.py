import time
import argparse
import pandas as pd
from utils import logging_wrapper
import missingno as msn

import matplotlib.pyplot as plt

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


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Required Args
    parser.add_argument("input", help="Path to input data", type=str)
    parser.add_argument("output", help="Path to output data", type=str)

    # Optional Args
    parser.add_argument("-ll", "--logging_level", help="Level of logging desired", type=int, default=3)
    parser.add_argument("-lp", "--logging_path", help="Path to save log file", type=str,
                        default="./logs/eda_{}.log".format(round(time.time())))

    # Parse arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arguments().__dict__
    logger = logging_wrapper(args['logging_level'], args['logging_path'])

    print("Read in the original data")
    logger.info("Read in the original data")
    df = pd.read_csv(args["input"])

    print(df.info)
    logger.info("Info: \n", df.info)

    print(df.shape)
    logger.info("Shape: \n", df.shape)

    desc = df.describe()
    desc.to_csv(args["output"])

    print('Label distribution:')
    df.is_attributed.value_counts(normalize=True).plot.bar(figsize=(10, 7), color='orange')
    plt.savefig("label_dist.png")

    print(df.is_attributed.value_counts(normalize=True))
    print(df.is_attributed.value_counts())

    print("Feature Exploration")
    for i in df.columns:
        print("\n There are {} unique values out of {} values of feature {}".format(df["{}".format(i)].nunique(),
                                                                                    df["{}".format(i)].count(), i))
        print("\n Top 5 values of feature {}:".format(i))
        feat_df = pd.DataFrame(df["{}".format(i)].value_counts())
        print(feat_df.head())

    print("Explore missing value:")
    msn.bar(df)
    plt.savefig("missing_value.png", color='orange')



