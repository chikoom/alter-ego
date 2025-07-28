import requests
from config import Config

class NotificationService:
    """Service for sending push notifications via Pushover"""
    
    @staticmethod
    def push(text):
        """Send a push notification with the given text"""
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": Config.get_pushover_token(),
                "user": Config.get_pushover_user(),
                "message": text,
            }
        )
    
    @staticmethod
    def record_user_details(email="[NA email]", phone="[NA phone]", name="[NA name]", notes="[NA notes]"):
        """Record user details and send notification"""
        message = f"AE - Contact details: {name} with email {email} and phone {phone} and notes {notes}"
        NotificationService.push(message)
        return {"recorded": "ok"}
    
    @staticmethod
    def record_unknown_question(question):
        """Record an unknown question and send notification"""
        message = f"AE - Unknown question: {question}"
        NotificationService.push(message)
        return {"recorded": "ok"} 
    
    @staticmethod
    def record_user_chat_begin(name):
        """Record a user chat beginning and send notification"""
        message = f"AE - A user ({name}) started speaking with you"
        NotificationService.push(message)
        return {"recorded": "ok"}
