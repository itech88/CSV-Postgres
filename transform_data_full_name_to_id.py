import pandas as pd
import transform_data_add_person_id_column
from datetime import datetime
from timer_decorator import timer
from logging_config import configure_logging

logger = configure_logging(__name__)

@timer
def transform_data_full_name_to_id(df):
    
    # List of column names to process.
    name_columns = ['provider', 'providers', 'patient', 'patients']
    
    # Mapping column names to respective person types to avoid repetitive string checks.
    col_to_person_type = {
        'provider': 'provider',
        'providers': 'provider',
        'patient': 'patient',
        'patients': 'patient'
    }
    
    # Select the intersecting columns that are present in the DataFrame.
    cols_to_process = df.columns.intersection(name_columns)
    detected_types = set()  # To keep track of all person types detected in the dataframe.

    for col in cols_to_process:
        col_lower = col.lower()  # Convert column name to lowercase for standard comparison.
        
        # Identify person type for the given column.
        person_type = col_to_person_type.get(col_lower)
        if person_type:
            detected_types.add(person_type)
            logger.info(f'Column: {col} is person type: {person_type}')
        else:
            logger.warning(f'Column was in named_columns list, but was not identified: {col}')

    # Split the columns and create new ones for first name and last name.
    df[['last_name', 'first_name']] = df[cols_to_process].stack().str.split(', ', expand=True).reset_index(level=1, drop=True)
    
    # Drop the original columns after processing.
    if cols_to_process.any():
        df.drop(cols_to_process, axis=1, inplace=True)
        logger.info(f'Columns dropped: {cols_to_process}')
    else:
        logger.info(f'No columns dropped, columns did not match in {name_columns}')
    
    # Handling scenario where dataframe has both 'provider' and 'patient' type columns.
    if len(detected_types) > 1:
        logger.warning("Multiple person types detected. Handling needs to be defined!")
        return df

    # Prepare data for further transformation based on the person type detected.
    person_type = next(iter(detected_types), None)
    if person_type:
        # Transform person type to create a new employee ID column.
        transform_data_add_person_id_column.transform_data_add_person_id_column(df, person_type)
    else:
        logger.warning("No valid person type detected for ID transformation.")
    
    return df
