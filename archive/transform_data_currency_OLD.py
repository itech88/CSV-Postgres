import pandas as pd
from datetime import datetime
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_currency(df):
    
    # define a list of column names that contain dollar amounts
    dollar_cols = ["Gross", "Discounts", "Taxes", "Adjustments", "Net", "Amount", "Balance"]
    # convert the column names to lowercase and save
    dollar_cols = [col.lower() for col in dollar_cols]
    # convert the column names to lowercase and save
    df.columns = df.columns.str.lower()
    

    # if there are no dollar columns, then skip this step
    if not any(col in df.columns for col in dollar_cols):
        logger.warning("No dollar columns found.")
        return df
    # if there are dollar columns, then remove the dollar sign and convert to float
    else:
        logger.info(
            "Dollar columns found. Removing dollar sign and converting to float."
        )
        for col in dollar_cols:
            df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)
            ic(df[col].head())

            # if anything fails, log it
            if df[col].isnull().values.any():
                logger.warning("Failed to convert column {} to float.".format(col))
                return df
            else:
                logger.info("Successfully converted column {} to float.".format(col))
                
        return df
