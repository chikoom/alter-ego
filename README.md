---
title: Alter_Ego
app_file: ./src/app.py
sdk: gradio
sdk_version: 5.33.1
---
# Alter Ego – AI Personality Chat

A modular, Python-based Gradio app that lets you chat with an AI persona powered by OpenAI, using your own career data, resume, and LinkedIn profile. Designed for personal branding, interactive resumes, or as a smart chatbot for your website.

---

## Features

- **Conversational AI**: Powered by OpenAI’s GPT models.
- **Personalized Knowledge**: Answers are based on your own resume, LinkedIn, and summary files.
- **Push Notifications**: Get notified when users leave their details or ask unknown questions.
- **Gradio Interface**: Clean, interactive web UI.
- **Modular Codebase**: Easy to extend and maintain.

---

## Folder Structure

```
Alter Ego/
│
├── src/
│   ├── app.py                # Main Gradio app entry point
│   ├── config.py             # Configuration and environment variables
│   ├── notifications.py      # Push notification logic
│   ├── personality.py        # AI persona logic
│   ├── tools.py              # Tool definitions for OpenAI function calling
│   ├── me/
│   │   ├── linkedin-profile.pdf
│   │   ├── personality-summary.md
│   │   └── idanbaron-resume-last-years.pdf
│   └── ...
│
├── requirements.txt          # All dependencies (for deployment)
├── README.md                 # This file
└── .gitignore                # Ignore venv, cache, etc.
```

---

## Setup & Usage

### 1. **Clone the Repo**
```sh
git clone <your-repo-url>
cd "Alter Ego"
```

### 2. **Create and Activate a Virtual Environment**
```sh
uv venv
source .venv/Scripts/activate  # On Windows (Git Bash)
```

### 3. **Install Dependencies**
```sh
uv pip install -r requirements.txt
```

### 4. **Run the App Locally**
```sh
python src/app.py
```
- The Gradio interface will open in your browser.

### 5. **Deploy to Gradio/Hugging Face Spaces**
```sh
gradio deploy src/app.py
```

---

## Configuration

- Place your resume, LinkedIn PDF, and summary markdown in `src/me/`.
- Set up your environment variables (e.g., for Pushover notifications) in a `.env` file or your system environment.

---

## Customization

- **Add new tools**: Edit `src/tools.py`.
- **Change persona logic**: Edit `src/personality.py`.
- **Change notification logic**: Edit `src/notifications.py`.

---

## Contributing

Pull requests and suggestions are welcome!  
Please open an issue to discuss your ideas or report bugs.

---

## License

MIT License