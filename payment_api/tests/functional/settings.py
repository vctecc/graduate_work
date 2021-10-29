import os

API_HOST = os.getenv("PAYMENTS_HOST", "localhost")
API_PORT = os.getenv("PAYMENTS_PORT", "8000")

API_SERVICE_URL = f"{API_HOST}:{API_PORT}"
API = "v1"
