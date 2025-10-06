import os
import whisper
import sounddevice as sd
import wavio
import subprocess
import imageio_ffmpeg as ffmpeg

# --- Settings ---
SAMPLE_RATE = 16000
DURATION = 5  # seconds

def record_audio(filename="command.wav"):
    print("🎙 Listening...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    wavio.write(filename, audio, SAMPLE_RATE, sampwidth=2)
    print("✅ Audio captured.")

def recognize_speech(filename="command.wav"):
    model = whisper.load_model("small")
    result = model.transcribe(filename)
    text = result["text"].strip().lower()
    print(f"🗣 You said: {text}")
    return text

def open_vscode():
    print("🚀 Opening VS Code...")
    subprocess.Popen(["code"])  # assumes `code` command is on PATH

def create_hello_world():
    print("🧠 Creating Hello World program...")
    os.makedirs("voice_generated", exist_ok=True)
    file_path = os.path.join("voice_generated", "hello.py")
    with open(file_path, "w") as f:
        f.write('print("Hello, world!")\n')
    subprocess.Popen(["code", file_path])  # open file in VS Code

def main():
    record_audio()
    command = recognize_speech()

    if "code" in command:
        open_vscode()
        print("🎧 Waiting for next instruction...")
        record_audio("next_command.wav")
        next_command = recognize_speech("next_command.wav")

        if "hello world" in next_command or "hello" in next_command:
            create_hello_world()
        else:
            print("❌ No known action for that command.")
    else:
        print("💤 No trigger word detected.")

if __name__ == "__main__":
    main()
