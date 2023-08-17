from icecream import ic, install
install() # this installs ic project wise to other modules
from timer_decorator import timer
import pandas as pd
import os
from logging_config import configure_logging
logger = configure_logging(__name__)
from config import parent_dir, input_path, input_filename


# import all the helper modules/micro-services
# import copy_to_directory
# import copy_to_s3

# delete blank cols
import transform_data_delete_blank_cols
import transform_data_currency
from transform_data_remove_subtotal_col import transform_data_remove_subtotal_col
import transform_data_full_name_to_id # transform_person_type_to_id will be encapsulated in transform_data_full_name_to_id
import transform_data_rename_percentage # transform_data_percentage_to_int will be encapsulated in transform_data_rename_percentage
import transform_data_rename_hash # transform_data_phone_format will be encapsulated in transform_data_rename_hash
import transform_data_add_col
import stage_data_for_ingest
import ingest_data_postgres


# make a function to set variables for the input and output files
@timer
def set_input_output_variables():
    # most_recent_file = os.listdir(input_path)[-1]

    # read the path inside input_filename.txt
    with open(input_filename, "r") as file:
        csv_path = file.readline().strip()  # assume the path is on the first line
        ic(csv_path)
    # get the base name of the CSV file
    csv_basename = os.path.basename(csv_path)
    ic(csv_basename)
    # remove the .csv extension
    input_title = os.path.splitext(csv_basename)[0]
    # lowercase the title for postgres
    input_title = input_title.lower()
    # replace spaces with underscores for postgres
    input_title = input_title.replace(" ", "_")
    # replace dashes with underscores for postgres
    input_title = input_title.replace("-", "_")
    # replace slashes with underscores for postgres
    input_title = input_title.replace("/", "_")
      
    ic(input_title)

    # in the future, need to add functions to get the CSV from Revolution APIs
    # and copy the CSV to the S3 bucket or staging area
    # but for now we can directly process the CSV file
    process_csv_file(csv_path, input_title, parent_dir)

@timer
def process_csv_file(csv_path, title, parent_dir):
    # read the data from the CSV file
    df = pd.read_csv(csv_path)

    # delete blank columns
    transform_data_delete_blank_cols.transform_data_delete_blank_cols(df)  
    ic(df.head())
    # identify all the currency columns and remove dollar signs
    transform_data_currency.transform_data_currency(df)
    
    # clean up the provider columns as full name and split into first and last name
    transform_data_full_name_to_id.transform_data_full_name_to_id(df)
    
    # remove the subtotal column
    df = transform_data_remove_subtotal_col(df)
            
    # rename the '%' column to 'percentage'
    transform_data_rename_percentage.transform_data_rename_percentage(df)
       
    # rename the '#' column to 'phone'
    transform_data_rename_hash.transform_data_rename_hash(df)
    # ad hoc transformation, ability to add any new columns needed
    transform_data_add_col.transform_data_add_col(df)
    # transformations complete, time to stage the data for ingest
    df = stage_data_for_ingest.stage_data_for_ingest(df, title, parent_dir)
    ic(df.head())
    ic(df.tail())

    # ingest the data into the database
    ingest_data_postgres.ingest_data_postgres(df, title)
    logger.info("Pipeline completed.")
    


set_input_output_variables()
