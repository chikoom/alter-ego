import openai
import json
from pypdf import PdfReader
from config import Config
from tools import tools, tool_functions

class Personality:
    """AI Personality class that represents a specific person"""
    
    def __init__(self):
        self.openai = openai
        self.name = Config.get_person_name()
        self._load_linkedin_profile()
        self._load_summary()
        self._load_resume()
    
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
    
    def chat(self, message, history):
        """Process a chat message and return a response"""
        messages = [
            {"role": "system", "content": self.system_prompt()}
        ] + history + [
            {"role": "user", "content": message}
        ]
        
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
        
        return response.choices[0].message.content 