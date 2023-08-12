import pandas as pd
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_phone_hyphens(df):
    # if the phone column exists 
    if "phone" in df.columns:
        # make the data type varchar
        df["phone"] = df["phone"].astype(str)
        # if the phone column has ten numerical digits
        if df["phone"].str.contains("^[0-9]{10}$").all():
            #add hyphens to the phone column
            df["phone"] = df["phone"].str.replace(r"(\d{3})(\d{3})(\d{4})", r"\1-\2-\3")
            logger.info("Phone column has been formatted with hyphens.")
        else:
            logger.warn("Phone column does not contain ten numerical digits. Nothing formatted.")
            # Log the irregular number and explicitly state the length of the entry
            for index, row in df.iterrows():
                if len(row["phone"]) != 10:
                    logger.warn("Irregular phone number: {}".format(row["phone"]))
    else:
        logger.warn("No phone column found. Nothing formatted.")
            
    return df
