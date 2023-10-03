import pandas as pd
import os
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

@timer
def stage_data_for_ingest(df, report_title, parent_dir):
    # specify the parent directory where the files will be stored
    # this will need to be changed to wherever the staged files will live
    ic(os.getcwd())
    # read the path inside parent_dir.txt
    with open(parent_dir, "r") as file:
        read_parent_dir = (
            file.readline().strip()
        )  # assume the path is on the first line

        # log and print current working directory and read_parent_dir for debugging
        current_working_dir = os.getcwd()
        ic(current_working_dir)
        ic(read_parent_dir)
        logger.info(f'Read parent directory: {read_parent_dir}')
        # resolve to absolute path
        absolute_parent_dir = os.path.join(current_working_dir, read_parent_dir)
        ic(absolute_parent_dir)
        logger.info(f'Resolved absolute parent directory: {absolute_parent_dir}')
        

    clean_directory = read_parent_dir + "/Clean_Layer"
    ic(clean_directory)
    logger.info(f'Clean directory path: {clean_directory}')
    # create the directory if it doesn't exist
    if not os.path.exists(clean_directory):
        os.makedirs(clean_directory)
        logger.info("Clean directory created.")

    # specify the input and output file names
    output_filename = report_title + "-Processed.csv"
    ic(output_filename)
    logger.info(f'Output filename: {output_filename}')

    # write the processed data to a new CSV file in the parent directory
    df.to_csv(os.path.join(clean_directory, output_filename), index=False)
    logger.info("Processed data written to CSV file.")
    return df
