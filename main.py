import os
import sys

import agent_interaction
import long_term_sql



def main(): 

    # long term chat storage
    memory = [] 
    sql = long_term_sql.table()
    cursor = sql.connect() 
    sql.create_table(cursor)





    interaction = agent_interaction.ModelInteract(memory)

    interaction.interact_loop()

    session_chat = interaction.get_all_mem()

    sql.create_entry(session_chat, cursor)

    sql.show_all(cursor)

    sql.close_connection(cursor) 
if __name__ == "__main__":
    main()
