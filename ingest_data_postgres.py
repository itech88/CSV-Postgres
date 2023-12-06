import logging
from sqlalchemy import create_engine, exc, text
import pandas as pd
import os
from timer_decorator import timer
from logging_config import configure_logging
from config import db_save_type
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
    server = os.getenv("SERVER")
    port = os.getenv("PORT")

    # return the username, password and database name
    return username, password, database, server, port

@timer
def ingest_data_postgres(df, table_name):
    '''
    Start the PostgreSQL container (and ensure it's attached to the network).
    Run your Python pipeline inside its container, making sure it's also attached to the 
    same network. Your pipeline should process the data, and once it reaches the 
    ingest_data_postgres function, it will ingest the data into the PostgreSQL container.
    '''
    # get the username and password
    username, password, database, server, port = get_username_password()
    with open(db_save_type, "r") as file:
        table_mod = file.readline().strip()  # assuming the column name is on the first line
        logger.info(f"Database table instruction: {table_mod}")

    '''
    Ensure that the .env file with the environment variables USERNAME, PASSWORD, and DB 
    is accessible within your Python pipeline container. If you're using Docker, this file 
    should be in a directory that's mounted as a volume inside the container, or you should 
    be copying it into the Docker image during the build process.
    Ensure the database URI in your Python code is pointing to the PostgreSQL container's name.
    Both the Python application and PostgreSQL should be on the same Docker network 
    to communicate. Double-check environment variables and file paths in the containerized setup,
    as they can differ from the local setup.
    '''
    DATABASE_URI = (
    
    "postgresql+psycopg2://"
    + username
    + ":"
    + password
    + f'@{server}:{port}/'
    + database
    )

    # Create a SQLAlchemy engine
    engine = create_engine(DATABASE_URI) # optional for engine logging, use echo=True


    try:
        '''the following is for transaction management testing
        # Use the to_sql function to write data from your DataFrame into PostgreSQL
        logging.info("Attempting to write data to PostgreSQL table: %s", table_name)
        logging.info(f'DataFrame head: \n{df.head()}')

        # attempt transation management explicitly
        connection = engine.connect()
        #df1 = pd.read_sql('Select * from q1_q2_misc_services', connection)
        #logging.info(df1.head())
        
        transaction = connection.begin()
        try:
            df.to_sql(table_name, connection, if_exists='append', index=False, method="multi")
            transaction.commit()
            #df2 = pd.read_sql('Select * from q1_q2_misc_services', connection)
            #logging.info(df2.head())
        
            #connection.commit()
            #df3 = pd.read_sql('Select * from q1_q2_misc_services', connection)
            #logging.info(df3.head())
        
        except Exception as e:
            transaction.rollback()
            logging.error(f"Error occurred: {e}")
        finally:
            connection.close()
        '''

        # change the name of the dataframe and do column transformation
        df.to_sql(
            table_name,
            engine,
            if_exists= 'append', # table_mod,  # If the table already exists, read the instruction to how to mod table
            index=False,  # Not writing the DataFrame's index to the database
            method="multi",  # Insert data in chunks
        )

        logging.info("SUCCESS!!!! Wrote data to PostgreSQL table: %s", table_name)
        logging.info(f'Database URI {DATABASE_URI}')

    except exc.SQLAlchemyError as e:
        logging.error("SQLAlchemy error occurred: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        # Always ensure the connection to the Postgres database is closed
        engine.dispose()
