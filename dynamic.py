import sys
import importlib
import configparser

from implementation import *
from implementation import ibuddy

# Read chosen implementation from config
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    implementation = config.get('general', 'implementation')
except:
    sys.exit('[error] Failed to read config file!')
    
# Load implementation
implementations = [subclass.__name__ for subclass in ibuddy.__subclasses__()]
try:
    if implementation in implementations:
        ibuddy = getattr(globals()[implementation], implementation)()
    else:
        raise
except:
    sys.exit('[error] Failed to load implementation!')

# Fun!
ibuddy.test()