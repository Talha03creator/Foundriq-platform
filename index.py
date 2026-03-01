import os
import sys

# Ensure the project root is in the Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import the actual app from the server module
from server.main import app
