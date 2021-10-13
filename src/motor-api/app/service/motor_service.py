from multiprocessing import Process
from time import sleep
import logging

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

log = logging.getLogger(__name__)

class MotorService:

    def __init__(self):
      # Back Left Motor
      self.pinsBackLeft = [21, 20, 16, 12]
      self.motorBackLeft = RpiMotorLib.BYJMotor("motorBackLeft", "28BYJ")

      # Back Right Motor
      self. pinsBackRight = [26, 19, 13, 6]
      self.motorBackRight = RpiMotorLib.BYJMotor("motorBackRight", "28BYJ")

      # Front Left Motor
      self.pinsFrontLeft = [5, 11, 9, 10]
      self.motorFrontLeft = RpiMotorLib.BYJMotor("motorFrontLeft", "28BYJ")

      # Front Right Motor
      self.pinsFrontRight = [14, 15, 18, 23]
      self.motorFrontRight = RpiMotorLib.BYJMotor("motorFrontRight", "28BYJ")

      self.motor_startup()

    def motor_startup():
        backLeftMotorProcess = Process(target=rotateMotor,args=(self.motorBackLeft,self.pinsBackLeft,False,15,))
        backRightMotorProcess = Process(target=rotateMotor,args=(self.motorBackRight,self.pinsBackRight,True,15,)) 
        frontLeftMotorProcess = Process(target=rotateMotor,args=(self.motorFrontLeft,self.pinsFrontLeft,True,15,))
        frontRightMotorProcess = Process(target=rotateMotor,args=(self.motorFrontRight,self.pinsFrontRight,False,15,))
        backLeftMotorProcess.start()
        backRightMotorProcess.start()
        sleep(.05)
        frontLeftMotorProcess.start()
        frontRightMotorProcess.start()
        backLeftMotorProcess.join()
        backRightMotorProcess.join()
        frontLeftMotorProcess.join()
        frontRightMotorProcess.join()
        

    def motor_rotate(motor, pins, isClockwise, offset):
        motor.motor_run(pins, .001, offset, isClockwise, False, "half", .05)
        
    def motor_close():
        backLeftMotorProcess = Process(target=rotateMotor,args=(self.motorBackLeft,self.pinsBackLeft,False,135,))
        backRightMotorProcess = Process(target=rotateMotor,args=(self.motorBackRight,self.pinsBackRight,True,135,)) 
        frontLeftMotorProcess = Process(target=rotateMotor,args=(mself.otorFrontLeft,self.pinsFrontLeft,True,135,))
        frontRightMotorProcess = Process(target=rotateMotor,args=(self.motorFrontRight,self.pinsFrontRight,False,135,))
        backLeftMotorProcess.start()
        backRightMotorProcess.start()
        sleep(.05)
        frontLeftMotorProcess.start()
        frontRightMotorProcess.start()
        backLeftMotorProcess.join()
        backRightMotorProcess.join()
        frontLeftMotorProcess.join()
        frontRightMotorProcess.join()
        
    def motor_open():
        backLeftMotorProcess = Process(target=rotateMotor,args=(self.motorBackLeft,self.pinsBackLeft,True,128,))
        backRightMotorProcess = Process(target=rotateMotor,args=(self.motorBackRight,self.pinsBackRight,False,128,))
        frontLeftMotorProcess = Process(target=rotateMotor,args=(self.motorFrontLeft,self.pinsFrontLeft,False,128,))
        frontRightMotorProcess = Process(target=rotateMotor,args=(self.motorFrontRight,self.pinsFrontRight,True,128))

        frontLeftMotorProcess.start()
        frontRightMotorProcess.start()
        sleep(.05)
        backLeftMotorProcess.start()
        backRightMotorProcess.start()
        backLeftMotorProcess.join()
        backRightMotorProcess.join()
        frontLeftMotorProcess.join()
        frontRightMotorProcess.join()
        