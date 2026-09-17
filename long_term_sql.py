import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class table:
    def __init__(self):
        self.conn = None


    @property
    def get_conn(self):
        return self.conn


    def connect(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="harness_user",
            password=os.getenv('DB_PASSWORD'),
            database="harness_db"
        )
        mycursor = self.conn.cursor()
        print("Table Connected")
        return mycursor


    def create_table(self, cursor, table_name: str, columns: dict):
        try:
            column_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])

            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
            cursor.execute(query)
            self.conn.commit()
            print(f"Table '{table_name}' created")
        except Exception as e:
            print(f"Error: {e}")


    def delete_table(self, cursor, table_name):
        cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()


    def create_entry(self, table_name: str, data: dict, cursor):
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())
        
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Entry added to {table_name}")
        except Exception as e:
            print(f"Error inserting entry: {e}")


    def purge_table(self, cursor):
        cursor.execute("DELETE FROM chats")


    def close_connection(self, cursor):
        cursor.close()
        self.conn.close()


    def specific_query(self, cursor, column, value, table):
        # Use %s placeholder for values
        query = f"SELECT `{column}` FROM `{table}` WHERE `{column}` = %s"
        cursor.execute(query, (value,))
        return cursor.fetchall()  # Returns list of matching rows (empty list if none)
