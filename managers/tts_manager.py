from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile


from filters.profanity_filter import IllegalWords

class TTS_Manager:
    def __init__(self):
        pass

    def can_speak(self, args: list[str]) -> bool:
        if any(arg.lower() in IllegalWords for arg in args):
            return False

        return True


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

        except Exception as e:
            print(f"An error occurred: {e}")
