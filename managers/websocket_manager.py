from obswebsocket import obsws, events, requests


class Websocket_Manager:
    def __init__(
        self,
        host: str,
        port: int,
        password: str
    ):
        self.websock = obsws(
            host=host,
            port=port,
            password=password
        )

        # THIS SHOULD BE DONE VERY LAST
        # OF INIT
        self.websock.connect()

    def on_tts_call(
        self,
        user: str,
        args: list[str],
    ):
        text: str = ""

        max_chars_per_line = 50
        char_count = 0
        for arg in args:

            # word + " "
            if len(arg) + 1 + char_count > max_chars_per_line:
                text += "\n"
                char_count = 0

            if char_count != 0: text += " "
            text += arg
            char_count = len(text) % max_chars_per_line + 1

            if char_count >= max_chars_per_line:
                text += "\n"

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_USERNAME",
            inputSettings={"text": user}
        ))

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_MESSAGE",
            inputSettings={"text": text }
        ))

