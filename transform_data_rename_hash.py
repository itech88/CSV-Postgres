import pandas as pd
import transform_data_phone_hyphens
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_rename_hash(df):
    # if this col exits
    if "#" in df.columns:
        # Drop any rows where '#' column is NaN
        df.dropna(subset=["#"], inplace=True)

        # rename the '%' column to 'percentage'
        df.rename(columns={"#": "phone"}, inplace=True)
        logger.info("Phone column renamed.")
        # add hyphens and make varchar
        transform_data_phone_hyphens.transform_data_phone_hyphens(df)
                
    else:
        logger.warn("No '#' column found. Nothing renamed.")
