import json

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday" ]
WEEKENDS = ["Saturday", "Sunday"]
OPEN_TIME = "08:00"
CLOSE_TIME = "20:00"

SERVICES = {
    "service1": {"name": "Auto glass replacement", "price": "100", "description": "Description of Service 1"},
    "service2": {"name": "Auto Glass Repair", "price": "200", "description": "Description of Service 2"},
    "service3": {"name": "Car Film/Wrap Application", "price": "300", "description": "Description of Service 3"},
}

LOCAL_STORES = {
    "store1": {"name": "Store 1", "location": "Cangshan District, Fuzhou, Fujian"},
    "store2": {"name": "Store 2", "location": "Jin'An, Fuzhou, Fujian"},
    "store3": {"name": "Store 3", "location": "189, Feifengshan Aoti Park, Cangshan District, Fuzhou, Fujian, China, 350028"},
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name to get weather for"}
                },
                "required": ["location"]
            }
        }
    }
]

INIT_MESSAGE = [
    {
        "role": "system",
        "content": """
You are an expert customer service agent from Triple X Group, acting as an assistant.
Do not guess customer info or private data.
        You can answer questions about the company, services, and orders.
        If you don't know the answer, say "I don't know" or "I cannot provide that information."
        If a function call is detected, execute it with the provided query.
        Do not provide any personal data or sensitive information.
        
        Here are the available functions:
        
        - company_info(query): Retrieve information about the company.
        - check_order(query): Check the status of an order based on the provided query.
        
If you need to fetch data, return ONLY in this format:

FunctionCall: {"name": "<function_name>", "args": {"query": "<query>"}}

Examples:
User: Tell me about the company.
Assistant: FunctionCall: {"name": "company_info", "args": {"query": "<query>"}}

User: What is the status of my order?
Assistant: FunctionCall: {"name": "check_order", "args": {"query": "<query>"}}

User: How many users signed up last week?
AI: Due to privacy, I cannot provide user data.

Huser: Hello!
AI: Hello! How can I help you today?
"""
    }
]