import pathlib
from flask.cli import load_dotenv

APP_PATH = pathlib.Path(__file__)
load_dotenv(str(APP_PATH.parent.parent.joinpath('.env').absolute()))
