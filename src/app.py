import gradio as gr
from personality import Personality

def main():
    """Main application entry point"""
    personality = Personality()
    gr.ChatInterface(personality.chat, type="messages").launch()

if __name__ == "__main__":
    main()
    