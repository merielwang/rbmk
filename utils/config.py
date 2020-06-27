import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)


PROD_DB_CONFIG = {
    "DATABASE": os.getenv('DB_NAME'),
    "USER": os.getenv('DB_USERNAME'),
    "PASSWORD": os.getenv('DB_PWD'),
    "HOST": os.getenv('DB_HOST'),
    "PORT": os.getenv('DB_PORT'),
}

DEV_DB_CONFIG = {
    "DATABASE": os.getenv('DB_NAME'),
    "USER": os.getenv('DB_USERNAME'),
    "PASSWORD": os.getenv('DB_PWD'),
    "HOST": os.getenv('DB_HOST'),
    "PORT": os.getenv('DB_PORT'),
}

DATA_KEY_1M = "Time Series (1min)"
DATA_KEY_5M = "Time Series (5min)"
DATA_INTERVAL_1M = "1min"
DATA_INTERVAL_5M = "5min"
