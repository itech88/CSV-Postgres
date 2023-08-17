import logging
from sqlalchemy import create_engine, exc
import pandas as pd
import os
from timer_decorator import timer
from logging_config import configure_logging
logger = configure_logging(__name__)

# from config import un_file_name, pw_file_name, database_file_name
from dotenv import load_dotenv, find_dotenv


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

@timer
def get_username_password():
    # env_path = os.path.join(".", ".env")
    load_dotenv(find_dotenv())
    # load_dotenv(env_path)
    # open the file containing the username
    # un_file = open(un_file_name, "r")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    database = os.getenv("DB")

    # return the username, password and database name
    return username, password, database

@timer
def ingest_data_postgres(df, table_name):
    # get the username and password
    username, password, database = get_username_password()

    DATABASE_URI = (
        "postgresql+psycopg2://"
        + username
        + ":"
        + password
        + "@localhost:5432/"
        + database
    )

    engine = create_engine(DATABASE_URI)
    logger.info("Successfully CONNected to PostgreSQL database: %s", database)

    try:
        # Use the to_sql function to write data from your DataFrame into PostgreSQL
        logging.info("Attempting to write data to PostgreSQL table: %s", table_name)
        # change the name of the dataframe and do column transformation
        df.to_sql(
            table_name,
            engine,
            if_exists="append",  # If the table already exists, it will replace it.
            index=False,  # Not writing the DataFrame's index to the database
            method="multi",  # Insert data in chunks
        )

        logging.info("Successfully Wrote data to PostgreSQL table: %s", table_name)

    except exc.SQLAlchemyError as e:
        logging.error("SQLAlchemy error occurred: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        # Always ensure the connection to the Postgres database is closed
        engine.dispose()
