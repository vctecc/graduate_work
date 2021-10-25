import os

API_HOST = os.getenv("SUBSCRIPTION_HOST", "localhost")
API_PORT = os.getenv("SUBSCRIPTION_PORT", "8001")

API_SERVICE_URL = f"{API_HOST}:{API_PORT}"
API_VERSION = "v1"

ALGORITHM = "HS256"
SECRET_KEY = "super-secret"
USER_ID = 'a49b436a-d0b3-4e3e-84e5-ac9204a33042'
