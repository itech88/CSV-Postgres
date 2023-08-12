import pandas as pd
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

# this could be a dependent upon the first column being 'Providers'
# or another field type, such as Patients, it depends on report
@timer
def transform_data_remove_subtotal_col(df):
    # a subtotal is a cell that is the last row in the dataframe
    
    # a subtotal is a cell that is the last row in the dataframe
    for col in df.columns:
        last_row = df[col].iloc[-1]
        # identify if all the values in the column are numeric
        col_is_numeric = pd.to_numeric(df[col], errors='coerce').notnull().all()
        # if the column is numeric, then it is a candidate for a subtotal column
        if col_is_numeric:
            logger.info(f"Column is numeric: {col}")
            ic(df.tail())
            logger.info(f"Last row: {last_row}")
            evaluate = df[col].iloc[:-1].sum()
            ic(evaluate)
            # if last_row is a sum of all the cells in that column except the last one, then it is a subtotal
            if last_row == evaluate:  # exclude the last row in the sum
                subtotal_col = col
                logger.info(f"Subtotal column found: {subtotal_col}")
                # now remove the entire row where the subtotal is found
                df = df[df[col] != last_row]
                logger.info(f"Subtotal column removed: {subtotal_col}")
                ic(df.tail())
                # after a subtotal column is found, exit the loop since the subtotal row has been removed for all columns
                break
            else:
                logger.info(f"Subtotal column not found: Here's the tail")
                ic(df.tail())
                logger.info(df.tail())
        else:
            logger.info(f"Column is not numeric: {col}")
            logger.info(f"Last row: {last_row}")
            continue

    return df
