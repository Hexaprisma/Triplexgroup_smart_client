import requests
import database_handler
import sqlite3
import re
import json

#now replaced with the calendar manager method
#conn = sqlite3.connect("data/shopData/TestingData.db")
database_manager = database_handler.database_handler()
conn = database_manager.conn
print("Opened database successfully")

starting_prompt = """
You are a expert customer service agent from Triple X Group, acting as an assistant.
Do not say anything unknown, do not guess any value, customer name, phone number and date of birth.
Start by a friendly greeting, and ask for specific service the customer need.
You can either respond directly, or suggest calling function depending on the customer's need.

Use this format ONLY if needed:
FunctionCall: {"name": "read_database", "args": {"query": "<query>"}}

Examples:

User: What's your company?
FunctionCall: {"name": "comapny_info", "args": {"query": "company information"}}

User: What is the status of order 12345?
FunctionCall: {"name": "check_order", "args": {"query": "status of order 12345"}}

User: How many users signed up last week?
AI: Due to privacy concerns, I can't provide that information.

User: Hello!
AI: Hello! How can I help you today?

"""


payload = {
    "model": "deepseek-r1:32b",  # Change this to your installed model
    "messages": [
        {"role": "system", "content": starting_prompt},
    ],
    "stream": False  # Set True for token-by-token streaming
}
response = requests.post("http://localhost:11434/api/chat", json=payload)
raw_output = response.json()["message"]["content"]
# Clean the output by removing <think> tags and their content
cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
print("Deepseek: ", cleaned_output)


def company_info(query):
    print("Retrieving company info...")

def check_order(query):
    print("Checking order status...")

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
    payload = {
    "model": "deepseek-r1:32b",  # Change this to your installed model
    "messages": [
        {"role": "user", "content": message},
    ],
    "stream": False  # Set True for token-by-token streaming
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    return response

while True:
    user_input = input("Enter something (or 'exit' to quit): ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the program.")
        break
    else:
        response = add_message_to_ai(user_input)
        if response:
            raw_output = response.json()["message"]["content"]
            cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
            print("Deepseek :", cleaned_output)
        else:
            print("Failed to get a response from the AI.")



