import pandas as pd
from datetime import datetime
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)
'''
First the function defines a list of all columns from reports that contain dollar signs and convert to lowercase.
Then that list is compared against the df.columns to find union columns. If none found, skip ahead.
If found, log and loop through the list to remove the dollar sign and convert datatype to float.
Logging will record any failures and successes
'''
@timer
def transform_data_currency(df):   
    # should I make this a config file list? 
    dollar_cols = ["gross", "discounts", "taxes", "adjustments", "net", "amount", "balance", "total $ paid"]    
    df.columns = df.columns.str.lower()    
    report_dollar_cols = [col for col in df.columns if col in dollar_cols]
    ic(f'Dollar signs in the DF', report_dollar_cols)

    if len(report_dollar_cols) == 0:
        logger.info("No dollar columns found in the report")
        return df
    
    else:        
        logger.info("Dollar columns found: {}".format(report_dollar_cols))
        
        for col in report_dollar_cols:           
            df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)            
            if df[col].isnull().values.any():
                # this warning logging is super messy, need unit test to clean it up
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
