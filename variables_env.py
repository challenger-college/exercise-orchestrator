import logging

from dotenv import load_dotenv
from pathlib import Path

import os


def load_environment_variable():
    if Path(".env.local").is_file():
        load_dotenv(".env.local")
    elif Path(".env").is_file():
        load_dotenv(".env")
    else:
        logging.critical("Please add .env file or .env.local")
        exit(1)
    variables = {
        "IP": os.getenv("IP_WEBSERVICE"),
        "TOKEN": os.getenv("API_TOKEN"),
        "CONTAINER_TIME_OUT": os.getenv("CONTAINER_TIME_OUT")
    }
    for name, value in variables.items():
        if value is None:
            logging.critical(f"Please add {name} variable in .env file.")
            exit(1)


def get_web_service_ip():
    return os.getenv("IP_WEBSERVICE")


def get_token_api():
    return os.getenv("API_TOKEN")


def get_container_time_out():
    return os.getenv("CONTAINER_TIME_OUT")