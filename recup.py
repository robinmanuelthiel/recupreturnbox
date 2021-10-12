import RPi.GPIO as GPIO
import subprocess
import json
from time import sleep
from RpiMotorLib import RpiMotorLib
from multiprocessing import Process

# Back Left Motor
pinsBackLeft = [21, 20, 16, 12];
motorBackLeft = RpiMotorLib.BYJMotor("motorBackLeft", "28BYJ");

# Back Right Motor
pinsBackRight = [26, 19, 13, 6];
motorBackRight = RpiMotorLib.BYJMotor("motorBackRight", "28BYJ");

# Front Left Motor
pinsFrontLeft = [5, 11, 9, 10];
motorFrontLeft = RpiMotorLib.BYJMotor("motorFrontLeft", "28BYJ");

# Front Right Motor
pinsFrontRight = [14, 15, 18, 23];
motorFrontRight = RpiMotorLib.BYJMotor("motorFrontRight", "28BYJ");

def startup():
    backLeftMotorProcess = Process(target=rotateMotor,args=(motorBackLeft,pinsBackLeft,False,15,));
    backRightMotorProcess = Process(target=rotateMotor,args=(motorBackRight,pinsBackRight,True,15,)); 
    frontLeftMotorProcess = Process(target=rotateMotor,args=(motorFrontLeft,pinsFrontLeft,True,15,));
    frontRightMotorProcess = Process(target=rotateMotor,args=(motorFrontRight,pinsFrontRight,False,15,));
    backLeftMotorProcess.start();
    backRightMotorProcess.start();
    sleep(.05)
    frontLeftMotorProcess.start();
    frontRightMotorProcess.start();
    backLeftMotorProcess.join();
    backRightMotorProcess.join();
    frontLeftMotorProcess.join();
    frontRightMotorProcess.join();
    

def rotateMotor(motor, pins, isClockwise, offset):
    motor.motor_run(pins, .001, offset, isClockwise, False, "half", .05);
    
def close():
    backLeftMotorProcess = Process(target=rotateMotor,args=(motorBackLeft,pinsBackLeft,False,135,));
    backRightMotorProcess = Process(target=rotateMotor,args=(motorBackRight,pinsBackRight,True,135,)); 
    frontLeftMotorProcess = Process(target=rotateMotor,args=(motorFrontLeft,pinsFrontLeft,True,135,));
    frontRightMotorProcess = Process(target=rotateMotor,args=(motorFrontRight,pinsFrontRight,False,135,));
    backLeftMotorProcess.start();
    backRightMotorProcess.start();
    sleep(.05)
    frontLeftMotorProcess.start();
    frontRightMotorProcess.start();
    backLeftMotorProcess.join();
    backRightMotorProcess.join();
    frontLeftMotorProcess.join();
    frontRightMotorProcess.join();
    
def open():
    backLeftMotorProcess = Process(target=rotateMotor,args=(motorBackLeft,pinsBackLeft,True,128,));
    backRightMotorProcess = Process(target=rotateMotor,args=(motorBackRight,pinsBackRight,False,128,));
    frontLeftMotorProcess = Process(target=rotateMotor,args=(motorFrontLeft,pinsFrontLeft,False,128,));
    frontRightMotorProcess = Process(target=rotateMotor,args=(motorFrontRight,pinsFrontRight,True,128));

    frontLeftMotorProcess.start();
    frontRightMotorProcess.start();
    sleep(.05)
    backLeftMotorProcess.start();
    backRightMotorProcess.start();
    backLeftMotorProcess.join();
    backRightMotorProcess.join();
    frontLeftMotorProcess.join();
    frontRightMotorProcess.join();
    
def checkCamera():
    subprocess.call(["fswebcam", "-d", "/dev/video0", "-r", "1280x720", "--no-banner", "./pic.jpg"])
    sleep(2);
    result = subprocess.check_output(["curl", "-X", "POST", "https://westeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/41701604-a314-42b7-865a-1a757d1e5b6f/classify/iterations/Iteration3/image", "--header", "Prediction-Key: 4d61970eb0664dc5999cf6775912d133", "-F", "imageData=@./pic.jpg"])
    parsedResult = json.loads(result)
    print(parsedResult)
    
    try:
        cupDetected = parsedResult["predictions"][0]["tagName"] == "recup";
        #cup = parsedResult["predictions"][1]
        
        if (cupDetected == True):
            return True
        else:
            return False
    except:
        print("Error")
        return False
        
startup();
while (True):
    isCup = checkCamera(); 
    if (isCup == True):
      print("Cup detected");
      open()
      sleep(.5);
      close();
    else:
        print("No cup detected");
