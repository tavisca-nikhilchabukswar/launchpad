import psycopg2
from configparser import ConfigParser
import sys

class tavisca_app:
    def __init__(self):
        self.app_name = None
        self.app_instance_type = None
        self.app_instance_count = None
        self.app_env = None
        self.app_type = None
        self.app_desired_containers = None
    