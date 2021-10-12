import os
import logging


class DefaultConfig:

    # General Stuff
    RELEASE = os.environ.get("RELEASE", "1.0")
    API_KEY = os.environ.get("API_KEY", "test")
    LOCAL_DEV = os.environ.get("LOCAL_DEV", False)

    # API Description
    API_TASK = os.environ.get("API_TASK", "Detection API")
    API_TITLE = "Recup Retun Box - {} API".format(API_TASK)
    API_DESCRIPTION = ""
    
    ROOT_PATH = os.environ.get("ROOT_PATH", "/")

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))