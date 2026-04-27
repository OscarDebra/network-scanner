"""
config.py
Configuration settings for the Network Scanner application.
All environment-specific settings are defined here so they can be changed in one place without touching application logic.

Change ALLOWED_SUBNET to match your local network. The default is set to a common private subnet, 
but you should verify this before running the scanner, scanning the wrong subnet may get you in trouble.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    DATABASE = "scanner.db"
    ALLOWED_SUBNET = "172.31.0.0/23"
    SCAN_TIMEOUT = 60
    RATE_LIMIT = 30  # minimum time between scans