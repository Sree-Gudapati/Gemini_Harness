import os

from dotenv import load_dotenv
from google import genai

import long_term_sql

load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')


class ModelInteract:
    def __init__(self, long_term_memory=None):
        self.long_term_memory = long_term_memory if long_term_memory is not None else []
        self.memory = self.long_term_memory

    def interact_loop(self):
        client = genai.Client()
        chat = client.chats.create(model="gemini-3.1-flash-lite")
        memory = []

        # connecting to db
        sql_table = long_term_sql.table()

        cursor = sql_table.connect()
        sql_table.create_table(cursor)

        try:
            while True:
                user_input = input("You: ")

                # Store user message
                sql_table.create_entry("user", user_input, cursor)

                # Send to model
                response = chat.send_message(user_input)
                assistant_response = response.text

                # Store model response
                sql_table.create_entry("model", assistant_response, cursor)

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
