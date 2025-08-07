import requests
import sqlite3
import re
import database_handler
import json
from .config import TOOLS, INIT_MESSAGE

# Initialize database
database_manager = database_handler.database_handler()
conn = database_manager.conn
print("Opened database successfully")

tools = TOOLS.copy()

# Conversation initialization
# This will hold the conversation history
messages = INIT_MESSAGE.copy()

# ---- Functions ----
def company_info(query):
    print("Retrieving company info...")
    return_message = database_manager.get_database_info()


def check_order(tracking_number):
    print(f"Checking order status for: {tracking_number}")
    order_info = database_manager._find_order(tracking_number)
    if order_info:
        return_message = f"Order found: {order_info['details']}"
    else:
        return_message = "Order not found."
    return return_message


def add_system_message(message):
    """Add a message to the conversation history."""
    messages.append({"role": "assistant", "content": message})
    print(f"Assistant: {message}")
    payload = {
        "model": "deepseek-r1:32b",
        "messages": messages,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    return response

# Send message to Ollama
def ask_ai(message):
    global messages
    messages.append({"role": "user", "content": message})
    payload = {
        "model": "deepseek-r1:32b",
        "messages": messages,
        "tools": tools,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    tool_calls = response.get("message", {}).get("tool_calls", [])
    if tool_calls:
        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"].get("arguments", {})
            print(f"Function call detected: {name} with args {args}")

            if name == "get_current_weather":
                location = args.get("location", "")
                print(f"Fetching weather for {location}...")
                # Here you would call the actual weather API
                # For now, we just simulate a response
                weather_info = f"Current weather in {location} is sunny with a temperature of 25°C."
                messages.append({"role": "assistant", "content": weather_info})
            elif name == "company_info":
                result = company_info(args.get("query", ""))
            elif name == "check_order":
                tracking_number = args.get("tracking_number", "")
                result = check_order(args.get("query", ""))
                if (result == 1):
                    msg = "Invalid tracking number format, please provide a valid 9 digit tracking number."
                    messages.append({"role": "assistant", "content": msg})
                elif (result == 2):
                    msg = "Order not found, please check the tracking number."
                    messages.append({"role": "assistant", "content": msg})
                else:
                    msg = f"Order found: {result['details']}"
                    messages.append({"role": "assistant", "content": msg})
                
            else:
                print(f"Unknown function call: {call['name']}")

            
    else:
        messages.append({"role": "assistant", "content": response.json()["message"]["content"]})

    return response


def initial_response():
    print("Welcome to Triple X Group! How can I assist you today?")




initial_response()

while True:
    user_input = input("You: (enter 'exit' or 'quit' to quit) ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = ask_ai(user_input)
    if response.status_code == 200:
        raw_output = response.json()["message"]["content"]
        # Remove thinking tags
        cleaned_output = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
        
        # Detect function call
        match = re.search(r'FunctionCall:\s*(\{.*\})', cleaned_output)
        if match:
            try:
                func_data = json.loads(match.group(1))
                func_name = func_data.get("name")
                query = func_data.get("args", {}).get("query", "")
                
                if func_name == "company_info":
                    company_info(query)
                elif func_name == "check_order":
                    check_order(query)
                else:
                    print(f"Unknown function: {func_name}")
            except json.JSONDecodeError:
                print("Invalid function call format")
        else:
            print("Deepseek:", cleaned_output)
            messages.append({"role": "assistant", "content": cleaned_output})
    else:
        print("AI request failed:", response.text)
