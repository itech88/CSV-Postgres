import pandas as pd
import logging


def transform_data_currency(df):
    # define a list of column names that contain dollar amounts
    dollar_cols = ["Gross", "Discounts", "Taxes", "Adjustments", "Net"]
    # remove the dollar sign from the specified columns and convert the values to float
    for col in dollar_cols:
        df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)
        # if anything fails, log it
        if df[col].isnull().values.any():
            logging.warning("Failed to convert column {} to float.".format(col))

    return df
