from fastapi import APIRouter

from controller.motor_controller import MotorController


router = APIRouter()


@router.get("/open", tags=["Motor"])
async def get_open():
    """Opens the motor
    """
    controller = MotorController()
    return controller.open()


@router.get("/close", tags=["Motor"])
async def get_close():
    """Opens the motor
    """
    controller = MotorController()
    return controller.close()
