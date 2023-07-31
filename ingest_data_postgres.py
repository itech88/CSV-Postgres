import logging
from sqlalchemy import create_engine, exc
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ingest_data_postgres(df, table_name):
    # remember to replace with .txt file
    username = "postgres"
    password = "your_password"
    database = "Insurance_2022"

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
