import os
import psycopg2
from psycopg2 import sql

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="postgres",
        port=5432,
    )
    return conn

# get_db_connection()