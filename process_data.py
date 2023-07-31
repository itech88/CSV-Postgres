import pandas as pd

# import get_data_csv
# import copy_to_directory
# import copy_to_s3
import transform_data_currency
from transform_data_remove_subtotal_col import transform_data_remove_subtotal_col
import transform_data_full_name_to_id
import os

# import transform_person_type_to_id
import transform_data_rename_percentage

# import transform_data_percentage_to_int
import stage_data_for_ingest
import ingest_data_postgres

# set the path for the CSV to be consumed


# make a function to set variables for the input and output files
def set_input_output_variables():
    # parent directory that holds the raw files and the processed files
    parent_dir = "/Users/itech88/Desktop/Projects/Palmdale/Revolution 22-23/Insurances/VSP/VSP Private"
    # the files will always be in the Raw Reports folder
    input_path = "/Users/itech88/Desktop/Projects/Palmdale/Revolution 22-23/Insurances/VSP/VSP Private/Raw Reports"
    # name the variable for the CSV file
    input_title = "VSP Private 2022"
    input_filename = input_title + ".csv"

    # in the future, need to add functions to get the CSV from Revolution APIs
    # and copy the CSV to the S3 bucket or staging area
    # but for now we can directly process the CSV file
    process_csv_file(input_path, input_title, input_filename, parent_dir)


def process_csv_file(path, title, filename, parent_dir):
    # construct the full path to the CSV file
    full_input_path = os.path.join(path, filename)
    # read the data from the CSV file
    df = pd.read_csv(full_input_path)

    # identify all the currency columns and remove dollar signs
    transform_data_currency.transform_data_currency(df)

    # clean up the provider columns as full name and split into first and last name
    transform_data_full_name_to_id.transform_data_full_name_to_id(df)

    # remove the subtotal column
    df, removal_status = transform_data_remove_subtotal_col(df)
    if removal_status:
        print("Subtotal column removed.")
    else:
        print("No subtotal column found. Nothing removed.")

    # rename the '%' column to 'percentage'
    if transform_data_rename_percentage.transform_data_rename_percentage(df):
        print("Percentage column renamed.")
    else:
        print("No '%' column found. Nothing renamed.")

    # transformations complete, time to stage the data for ingest
    df = stage_data_for_ingest.stage_data_for_ingest(df, title, parent_dir)

    # ingest the data into the database
    ingest_data_postgres.ingest_data_postgres(df, title)


set_input_output_variables()
