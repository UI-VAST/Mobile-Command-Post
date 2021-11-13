#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/Mobile-Command-Post/")

from SatComm import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
