import pandas as pd
from datetime import datetime
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)
'''
First the function reads all columns from reports.
Then all df.columns are lowercased for consistency
'''
@timer
def transform_data_lowercase_cols(df):
    """Lowercases all column names in the DataFrame for consistency.

    Parameters:
        df: DataFrame whose columns are to be lowercased.
    """
    df.columns = map(str.lower, df.columns)
    logger.info("All columns have been lowercased.")
    return df