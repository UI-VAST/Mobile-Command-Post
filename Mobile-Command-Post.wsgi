#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/Mobile-Command-Post/SatComm")

from SatComm import app as application
application.secret_key = 'something super SUPER secret'
