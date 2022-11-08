import re, os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from moniker_handler import Handler, Config

configFile = os.path.join(os.path.dirname(__file__), "config/monikers.json")

handler = Handler(
    Config(configFile), 
    {
    }
)

handler.subscribe()