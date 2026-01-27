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
        "CLIENT_ID": data['CLIENT_ID'],
        "CLIENT_SECRET": data['CLIENT_SECRET'],
        "JOIN": data['JOIN'],
        "NICK": data['NICK'],
        "OAUTH": data['OAUTH'],
        "REFRESH_TOKEN": data['REFRESH_TOKEN'],
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
