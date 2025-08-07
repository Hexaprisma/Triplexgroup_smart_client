from datetime import datetime, timedelta

from sympy import re
from .config import SERVICES, WEEKDAYS, WEEKENDS, OPEN_TIME, CLOSE_TIME, LOCAL_STORES, TOOLS
import sqlite3


class database_handler:

    def __init__(self, db_path = '/home/edows/Documents/smart_client_prj/Triplexgroup_smart_client/data/company_info.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        #self.create_table()

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

    # tracking number is a unique identifier for an order
    # tracking number is a nine digit number: 565673567
    def is_valid_tracking_number(self, tracking_number):
        """Check if the tracking number is valid."""
        #normalize the tracking number to all digits
        tracking_number = re.sub(r'\D', '', tracking_number)
        #check if the tracking number is nine digits long
        if len(tracking_number) == 9 and tracking_number.isdigit():
            return True
        return False

    def _find_order(self, tracking_number):
        """Find an order by tracking number."""
        if(self.is_valid_tracking_number(tracking_number) == False):
            return 1
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE tracking_number=?", (tracking_number,))
        order = cursor.fetchone()
        if order:
            return {"tracking_number": order[0], "status": order[1], "details": order[2]}
        else:
            return 2

    def get_database_info(self):
        """Return a list of dicts containing the table name and column for each table in the database."""
        table_dicts = []
        for table_name in self.get_table_names():
            columns_names = self.get_column_names(table_name)
            table_dicts.append({"table_name": table_name, "columns": columns_names})
        return table_dicts

    def get_table_names(self):
        """Return a list of table names."""
        table_names = []
        #conn.execute is used to execute an SQL statement. It returns a cursor object 
        #that allows you to interate over the results of a query. 
        tables = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in tables.fetchall():
            table_names.append(table[0])
            print(table[0])
        return table_names

    def get_column_names(self, table_name):
        """Return a list of column names."""
        column_names = []
        columns = self.conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
        for col in columns:
            column_names.append(col[1])
        return column_names

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

    def is_valid_service(self, service):
        """Check if a service exists in the database."""
        return service in SERVICES
    

    
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
