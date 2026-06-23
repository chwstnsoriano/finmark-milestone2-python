import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
PASSWORD_SALT = os.getenv("PASSWORD_SALT", "default_salt")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM", "HS256")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "30"))