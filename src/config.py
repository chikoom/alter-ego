from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

class Config:
    """Configuration class to manage environment variables and settings"""
    
    @staticmethod
    def get_pushover_token():
        """Get Pushover API token from environment"""
        return os.getenv("PUSHOVER_TOKEN")
    
    @staticmethod
    def get_pushover_user():
        """Get Pushover user key from environment"""
        return os.getenv("PUSHOVER_USER")
    
    @staticmethod
    def get_openai_api_key():
        """Get OpenAI API key from environment"""
        return os.getenv("OPENAI_API_KEY")
    
    @staticmethod
    def get_person_name():
        """Get the name of the person being represented"""
        return "Idan Baron"
    
    @staticmethod
    def get_linkedin_profile_path():
        """Get path to LinkedIn profile PDF"""
        return "./src/me/linkedin-profile.pdf"
    
    @staticmethod
    def get_summary_path():
        """Get path to summary file"""
        return "./src/me/personality-summary.md" 

    @staticmethod
    def get_resume_path():
        """Get path to resume file"""
        return "./src/me/idanbaron-resume-last-years.pdf" 