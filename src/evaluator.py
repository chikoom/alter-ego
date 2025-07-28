import os
from pydantic import BaseModel
from openai import OpenAI
from config import Config

# Create a Pydantic model for the Evaluation
class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

class Evaluator:
    """Evaluator class to assess the quality of AI responses"""
    
    def __init__(self):
        self.name = Config.get_person_name()
        self._load_context()
        self._setup_gemini()
    
    def _load_context(self):
        """Load the context information for evaluation"""
        from pypdf import PdfReader
        
        # Load LinkedIn profile
        reader = PdfReader(Config.get_linkedin_profile_path())
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        
        # Load summary
        with open(Config.get_summary_path(), "r", encoding="utf-8") as f:
            self.summary = f.read()

        # Load resume
        reader = PdfReader(Config.get_resume_path())
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

    
    def _setup_gemini(self):
        """Setup Gemini API client"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.gemini = None
        else:
            self.gemini = OpenAI(
                api_key=api_key, 
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
    
    def evaluator_system_prompt(self):
        """Generate the evaluator system prompt"""
        system_prompt = f"""You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {self.name} and is representing {self.name} on their website. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
The Agent has been provided with context on {self.name} in the form of their summary, resume and LinkedIn details. Here's the information:"""

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"""CRITICAL EVALUATION CRITERIA:
1. REJECT if the response is in pig latin or any other non-English language
2. REJECT if the response is unprofessional or inappropriate for a business context
3. REJECT if the response doesn't answer the question properly
4. REJECT if the response is too short or lacks detail
5. ACCEPT only if the response is professional, clear, and appropriate

IMPORTANT: If you see words like "ay", "way", "ayway" at the end of words, or if the response looks like gibberish, it's likely pig latin and should be REJECTED.

Respond with either "ACCEPTABLE" or "UNACCEPTABLE" followed by your reasoning."""
        return system_prompt
    
    def evaluator_user_prompt(self, reply, message, history):
        """Generate the evaluator user prompt"""
        # Convert history to readable format
        formatted_history = []
        for msg in history:
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                formatted_history.append(f"{msg['role'].title()}: {msg['content']}")
            elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                # Handle Gradio chat format [user_msg, bot_msg]
                formatted_history.append(f"User: {msg[0]}")
                if msg[1] is not None:
                    formatted_history.append(f"Assistant: {msg[1]}")
        
        history_text = "\n".join(formatted_history) if formatted_history else "No previous conversation"
        
        user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history_text}\n\n"
        user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
        user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
        return user_prompt
    
    def evaluate(self, reply, message, history) -> Evaluation:
        """Evaluate a response using Gemini API"""
        print(f"Evaluator called with reply: {reply}")
        print(f"Evaluator called with message: {message}")
        
        # Check if Gemini client is available
        if self.gemini is None:
            print("ERROR: Gemini client not available - missing API key")
            # Return a default evaluation that rejects pig latin
            response_lower = reply.lower()
            if any(word in response_lower for word in ['way', 'ay', 'ayway']):
                print("Detected pig latin - rejecting")
                return Evaluation(
                    is_acceptable=False,
                    feedback="Response rejected: Pig latin detected"
                )
            else:
                print("No pig latin detected - accepting")
                return Evaluation(
                    is_acceptable=True,
                    feedback="Response accepted: No pig latin detected"
                )
        
        # Create a simple user prompt without complex history formatting
        user_prompt = f"""Please evaluate this response:

User Question: {message}
Agent Response: {reply}

Please respond with either "ACCEPTABLE" or "UNACCEPTABLE" followed by your reasoning."""
        
        print(f"User prompt: {user_prompt}")
        
        messages = [
            {"role": "system", "content": self.evaluator_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]
        
        print(f"About to call Gemini API...")
        response = self.gemini.chat.completions.create(
            model="gemini-2.0-flash", 
            messages=messages
        )
        
        # Parse the response manually
        response_text = response.choices[0].message.content
        
        # Simple parsing logic - look for keywords
        response_lower = response_text.lower()
        
        # Check if response indicates acceptance
        if 'unacceptable' in response_lower:
            is_acceptable = False
        elif 'acceptable' in response_lower:
            is_acceptable = True
        else:
            # Default to False for unclear responses
            is_acceptable = False
        
        # Debug: Print the evaluator response for debugging
        print(f"Evaluator response: {response_text}")
        print(f"Is acceptable: {is_acceptable}")
        
        return Evaluation(
            is_acceptable=is_acceptable,
            feedback=response_text
        )

# Example usage function
def example_evaluation():
    """Example of how to use the evaluator"""
    from personality import Personality
    
    # Initialize personality and evaluator
    personality = Personality()
    evaluator = Evaluator()
    
    # Example conversation
    messages = [
        {"role": "system", "content": personality.system_prompt()}
    ] + [
        {"role": "user", "content": "do you hold a patent?"}
    ]
    
    # Get response from personality
    response = openai.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages
    )
    reply = response.choices[0].message.content
    
    # Evaluate the response
    evaluation = evaluator.evaluate(reply, "do you hold a patent?", [])
    
    print(f"Response: {reply}")
    print(f"Acceptable: {evaluation.is_acceptable}")
    print(f"Feedback: {evaluation.feedback}")
    
    return evaluation 