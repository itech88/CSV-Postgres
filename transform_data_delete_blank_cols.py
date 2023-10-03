import pandas as pd
import numpy as np
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

'''this function asks the user if it is ok to delete blank or NaN columns
then a log is recorded upon deletion, if not ok to delete nothing happens'''
@timer
def transform_data_delete_blank_cols(df):
    for col in df.columns:
        if 'Unnamed' in col:
            response = input(f"Delete blank/unnamed column: [{col}]? (y/n): ")
            if response.lower() == "y":                
                df.drop(columns=col, inplace=True)
                logger.info(f"Deleted blank column: [{col}]")
                ic(df.head())
            else:
                continue
        elif pd.isnull(col):
            response = input(f"Delete NaN column: [{col}]? (y/n): ")
            if response.lower() == "y":
                df.drop(columns=col, inplace=True)
                logger.info(f"Deleted NaN column: [{col}]")
            else:
                continue

    # No return statement is needed

    