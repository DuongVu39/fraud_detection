import time
import pandas as pd

# Self Imports:
from src.utils import logging_wrapper


def order_by_time(df, logger=None):
    df['click_time'] = pd.to_datetime(df['click_time'])

    print("Sorting by click time and reset index")
    if logger:
        logger.info("Sorting by click time and reset index")

    df = df.sort_values("click_time").reset_index(drop=True)

    return df


def _rate_encode_category(x):
    """Rate encodes a single categorical column. Value in the column represents the frequency the category occurred."""
    raw_count = x.value_counts().loc[x]
    rate = raw_count / x.shape[0]
    return rate.values


def rate_encode_df(df, to_rate_encode, replace=True, prefix='rate_'):
    """
    Interface to rate encode categorical variables specified in the fraud_lib.preprocessing.model module.

    Args:
        df (DataFrame):
        replace (bool): If True, replaces the column with the rate encoded values.
        prefix (str): Used for new column names if replace is False.
        to_rate_encode (list):

    Returns:
        (DataFrame): Input DataFrame with updated columns, either replaced or new.
    """
    if not isinstance(to_rate_encode, list):
        if isinstance(to_rate_encode, str):
            to_rate_encode = [to_rate_encode]
        else:
            raise ValueError(f"`to_rate_encode` must be a list or str. {type(to_rate_encode)} not accepted.")
    else:

        if not replace:
            try:
                new_cols = df.loc[:, to_rate_encode].apply(_rate_encode_category, axis=0)
                new_col_names = [f"{prefix}_{i}" for i in new_cols.columns]
                new_cols.columns = new_col_names
                df = df.join(new_cols)

            except TypeError as e:  # If the slice is just a single series, dont need to use apply really.
                if len(to_rate_encode) == 1:
                    df[f"{prefix}_{to_rate_encode[0]}"] = _rate_encode_category(df.loc[:, to_rate_encode[0]])
        else:
            try:
                df.loc[:, to_rate_encode] = df.loc[:, to_rate_encode].apply(_rate_encode_category, axis=0)
            except TypeError as e:  # If the slice is just a single series, axis shouldn't be passed.
                if len(to_rate_encode) == 1:
                    df.loc[:, to_rate_encode] = _rate_encode_category(df.loc[:, to_rate_encode[0]])

        return df



