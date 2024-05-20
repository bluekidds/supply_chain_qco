import pandas as pd
import sqlite3
import streamlit as st

def create_table(dbname='wbs.db'):
    with sqlite3.connect(dbname) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WBS_Elements (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            level INTEGER,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES WBS_Elements(id)
        )
        ''')
        conn.commit()  # Ensure changes are committed
        print("Table WBS_Elements created or verified successfully.")


def insert_data(dataframe, dbname='wbs.db'):
    try:
        with sqlite3.connect(dbname) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM WBS_Elements')  # Clear the table before inserting new data
            for _, row in dataframe.iterrows():
                cursor.execute('''
                INSERT INTO WBS_Elements (id, name, description, level, parent_id)
                VALUES (?, ?, ?, ?, ?)
                ''', (row['ID'], row['Name'], row['Description'], row['Level'], row['Parent ID']))
            conn.commit()  # Commit after insertion
            print("Data inserted successfully into the database.")
    except Exception as e:
        print(f"Error during database operation: {e}")
        raise
def read_excel_and_populate_db(filepath, dbname='wbs.db'):
    xls = pd.ExcelFile(filepath)
    for sheet_name in xls.sheet_names:
        st.write(sheet_name)
        df = pd.read_excel(xls, sheet_name=sheet_name)
        st.write(df.head(2))
        print(f"Processing {sheet_name} with columns: {df.columns}")
        insert_data(df, dbname)
    print("Database populated successfully.")

def print_schema(dbname='wbs.db'):
    with sqlite3.connect(dbname) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='WBS_Elements'")
        schema = cursor.fetchone()
        print("Schema of WBS_Elements table:")
        print(schema[0] if schema else "No schema found.")

def print_table_contents(dbname='wbs.db'):
    with sqlite3.connect(dbname) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WBS_Elements")
        rows = cursor.fetchall()
        print("Contents of WBS_Elements table:")
        for row in rows:
            print(row)
