"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import scaling_api.views
