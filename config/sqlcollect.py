# This Python script connects to a PostgreSQL database and utilizes Pandas to obtain data and create a data frame
# A initialization and configuration file is used to protect the author's login credentials

import psycopg2
import pandas as pd

# Import the 'config' funtion from the config.py file
from .config import config



def getTable(sql_query):
    # Establish a connection to the database by creating a cursor object

    # Obtain the configuration parameters
    params = config()
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
    # Create a new cursor
    cur = conn.cursor()

    try:
        cur.execute(sql_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cur.close()
        return 1


    # Utilize the create_pandas_table function to create a Pandas data frame
    # Store the data as a variable
    # Will issue a warning, but it works 
    #quakes = pd.read_sql_query(sql_query, conn)
    tupples = cur.fetchall()

    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()

    column_names = ["datetime", "latitude", "longitude", "depth", "magnitude"]
    quakes = pd.DataFrame(tupples, columns=column_names)
    # Return quakes table
    return quakes
    
