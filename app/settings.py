from os import environ
from dotenv import load_dotenv

load_dotenv()

USER       = environ.get("MYSQL_USER")
PASSWORD   = environ.get("MYSQL_PASSWORD")
HOST       = environ.get("MYSQL_HOST", default="localhost")
DATABASE   = environ.get("MYSQL_DATABASE")
PORT       = environ.get("MYSQL_PORT", default=3306)
ALGORITHM  = environ.get("ALGORITHM")
SECRET_KEY = environ.get("SECRET_KEY")

GITHUB = {
    "client_id":     environ.get("GITHUB_CLIENT_ID"),
    "client_secret": environ.get("GITHUB_CLIENT_SECRET"),
    "callback_uri":  environ.get("GITHUB_CALLBACK_URI")
}
