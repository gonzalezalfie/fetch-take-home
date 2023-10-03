# This script has the goal of uploadig the masked data to postgres.

# Set the working directory.

import sys

working_directory = sys.argv[1]

# Import the necessary modules and functions.

import pandas as pd

import psycopg2
from sqlalchemy import create_engine

# Create a connection to the PostgreSQL server.
# I know that it's an extremely bad practice to put the explicit 
# credentials in the code, but since this task uses sample data 
# from public docker images, I guess it's fine.

conn = psycopg2.connect(
    host = "localhost", 
    database = "postgres", 
    user = "postgres", 
    password = "postgres"
)

# Read the masked_data.csv file, which contains the masked data.

masked_data_file_name = working_directory + "/masked_data.csv"

df_masked = pd.read_csv(masked_data_file_name)

# Add the message data to postgres.

# Again, it's not ideal to show the explicit credentials.

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")

with engine.connect() as conn:
    
    df_masked.to_sql(name = "user_logins", 
              con = engine, 
              if_exists = "append", 
              index = False)

# Close the connection.

conn.close()

# And that's it. The data is now in the server.
# You can go to the postgres terminal and run 
# select * from user_logins;
# to see that the table has now the data.

