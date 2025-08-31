from gtts import gTTS
import tempfile

def text_to_speech(text: str):
    try:
        tts = gTTS(text=text, lang="en")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
