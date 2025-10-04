import os
import queue
import sounddevice as sd
import numpy as np
import whisper
import torch

# ✅ Auto-select device (GPU if available)
# Using torch.cuda.is_available() is the standard and recommended way.
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ✅ 1. USE A SMALLER, FASTER MODEL
# "base" is a great balance of speed and accuracy for command recognition.
# For even more speed, you could use "tiny".
model = whisper.load_model("base", device=device)
print("Model loaded successfully!")

# Recording parameters
SAMPLE_RATE = 16000 # Whisper's required sample rate
DURATION = 4      # seconds of audio to capture per chunk
BLOCK_SIZE = 1024 # How many frames per buffer
q = queue.Queue()

def callback(indata, frames, time, status):
    """Audio callback—captures mic input and puts it into a queue."""
    if status:
        print(status)
    q.put(indata.copy())

def execute_command(text):
    """Simple command mapping"""
    if "browser" in text:
        print("✅ Opening Chrome...")
        os.system("start chrome")
    elif "notepad" in text:
        print("✅ Opening Notepad...")
        os.system("notepad")
    elif "calculator" in text:
        print("✅ Opening Calculator...")
        os.system("calc")
    elif "exit" in text or "quit" in text:
        print("Exiting program...")
        exit(0)
    # else:
    #     print("Command not recognized:", text) # Optional: uncomment for debugging

# --- Main Loop ---
# This setup is cleaner and more direct for collecting audio chunks.
try:
    print("Listening for commands... (say 'exit' to quit)")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', blocksize=BLOCK_SIZE, callback=callback):
        while True:
            # Calculate the number of blocks needed for DURATION seconds of audio
            num_blocks_to_capture = int(SAMPLE_RATE * DURATION / BLOCK_SIZE)
            
            # Collect audio data from the queue
            audio_blocks = []
            for _ in range(num_blocks_to_capture):
                audio_blocks.append(q.get())

            # ✅ 2. PROCESS AUDIO DIRECTLY FROM MEMORY
            # Concatenate the blocks and flatten to a 1D array
            audio_np = np.concatenate(audio_blocks, axis=0).flatten()

            # ✅ 3. TRANSCRIBE WITH FP16 FOR GPU SPEEDUP
            # The fp16 option is safely ignored if running on CPU
            result = model.transcribe(
                audio_np, 
                language="en", 
                fp16=torch.cuda.is_available()
            )
            
            text = result["text"].lower().strip()

            # Only process if speech is detected
            if text:
                print(f"Recognized: '{text}'")
                execute_command(text)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
    exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)