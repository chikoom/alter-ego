from notifications import NotificationService

record_user_chat_begin_json = {
    "name": "record_user_chat_begin",
    "description": "Use this tool only once in a conversation, when the user first gives you their name",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
        },
        "required": ["name"],
        "additionalProperties": False
    }
}

# Tool definitions for OpenAI function calling
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address or a phone number",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "phone": {
                "type": "string",
                "description": "The phone number of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# List of available tools
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
    {"type": "function", "function": record_user_chat_begin_json}
]

# Tool function mapping
tool_functions = {
    "record_user_details": NotificationService.record_user_details,
    "record_unknown_question": NotificationService.record_unknown_question,
    "record_user_chat_begin": NotificationService.record_user_chat_begin
} 