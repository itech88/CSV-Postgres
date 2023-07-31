import pandas as pd


def transform_data_currency(df):
    # define a list of column names that contain dollar amounts
    dollar_cols = ["Qty", "Gross", "Discounts", "Taxes", "Adjustments", "Net"]

    # remove the dollar sign from the specified columns and convert the values to float

    for col in dollar_cols:
        df[col] = df[col].replace("[\$,]", "", regex=True).astype(float)

    # do I need to return anything if one of these steps fails?
    return df
