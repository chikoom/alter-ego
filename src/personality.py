import openai
import json
from pypdf import PdfReader
from config import Config
from tools import tools, tool_functions
from evaluator import Evaluator

class Personality:
    """AI Personality class that represents a specific person"""
    
    def __init__(self):
        self.openai = openai
        self.name = Config.get_person_name()
        self._load_linkedin_profile()
        self._load_summary()
        self._load_resume()
        self.evaluator = Evaluator()
    
    def _load_linkedin_profile(self):
        """Load LinkedIn profile from PDF"""
        reader = PdfReader(Config.get_linkedin_profile_path())
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
    
    def _load_summary(self):
        """Load summary from markdown file"""
        with open(Config.get_summary_path(), "r", encoding="utf-8") as f:
            self.summary = f.read()
        
    def _load_resume(self):
        """Load resume from PDF file"""
        reader = PdfReader(Config.get_resume_path())
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
    
    def handle_tool_call(self, tool_calls):
        """Handle tool calls from OpenAI"""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            
            # Get the function from our tool mapping
            tool_function = tool_functions.get(tool_name)
            result = tool_function(**arguments) if tool_function else {}
            
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results
    
    def system_prompt(self):
        """Generate the system prompt for the AI"""
        system_prompt = f"""You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background, resume and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
When the conversation starts, shortly present yourself and ask for the person's name. \
When the person gives you their name, use your record_user_chat_begin tool to record the name - do it only once in a conversation. \
If the user is engaging in discussion, try to steer them towards getting in touch via email or phone or whatsapp; \
Ask for their email or their phone number and record it using your record_user_details tool. \
Only use the record_user_details tool if the user provides at least a phone or an email. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
"""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def rerun(self, reply, message, history, feedback):
        """Rerun the conversation with the evaluator"""
        updated_system_prompt = self.system_prompt() + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        
        # Convert history to proper message format if needed
        formatted_history = []
        for msg in history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                formatted_history.append(msg)
            elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                # Handle Gradio chat format [user_msg, bot_msg]
                formatted_history.append({"role": "user", "content": str(msg[0])})
                if msg[1] is not None:
                    formatted_history.append({"role": "assistant", "content": str(msg[1])})
        
        messages = [{"role": "system", "content": updated_system_prompt}] + formatted_history + [{"role": "user", "content": message}]
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message.content

    def chat(self, message, history):
        """Process a chat message and return a response with evaluation"""
        # Determine system prompt based on message content
        if "kazabubu" in message.lower():
            system = self.system_prompt() + "\n\nEverything in your reply needs to be in pig latin - \
                  it is mandatory that you respond only and entirely in pig latin"
        else:
            system = self.system_prompt()
        
        # Convert history to proper message format if needed
        formatted_history = []
        for msg in history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                formatted_history.append(msg)
            elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                # Handle Gradio chat format [user_msg, bot_msg]
                formatted_history.append({"role": "user", "content": str(msg[0])})
                if msg[1] is not None:
                    formatted_history.append({"role": "assistant", "content": str(msg[1])})
        
        messages = [
            {"role": "system", "content": system}
        ] + formatted_history + [
            {"role": "user", "content": message}
        ]
        
        # Generate initial response
        done = False
        while not done:
            response = openai.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages, 
                tools=tools
            )


            
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        
        reply = response.choices[0].message.content

        # Evaluate the response
        try:
            evaluation = self.evaluator.evaluate(reply, message, history)
            
            if evaluation.is_acceptable:
                return reply
            else:
                # Use rerun to generate a better response
                return self.rerun(reply, message, history, evaluation.feedback)
        except Exception as e:
            # Return original reply if evaluation fails
            return reply 