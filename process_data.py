import pandas as pd
import os
from config import parent_dir, input_path, input_filename

# import all the helper modules/micro-services
# import get_data_csv
# import copy_to_directory
# import copy_to_s3
import transform_data_currency
from transform_data_remove_subtotal_col import transform_data_remove_subtotal_col
import transform_data_full_name_to_id


# import transform_person_type_to_id
import transform_data_rename_percentage

# import transform_data_percentage_to_int
import stage_data_for_ingest
import ingest_data_postgres


# make a function to set variables for the input and output files
def set_input_output_variables():
    # most_recent_file = os.listdir(input_path)[-1]

    # read the path inside input_filename.txt
    with open(input_filename, "r") as file:
        csv_path = file.readline().strip()  # assume the path is on the first line
    # get the base name of the CSV file
    csv_basename = os.path.basename(csv_path)
    # remove the .csv extension
    input_title = os.path.splitext(csv_basename)[0]

    # in the future, need to add functions to get the CSV from Revolution APIs
    # and copy the CSV to the S3 bucket or staging area
    # but for now we can directly process the CSV file
    process_csv_file(csv_path, input_title, parent_dir)


def process_csv_file(csv_path, title, parent_dir):
    # construct the full path to the CSV file
    # full_input_path = os.path.join(path, filename)
    # print(full_input_path)
    # read the data from the CSV file
    df = pd.read_csv(csv_path)

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
