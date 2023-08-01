import logging
from sqlalchemy import create_engine, exc
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# create a method to open .txt files that contain username and password
un_file_name = "/Users/itech88/Documents/Secure/un.txt"
pw_file_name = "/Users/itech88/Documents/Secure/pw.txt"


def get_username_password(un_file_name, pw_file_name):
    # open the file containing the username
    un_file = open(un_file_name, "r")
    # read the username
    username = un_file.read()
    # close the file
    un_file.close()
    # open the file containing the password
    pw_file = open(pw_file_name, "r")
    # read the password
    password = pw_file.read()
    # close the file
    pw_file.close()
    # return the username and password
    return username, password


def ingest_data_postgres(df, table_name):
    # get the username and password
    username, password = get_username_password(un_file_name, pw_file_name)
    database = "historical_reports_2022"

    DATABASE_URI = (
        "postgresql+psycopg2://"
        + username
        + ":"
        + password
        + "@localhost:5432/"
        + database
    )

    engine = create_engine(DATABASE_URI)

    try:
        # Use the to_sql function to write data from your DataFrame into PostgreSQL
        logging.info("Attempting to write data to PostgreSQL table: %s", table_name)

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",  # If the table already exists, it will replace it.
            index=False,  # Not writing the DataFrame's index to the database
            method="multi",  # Insert data in chunks
        )

        logging.info("Successfully wrote data to PostgreSQL table: %s", table_name)

    except exc.SQLAlchemyError as e:
        logging.error("SQLAlchemy error occurred: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        # Always ensure the connection to the Postgres database is closed
        engine.dispose()
