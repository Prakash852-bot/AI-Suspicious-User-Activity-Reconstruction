
import sqlite3
import pandas as pd
from pathlib import Path

# Database location
DB_FOLDER = Path("database")
DB_FOLDER.mkdir(exist_ok=True)

DB_PATH = DB_FOLDER / "forensic_database.db"


def create_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create normalized events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS normalized_events (
            event_id INTEGER,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            object TEXT,
            source TEXT,
            source_reference TEXT
        )
    """)

    # Create timeline table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_timeline (
            event_id INTEGER,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            object TEXT,
            source TEXT,
            source_reference TEXT,
            time_difference TEXT
        )
    """)

    # Create suspicious findings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suspicious_findings (
            user TEXT,
            login_time TEXT,
            file_access_time TEXT,
            file_name TEXT,
            usb_connection_time TEXT,
            usb_device TEXT,
            time_window TEXT,
            finding TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


def save_dataframe(data, table_name):

    connection = sqlite3.connect(DB_PATH)

    data.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print(f"{table_name} saved successfully!")


def display_database_records():

    connection = sqlite3.connect(DB_PATH)

    tables = [
        "normalized_events",
        "activity_timeline",
        "suspicious_findings"
    ]

    for table in tables:

        print(f"\nDATABASE TABLE: {table}")

        data = pd.read_sql_query(
            f"SELECT * FROM {table}",
            connection
        )

        print(data.to_string(index=False))

    connection.close()
