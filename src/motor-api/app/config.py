import os
import logging


class DefaultConfig:

    # General Stuff
    RELEASE = os.environ.get("RELEASE", "1.0")
    API_KEY = os.environ.get("API_KEY", "test")
    LOCAL_DEV = os.environ.get("LOCAL_DEV", False)

    # API Description
    API_TASK = os.environ.get("API_TASK", "Motor")
    API_TITLE = "Recup Retun Box - {} API".format(API_TASK)
    API_DESCRIPTION = ""

    MOTOR1 = {
        "pin1": os.environ.get("MOTOR1_PIN1", "17"),
        "pin2": os.environ.get("MOTOR1_PIN2", "18"),
        "pin3": os.environ.get("MOTOR1_PIN3", "21"),
        "pin4": os.environ.get("MOTOR1_PIN4", "22")
    }

    ROOT_PATH = os.environ.get("ROOT_PATH", "/")

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
