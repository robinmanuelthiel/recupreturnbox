from fastapi import APIRouter

from controller.motor_controller import MotorController


router = APIRouter()


@router.get("/open", tags=["Motor"])
async def get_open():
    """Opens the motor
    """
    controller = MotorController()
    return controller.motor_open()


@router.get("/close", tags=["Motor"])
async def get_close():
    """Opens the motor
    """
    controller = MotorController()
    return controller.motor_close()


@router.post("/rotate", tags=["Motor"])
async def post_rotate(rotation_offset):
    """Rotates the motor
    """
    controller = MotorController()
    return controller.motor_rotate(rotation_offset)
