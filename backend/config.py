import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    DATABASE = "scanner.db"
    ALLOWED_SUBNET = "10.58.176.0/23"  # only scan your own network
    SCAN_TIMEOUT = 60
    RATE_LIMIT_SECONDS = 30  # min time between scans