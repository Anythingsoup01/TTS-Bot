from types import FunctionType

from managers.moderators import MODEREATORS


class Command_Manager:
    def __init__(self):
        # List of str -> func
        self.public_commands = {}
        self.internal_commands = {}

    def register_func(
        self,
        name: str,
        func: FunctionType,
        cooldown: int,
        internal: bool
    ):
        command = {
            "func": func,
            "cooldown": cooldown,
        }

        if internal:
            self.internal_commands[name] = command
        else:
            self.public_commands[name] = command

    def split_by_n(self, text: str, n: int):
        out = []
        for i in range(0, len(text), n):
            out.append(text[i:i + n])
        return out

    def handle(
        self,
        user: str,
        command: str,
    ):
        is_command = command.startswith("!");
        is_cheer = command.lower().startswith("cheer");
        
        if is_command:
            self._handle_internal_command(user, command)
        elif is_cheer:
            self._handle_public_command(user, command)

    def _handle_internal_command(
        self,
        user: str,
        command: str,
    ):
        parts = command[1:].split()
        cmd = parts[0].lower()
        args = parts[1:]

        if user.lower() not in MODEREATORS:
            return

        if cmd not in self.internal_commands:
            return

        self.internal_commands[cmd]["func"](args)

    def _handle_public_command(
        self,
        user: str,
        text: str,
    ):
        parts = text[:].split()
        cmd = parts[0].lower()
        tmp = self.split_by_n(cmd, 5)

        if len(tmp) != 2:
            return

        cmd = tmp[0]
        bits = tmp[1]
        args = parts[1:]

        if cmd not in self.public_commands:
            return

        self.public_commands[cmd]["func"](user=user, bits=int(bits), args=args)
