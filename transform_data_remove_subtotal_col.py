import pandas as pd


# this could be a dependent upon the first column being 'Providers'
# or another field type, such as Patients, it depends on report
def transform_data_remove_subtotal_col(df):
    # identify all possible column headers for the first column
    # in this order, providers will never be a first column becaues the transformation that happened earlier
    first_column_headers = [
        "employee_id",
        "patient_id",
        "Locations",
        "Card Type",
        "Code",
    ]
    removal = ""
    # if the first column is in the list of possible column headers
    if df.columns[0] in first_column_headers:
        # remove the subtotal row where 'first_column_headers' is null or empty
        df = df[df[df.columns[0]].notna() & df[df.columns[0]].ne("")]
        removal = True
    else:
        print(
            f"The first column is not in list of possible column headers: [{first_column_headers}]"
        )
        print("The first column is named: " + df.columns[0])
        removal = False

    return df, removal
