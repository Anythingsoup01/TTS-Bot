import yaml

def load_information():
    config = {}
    try:
        with open(".config/config.yaml", "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: The file 'config.yaml' does not exist")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

    return config

def save_information(data):
    yaml_data = {
        "TW_CLIENT_ID": data['TW_CLIENT_ID'],
        "TW_CLIENT_SECRET": data['TW_CLIENT_SECRET'],
        "TW_JOIN": data['TW_JOIN'],
        "TW_NICK": data['TW_NICK'],
        "TW_OAUTH": data['TW_OAUTH'],
        "TW_REFRESH_TOKEN": data['TW_REFRESH_TOKEN'],
        "WS_HOST": data['WS_HOST'],
        "WS_PORT": data['WS_PORT'],
        "WS_PASS": data['WS_PASS'],
    }

    try:
        with open(".config/config.yaml", "w") as file:
            yaml.safe_dump(yaml_data, file)
    except FileNotFoundError:
        print("Error: The file 'config.yaml' does not exist")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
