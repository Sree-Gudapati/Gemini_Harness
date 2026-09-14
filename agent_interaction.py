from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')



class ModelInteract():
    def __init__(self, long_term_memory=None):
        self.long_term_memory = long_term_memory if long_term_memory is not None else []
        self.memory = self.long_term_memory

    def interact_loop(self):
        client = genai.Client()
        chat = client.chats.create(model="gemini-3.1-flash-lite")
        memory = []

        try:
            while True:
                user_input = input("You: ")
    
                # Store user message
                memory.append({"role": "user", "content": user_input})
    
                # Send to model
                response = chat.send_message(user_input)
                assistant_response = response.text
    
                # Store model response
                memory.append({"role": "assistant", "content": assistant_response})
    
                print(f"Assistant: {assistant_response}")
    
        except KeyboardInterrupt:
            print("\n\nExiting...")
            self.long_term_memory = memory

    def get_all_mem(self):
        return self.long_term_memory

    def get_n_interactions(self, n):
        for k in self.long_term_memory:
            print(k)