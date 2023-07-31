import pandas as pd
import os


def stage_data_for_ingest(df, report_title, parent_dir):
    # specify the parent directory where the files will be stored
    # this will need to be changed to wherever the staged files will live
    print(os.getcwd())
    clean_directory = parent_dir + "/Clean_Layer"
    # create the directory if it doesn't exist
    if not os.path.exists(clean_directory):
        os.makedirs(clean_directory)

    # specify the input and output file names
    output_filename = report_title + "-Processed.csv"

    # write the processed data to a new CSV file in the parent directory
    df.to_csv(os.path.join(clean_directory, output_filename), index=False)

    return df
