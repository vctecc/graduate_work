import os

API_HOST = os.getenv("PAYMENTS_API_HOST", "localhost")
API_PORT = os.getenv("PAYMENTS_API_PORT", "8000")

API_SERVICE_URL = f"{API_HOST}:{API_PORT}"
API = "v1"
