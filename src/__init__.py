# Alter Ego - AI Personality Chat Application
# This package contains the modular components for the AI personality chat system

from .config import Config
from .notifications import NotificationService
from .tools import tools, tool_functions
from .personality import Personality

__version__ = "1.0.0"
__author__ = "Idan"

__all__ = [
    "Config",
    "NotificationService", 
    "tools",
    "tool_functions",
    "Personality"
] 