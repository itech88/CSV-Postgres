import pandas as pd
import transform_data_percentage_to_int
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_rename_percentage(df):
    # if this col exits
    if "%" in df.columns:
        # Drop any rows where '%' column is NaN
        df.dropna(subset=["%"], inplace=True)

        # rename the '%' column to 'percentage'
        df.rename(columns={"%": "percentage"}, inplace=True)
        logger.info("Percentage column renamed.")
        # remove the percentage sign from the 'percentage' column,
        # convert the values to float,
        # and multiply by 100 to get the percentage as an integer
        transform_data_percentage_to_int.transform_data_percentage_to_int(df)
                
    else:
        logger.warn("No '%' column found. Nothing renamed.")
