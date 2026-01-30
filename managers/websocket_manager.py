from obswebsocket import obsws, events, requests

MAXIMUM_TTS_DONATIONS = 10

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

        self.previous_message_donations: list[str] = []
        self.previous_non_message_donations: list[str] = []

        # THIS SHOULD BE DONE VERY LAST
        # OF INIT
        self.websock.connect()


    def _add_donation_without_message(
        self,
        user: str,
        bits: int
    ):
        if len(self.previous_non_message_donations) >= MAXIMUM_TTS_DONATIONS:
            self.previous_non_message_donations = self.previous_non_message_donations[1:]

        self.previous_non_message_donations.append(f"{user} - {bits} | ")

    def _add_donation_message(
        self,
        user: str,
        bits: int,
        msg: list[str]
    ):
        if len(self.previous_message_donations) >= MAXIMUM_TTS_DONATIONS:
            self.previous_message_donations = self.previous_message_donations[1:]

        self.previous_message_donations.append(f"{user}:{bits} -" + " ".join(msg) + " | ")

    def add_donation(
        self,
        user: str,
        bits: int,
        msg: list[str]
    ):
        if len(msg) > 0:
            self._add_donation_message(user, bits, msg)
        else:
            self._add_donation_without_message(user, bits)

    def on_tts_call(
        self,
        user: str,
        bits: int,
        args: list[str],
    ):
        text: str = ""

        for arg in args:
            text += arg + " "

        userBox = f"{user} : {bits} Bits"

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_USERNAME",
            inputSettings={"text": userBox}
        ))

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_MESSAGE",
            inputSettings={"text": text}
        ))

        self.add_donation(user, bits, args)

        text = ""
        for arg in self.previous_message_donations:
            text += arg + " "

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_MSG_SCROLL",
            inputSettings={"text": text}
        ))

        text = ""
        for arg in self.previous_non_message_donations:
            text += arg + " "

        self.websock.call(requests.SetInputSettings(
            inputName="TTS_DONO_SCROLL",
            inputSettings={"text": text}
        ))
