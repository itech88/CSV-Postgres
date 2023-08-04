import pandas as pd
import logging


def transform_data_currency(df):
    # define a list of column names that contain dollar amounts
    dollar_cols = ["Gross", "Discounts", "Taxes", "Adjustments", "Net"]

    # if there are no dollar columns, then skip this step
    if not any(col in df.columns for col in dollar_cols):
        logging.info("No dollar columns found.")
        return df
    # if there are dollar columns, then remove the dollar sign and convert to float
    else:
        logging.info(
            "Dollar columns found. Removing dollar sign and converting to float."
        )
        for col in dollar_cols:
            df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)

            # if anything fails, log it
            if df[col].isnull().values.any():
                logging.warning("Failed to convert column {} to float.".format(col))
                return df
            else:
                logging.info("Successfully converted column {} to float.".format(col))
                return df
