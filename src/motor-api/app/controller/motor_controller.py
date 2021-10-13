
import logging

from service.motor_service import MotorService


log = logging.getLogger(__name__)


class MotorController:

    def __init__(self):
        self.service = MotorService()

    def open(self):
        return self.service.motor_open()

    def close(self):
        return "close"
