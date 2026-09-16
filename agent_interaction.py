import os

from dotenv import load_dotenv
from google import genai
from google.genai import types 

import long_term_sql
import tool_calling

load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')


class ModelInteract:
    client = genai.Client()


    def __init__(self, long_term_memory=None):
        self.long_term_memory = long_term_memory if long_term_memory is not None else []
        self.memory = self.long_term_memory


    def interact_loop(self):
        # connecting to db
        sql_table = long_term_sql.table()
        cursor = sql_table.connect()

        tool_access = tool_calling.tools(cursor, sql_table)
        chat = self.client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                tools=tool_access.get_all_tools()
            )
        )
        memory = []

        sql_table.create_table(cursor, 'chat', columns = {
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "role": "VARCHAR(20) NOT NULL",
        "content": "LONGTEXT NOT NULL"
        })

        try:
            while True:
                user_input = input("You: ")

                # Store user message
                sql_table.create_entry("chat", {"role": "user", "content": user_input}, cursor)

                # Send to model
                response = chat.send_message(user_input)
                assistant_response = response.text

                sql_table.create_entry("chat", {"role": "assistant", "content": assistant_response}, cursor)
                print(f"Assistant: {assistant_response}")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            self.long_term_memory = memory

        sql_table.close_connection(cursor)


    def get_all_mem(self):
        return self.long_term_memory


    def get_n_interactions(self, n):
        for k in self.long_term_memory:
            print(k)

