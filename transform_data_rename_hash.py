import pandas as pd
import transform_data_phone_format
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_rename_hash(df):
    # if this col exits
    if "#" in df.columns:
        # Option to drop any rows where '#' column is NaN
        response = input("Do you want to drop rows where '#' column is NaN? (y/n) ")
        if response.lower() == "y":
            # show the rows that are about to be dropped
            logger.info("Rows about to be dropped where '#' column is NaN:")
            ic((df[df["#"].isnull()]))
            logger.info(df[df["#"].isnull()])
            df.dropna(subset=["#"], inplace=True)
            logger.info("Successfully dropped rows where '#' column is NaN.")
        else:
            logger.info("Rows not dropped where '#' column is NaN.")


        # rename the '%' column to 'percentage'
        df.rename(columns={"#": "phone"}, inplace=True)
        logger.info("Phone column renamed.")
        # add hyphens and make varchar
        transform_data_phone_format.transform_data_phone_format(df)
                
    else:
        logger.warn("No '#' column found. Nothing renamed.")
