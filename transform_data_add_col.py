import pandas as pd
from timer_decorator import timer
from logging_config import configure_logging
from config import new_col_name, new_col_values
logger = configure_logging(__name__)

@timer
def transform_data_add_col(df):
    with open(new_col_name, "r") as file:
        col_name_to_add = file.readline().strip()  # assuming the column name is on the first line
        logger.info(f"New column name is: {col_name_to_add}")

    #check to see if there is a value specified for the new column
    with open(new_col_values, "r") as file:
        col_values_to_add = file.readline().strip() #assuming the values is on the first line
        
    if col_values_to_add:
        df[col_name_to_add] = col_values_to_add
        logger.info(f"New column values are: {col_values_to_add}")
    # if the value is not specified, add NaN values
    else:
        df[col_name_to_add] = pd.np.nan  # using pd.np.nan here for NaN values
        logger.info(f"New column values are: NaN")
    
    logger.info(f"Added new column named: {col_name_to_add} with values: {col_values_to_add}")
    return df
