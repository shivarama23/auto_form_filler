from db import get_db_connection

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the table creation queries
    table_creation_queries = {
        "chat_sessions": """
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255) NOT NULL UNIQUE,
                user_data JSONB NOT NULL,
                history JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        "another_table": """
            CREATE TABLE IF NOT EXISTS another_table (
                id SERIAL PRIMARY KEY,
                some_field VARCHAR(100) NOT NULL
            )
        """
    }

    # Loop through and create each table
    for table_name, query in table_creation_queries.items():
        print(f"Checking and initializing table: {table_name}")
        cursor.execute(query)

    conn.commit()
    print("Database initialized successfully.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    initialize_database()
