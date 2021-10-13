import logging

from fastapi import FastAPI, HTTPException


log = logging.getLogger(__name__)


class MotorController:

    def __init__(self):
        try:
            from service.motor_service import MotorService
            self.service = MotorService()
        except Exception  as error:
            log.error(error)
            raise HTTPException(status_code=500, detail=f'{error.__class__.__name__}')

        

    def motor_open(self):
        return self.service.motor_open()


    def motor_close(self):
        return self.service.motor_close()
