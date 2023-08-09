import pandas as pd
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_percentage_to_int(df):
    # remove the percentage sign from the 'percentage' column,
    # convert the values to floats, and then convert to integers
    if "percentage" in df.columns:
        df["percentage"] = (df["percentage"].str.rstrip("%").astype("float")).astype(
            int
        )
        logger.info("Percentage column converted to integers.")

    return df
