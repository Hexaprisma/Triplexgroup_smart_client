from datetime import datetime, timedelta
import sqlite3

class database_handler:
    def save_conversation_to_db(conversation):
        conn = sqlite3.connect('conversations.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                    (id INTEGER PRIMARY KEY, user_input TEXT, bot_response TEXT)''')
        c.execute("INSERT INTO conversations (user_input, bot_response) VALUES (?, ?)",
                (conversation['user_input'], conversation['bot_response']))
        conn.commit()
        conn.close()

    #def get_service_info():
