from datetime import datetime, timedelta
import sqlite3

class database_handler:

    def __init__(self, db_path = 'data/company_info.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def _load_service_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        price TEXT, 
        discription TEXT,
        )
        ''')
        self.conn.commit()

    def _find_order(self, case_id):
        """Find an order by case ID."""

    def get_database_info(self):
        """Return a list of dicts containing the table name and column for each table in the database."""
        table_dicts = []
        for table_name in slef.get_table_names():
            columns_names = self.get_column_names(table_name)
            table_dicts.append({"table_name": table_name, "columns": columns_names})
        return table_dicts

    def ask_database(self, query):
        """Execute a query on the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

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

    def close(self):
        """Close the database connection."""
        self.conn.close()
