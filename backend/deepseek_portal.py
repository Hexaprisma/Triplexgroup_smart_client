import requests
import database_handler
import sqlite3
import re

test_prompt = """Hello, please introduce yourself and tell me what you can do."""


starting_prompt = """
You are a expert customer service agent from Triple X Group, acting as an assistant.
Do not say anything unknown, do not guess any value, customer name, phone number and date of birth.
Start by a friendly greeting, and ask for specific service the customer need.
You can either respond directly, or suggest calling the read_database function.

Use this format ONLY if needed:
FunctionCall: {"name": "read_database", "args": {"query": "<query>"}}

Examples:

User: What's your company?
FunctionCall: {"name": "read_database", "args": {"query": "company information"}}

User: What is the status of order 12345?
FunctionCall: {"name": "read_database", "args": {"query": "status of order 12345"}}

User: How many users signed up last week?
AI: Due to privacy concerns, I can't provide that information.

User: Hello!
AI: Hello! How can I help you today?

"""
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "deepseek-r1:32b",
        "prompt": test_prompt,
        "stream": False,
    },
)

raw_output = response.json()["response"]
cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
print("Deepseek: ", cleaned_output)



response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "deepseek-r1:32b",
        "role": "system",
        "prompt": starting_prompt,
        "stream": False,
    },
)

raw_output = response.json()["message"]["content"]
# Clean the output by removing <think> tags and their content
#cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
print("Deepseek: ", raw_output)


def read_database(query):
    """Read conversations from the database."""
    try:
        conn = sqlite3.connect('conversations.db')
        c = conn.cursor()
        c.execute("SELECT * FROM conversations WHERE query=?", (query,))
        rows = c.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
        print("Database is ready.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def check_service_availability(service_name):
    """Check if a service is available."""
    try:
        response = requests.get(f"http://localhost:11434/api/services/{service_name}")
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"An error occurred while checking service availability: {e}")
        return False
    
def check_order_status(order_id):
    """Check the status of an order."""
    try:
        response = requests.get(f"http://localhost:11434/api/orders/{order_id}/status")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"An error occurred while checking order status: {e}")
        return None
    
def add_message_to_ai(message):
    """Add a message to the AI's conversation history."""
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "deepseek-r1:32b",
            "role": "user",
            "prompt": message,
            "stream": False,
        }
    )
    return response if response.status_code == 200 else None

while True:
    user_input = input("Enter something (or 'exit' to quit): ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the program.")
        break
    else:
        response = add_message_to_ai(user_input)
        if response:
            raw_output = response.json()["message"]["content"]
            #cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
            print("Deepseek :", response)
        else:
            print("Failed to get a response from the AI.")



