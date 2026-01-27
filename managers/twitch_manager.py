from managers.save_manager import load_information, save_information
from managers.command_manager import Command_Manager
from managers.tts_manager import TTS_Manager
import requests, socket, ssl

class Twitch_Manager:
    def __init__(self):

        self.sock = None

        self._iternal_socket_handler()

        self.running = True
        self.instance_running = False

        self.tts_manager = TTS_Manager()

        self.command_manager = Command_Manager()
        self.command_manager.register_func("close", self.close, 0, True)
        self.command_manager.register_func("restart", self.restart, 0, True)
        self.command_manager.register_func("say", self.tts_manager.speak, 0, False)

    def refresh_access_token(self):
        r = requests.post(
        "https://id.twitch.tv/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": self.config["REFRESH_TOKEN"],
            "client_id": self.config["CLIENT_ID"],
            "client_secret": self.config["CLIENT_SECRET"],
            },
        timeout=10,
        )
        r.raise_for_status()
        tokens = r.json()

        self.config['OAUTH'] = tokens['access_token']
        self.config['REFRESH_TOKEN'] = tokens['refresh_token']

        save_information(self.config)

    def _iternal_socket_handler(self):
        if self.sock is not None:
            self.sock = self.sock.close()

        self.config = load_information()
        self.refresh_access_token()

        server = "irc.chat.twitch.tv"
        port = 6697

        oauth = f"PASS oauth:{self.config['OAUTH']}\r\n"
        nick =  f"NICK {self.config['NICK']}\r\n"
        join =  f"JOIN #{self.config['JOIN']}\r\n"

        context = ssl.create_default_context()

        self.sock = socket.create_connection((server, port))
        self.sock = context.wrap_socket(self.sock, server_hostname=server)

        self.sock.sendall(b"CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership\r\n")
        self.sock.sendall(oauth.encode("utf-8"))
        self.sock.sendall(nick.encode("utf-8"))
        self.sock.sendall(join.encode("utf-8"))

    def shutdown(self):
        if self.sock is not None:
            self.sock = self.sock.close()


    def parse_message(self, raw: str):
        if "PRIVMSG" not in raw:
            return None, None

        prefix, msg = raw.split("PRIVMSG", 1)
        user = prefix.split("!", 1)[0][1:]
        user = user.split(":", 1)[1].strip()
        text = msg.split(":", 1)[1].strip()

        return user, text

    def is_mod(self, user: str):
        print(user)
        if user == "anythingsoup":
            return True
        return False

    def close(self, user: str, args: list[str]):
        self.running = False
        self.instance_running = False

    def restart(self, user: str, args: list[str]):
        self.instance_running = False

    def run(self):
        while self.running:
            self._iternal_socket_handler()
            self.instance_running = True
            self.run_instance()

    def run_instance(self):
        while self.instance_running:
            data = self.sock.recv(4096).decode("utf-8", errors="ignore").strip()

            if data.startswith("PING"):
                self.sock.send(b"PONG :tmi.twitch.tv\r\n")
                continue

            user, text = self.parse_message(data)
            if text:
                self.command_manager.handle(user, text, self.is_mod(user))
