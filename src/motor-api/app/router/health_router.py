from fastapi import APIRouter

from controller.health_controller import HealthController
from model.health_model import HealthResult


router = APIRouter()


@router.get("", response_model=HealthResult, tags=["Health"])
async def get_health():
    """Returns the health status of the API
    A status `true` is good.
    ```json
    {
        "Status": true
    }
    ```
    """
    controller = HealthController()
    return controller.check()