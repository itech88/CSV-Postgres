import pandas as pd


def transform_data_percentage_to_int(df):
    # remove the percentage sign from the 'percentage' column,
    # convert the values to floats, and then convert to integers
    if "percentage" in df.columns:
        df["percentage"] = (df["percentage"].str.rstrip("%").astype("float")).astype(
            int
        )

    return df
