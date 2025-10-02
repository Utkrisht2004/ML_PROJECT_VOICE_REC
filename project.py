import os
import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Load Vosk English model (make sure you downloaded and extracted it to "model/")
model = Model("C:/PROGRAMMING2/ML CLASS/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

# Queue for audio input
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Command mapping
def execute_command(text):
    if "chrome" in text:
        print("Opening Chrome...")
        os.system("start chrome")  # Windows
    elif "notepad" in text:
        print("Opening Notepad...")
        os.system("notepad")
    elif "calculator" in text:
        print("Opening Calculator...")
        os.system("calc")
    elif "exit" in text:
        print("Exiting program...")
        sys.exit(0)
    else:
        print("Command not recognized:", text)

# Start listening
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Listening for English commands... (say 'exit' to quit)")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower()
            if text:
                print("Recognized:", text)
                execute_command(text)
