from multiprocessing import Process
from time import sleep
import logging
from config import DefaultConfig

from RpiMotorLib import RpiMotorLib

log = logging.getLogger(__name__)


class MotorService:

    def __init__(self, config=DefaultConfig):
        # Back Left Motor
        self.pinsPrimaryMotor = [
            config.MOTOR1.pin1,
            config.MOTOR1.pin2,
            config.MOTOR1.pin3,
            config.MOTOR1.pin4]
        self.primaryMotor = RpiMotorLib.BYJMotor("motorPrimary", "28BYJ")

        self.motor_startup()

    def motor_startup(self):
        primaryMotorProcess = Process(
            target=self.motor_move,
            args=(
                self.primaryMotor, self.pinsBackLeft, False, 15,)
        )
        primaryMotorProcess.start()
        sleep(.05)
        primaryMotorProcess.join()

    def motor_move(self, motor, pins, isClockwise, offset):
        motor.motor_run(pins, .001, offset, isClockwise, False, "half", .05)

    def motor_close(self):
        primaryMotorProcess = Process(
            target=self.motor_move,
            args=(self.primaryMotor, self.pinsPrimaryMotor, False, 128,)
        )
        primaryMotorProcess.start()
        sleep(.05)
        primaryMotorProcess.join()

    def motor_open(self):
        primaryMotorProcess = Process(
            target=self.motor_move,
            args=(self.primaryMotor, self.pinsPrimaryMotor, True, 128,)
        )

        primaryMotorProcess.start()
        sleep(.05)
        primaryMotorProcess.join()

    def motor_rotate(self, rotation_offset):
        primaryMotorProcess = Process(
            target=self.motor_move,
            args=(
                self.primaryMotor,
                self.pinsPrimaryMotor,
                True,
                rotation_offset)
        )

        primaryMotorProcess.start()
        sleep(.05)
        primaryMotorProcess.join()
