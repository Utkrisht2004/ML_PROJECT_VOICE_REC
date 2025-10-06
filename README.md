# Voice Command Control (English)

This project allows you to control your laptop using **voice commands in English**.  
It uses the [Whisper](https://openai.com/index/whisper/) speech recognition library and Python.

---

## 🚀 Features
- Recognizes **English voice commands** via microphone.
- Executes simple system commands like:
  - "open chrome"
  - "open notepad"
  - "open calculator"
  - "exit"
- Runs **offline** (no internet required).
- Extendable to **Hindi (and other languages)** in future.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- [Vosk](https://alphacephei.com/vosk/) (offline speech recognition)
- [SoundDevice](https://python-sounddevice.readthedocs.io/) (microphone input)
- `os` (to run system commands)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/voice-control.git
   cd voice-control


## Virtual Environment Suggested
- python -m venv venv
- source venv/bin/activate      # Linux/Mac
- venv\Scripts\activate         # Windows

## Dependencies Installation
pip install -r requirements.txt

## Voice Model

- Go to: https://alphacephei.com/vosk/models
- Download vosk-model-en-us-0.22 (recommended for accuracy)

## Project Structure
```
voice-control/
│── project.py          # Main program
│── requirements.txt    # Python dependencies
│── .gitignore          # Ignore cache, venv, large models
│── README.md           # Project documentation
│── model/              # Downloaded Vosk model (ignored by git)
```

## Future Work

- Add multi-language support.
- Add voice automation for program development.
- Extend command set with NLP-based intent detection.
- Dockerize the app for portability.