import pandas as pd
from datetime import datetime
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def transform_data_currency(df):
    # define a list of column names from Revolution reports that contain dollar amounts
    dollar_cols = ["gross", "discounts", "taxes", "adjustments", "net", "amount", "balance"]
    # convert the column names to lowercase and save
    df.columns = df.columns.str.lower()
    # compare the df.columns to the dollar_cols list and return a list of columns that are in both
    report_dollar_cols = [col for col in df.columns if col in dollar_cols]
    ic(f'Dollar signs in the DF', report_dollar_cols)

    # if there are no dollar columns, then skip this step
    if len(report_dollar_cols) == 0:
        logger.info("No dollar columns found in the report")
        return df
    # if there are dollar columns, then continue
    else:
        # log the dollar columns found
        logger.info("Dollar columns found: {}".format(report_dollar_cols))
        # run a for loop to remove the dollar sign and convert to float
        for col in report_dollar_cols:
            # remove the dollar sign and convert to float
            df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)
            # if anything fails, log it
            if df[col].isnull().values.any():
                # log the error and the row that failed
                logger.warning("Failed to convert column '{}' to float.".format(col))
                # log the row that failed
                logger.warning("The row that failed is: {}".format(df[df[col].isnull()]))
                logger.warning(df[df[col].isnull()])
                continue
            else:
                logger.info("Successfully converted column '{}' to float.".format(col))

        # No need to add the cols in report_dollar_cols to the end of df.columns
        # since you have already replaced the original columns with the transformed values

        # No need to drop the original columns either, as they've already been transformed

        ic(f'Removed dollar sign from affected columns', df)
        return df
