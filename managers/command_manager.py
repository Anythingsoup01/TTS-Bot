from types import FunctionType


class Command_Manager:
    def __init__(self):
        # List of str -> func
        self.commands = {}

    def register_func(
        self,
        name: str,
        func: FunctionType,
        cooldown: int,
        mod_only: bool
    ):
        self.commands[name] = {
            "func": func,
            "cooldown": cooldown,
            "mod_only": mod_only,
            "last_used": 0
        }

    def handle(
        self,
        user: str,
        text: str,
        is_mod: bool
    ):
        if not text.startswith("!"):
            return

        parts = text[1:].split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd not in self.commands:
            return

        if self.commands[cmd]["mod_only"] and not is_mod:
            return

        self.commands[cmd]["func"](user=user, args=args)
