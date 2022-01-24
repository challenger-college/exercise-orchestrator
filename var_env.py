from dotenv import load_dotenv
from pathlib import Path

import sys

if Path(".env.local").is_file():
    load_dotenv(".env.local")
elif Path(".env").is_file():
    load_dotenv(".env")
else:
    print("Error, please add .env or .env.local", file=sys.stderr)
    exit(1)
