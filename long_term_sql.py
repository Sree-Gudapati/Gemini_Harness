import mysql.connector


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
            password="135388",
            database="harness_db"
        )
        mycursor = self.conn.cursor()
        print("Table Connected")
        return mycursor

    def create_table(self, cursor):
        try:
            cursor.execute("CREATE TABLE chats (created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, role VARCHAR(20) NOT NULL, content LONGTEXT NOT NULL)")
            self.conn.commit()
            print("Table created")
        except:
            print("Table already created")

    def delete_table(self, cursor, table_name):
        cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()

    def create_entry(self, role, content, cursor):
        values = (role, content)
        cursor.execute("INSERT INTO chats (role, content) VALUES (%s, %s)", values)
        self.conn.commit()

    def purge_table(self, cursor):
        cursor.execute("DELETE FROM chats")

    def show_all(self, cursor):
        cursor.execute("SELECT created_at, role, content FROM chats")
        for timestamp, role, content in cursor:
            formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{formatted_time}] {role}: {content}")

    def close_connection(self, cursor):
        cursor.close()
        self.conn.close()
