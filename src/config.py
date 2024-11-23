##############################################
# Title: Modular Config Script
# Author: Christopher Romanillos
# Description: modular config script
# Date: 11/23/24
# Version: 1.0
##############################################
import yaml
import os
from dotenv import load_dotenv

def load_config(config_path):
    """Load configuration from a YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def load_env_variables(key):
    """Load environment variables."""
    load_dotenv()
    return os.getenv(key)
 
