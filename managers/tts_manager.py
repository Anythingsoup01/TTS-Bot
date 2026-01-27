from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile


class TTS_Manager:
    def __init__(self):
        pass

    def speak(self, user: str, args: list[str]):
        my_string = f"{user} says: " + " ".join(args)
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_filename = fp.name

            tts = gTTS(text=my_string, lang='en', slow=False)
            tts.save(temp_filename)

            audio = AudioSegment.from_mp3(temp_filename)
            audio = audio - 10
            play(audio)

            # Optional: remove the file after playing (this part might need refinement for timing)
            # os.remove(temp_filename) 
        except Exception as e:
            print(f"An error occurred: {e}")
