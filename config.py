import json
import os
import sys


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

def default_config():

    return {
        "workspaces": {
            "Default": {
                "applications": []
            }
        }
    }


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return default_config()

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        # New format
        if "workspaces" in data:

            if not data["workspaces"]:
                return default_config()

            return data


        # Old format
        if "applications" in data:

            return {
                "workspaces": {
                    "Default": {
                        "applications":
                            data["applications"]
                    }
                }
            }


        return default_config()


    except (
        json.JSONDecodeError,
        OSError
    ):

        return default_config()


def save_config(config):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_apps():

    config = load_config()

    return (
        config["workspaces"]
        ["Default"]
        ["applications"]
    )


def save_apps(applications):

    config = load_config()

    config["workspaces"]["Default"]["applications"] = [

        {
            "name": app["name"],
            "path": app["path"]
        }

        for app in applications

    ]

    save_config(config)