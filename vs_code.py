import os
import whisper
import sounddevice as sd
import wavio
import subprocess
import imageio_ffmpeg  # <-- Changed this line (removed 'as ffmpeg')

# --- FIX: Add FFmpeg to the system's PATH ---
# whisper needs ffmpeg to load audio files, and imageio_ffmpeg provides it.
# This adds the directory containing ffmpeg.exe to the PATH.
try:
    ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] += os.pathsep + ffmpeg_dir
    print("✅ FFmpeg path added to environment.")
except Exception as e:
    print(f"⚠️ Could not find or add FFmpeg path: {e}")
    print("Please ensure 'imageio_ffmpeg' is installed (`pip install imageio_ffmpeg`)")
    print("Or, install FFmpeg manually and add it to your system's PATH.")
# -------------------------------------------


# --- Settings ---
SAMPLE_RATE = 16000
DURATION = 5  # seconds

def record_audio(filename="command.wav"):
    """Records audio from the microphone."""
    print("🎙 Listening...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wavio.write(filename, audio, SAMPLE_RATE, sampwidth=2)
    print("✅ Audio captured.")

def recognize_speech(model, filename="command.wav"):
    """Transcribes audio using the pre-loaded whisper model."""
    # Model is now passed as an argument, not loaded here
    result = model.transcribe(filename)
    text = result["text"].strip().lower()
    print(f"🗣 You said: {text}")
    return text

def open_vscode():
    """Opens the VS Code application."""
    print("🚀 Opening VS Code...")
    try:
        subprocess.Popen(["code"])  # assumes `code` command is on PATH
    except FileNotFoundError:
        print("❌ Error: 'code' command not found. Is VS Code installed and on your PATH?")

def create_hello_world():
    """Creates a 'hello.py' file and opens it in VS Code."""
    print("🧠 Creating Hello World program...")
    os.makedirs("voice_generated", exist_ok=True)
    file_path = os.path.join("voice_generated", "hello.py")
    
    with open(file_path, "w") as f:
        f.write('print("Hello, world!")\n')
    
    try:
        subprocess.Popen(["code", file_path])  # open file in VS Code
    except FileNotFoundError:
        print(f"❌ Error: 'code' command not found. Could not open {file_path}.")

def main():
    # --- PERFORMANCE FIX: Load model once at the start ---
    print("Loading whisper model (this may take a moment)...")
    try:
        model = whisper.load_model("small")
    except Exception as e:
        print(f"❌ Failed to load whisper model: {e}")
        print("Ensure 'openai-whisper' is installed (`pip install openai-whisper`)")
        return
    print("✅ Model loaded. Assistant is ready.")
    # ----------------------------------------------------

    record_audio()
    command = recognize_speech(model, "command.wav")  # <-- Pass model in

    if "code" in command:
        open_vscode()
        print("🎧 Waiting for next instruction...")
        record_audio("next_command.wav")
        next_command = recognize_speech(model, "next_command.wav")  # <-- Pass model in

        if "hello world" in next_command or "hello" in next_command:
            create_hello_world()
        else:
            print("❌ No known action for that command.")
    else:
        print("💤 No trigger word detected.")

if __name__ == "__main__":
    main()