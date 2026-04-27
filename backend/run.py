"""
run.py
Entry point for the Network Scanner Flask application.
Run this file with: sudo python run.py
Requires sudo so nmap can read MAC addresses via ARP.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)