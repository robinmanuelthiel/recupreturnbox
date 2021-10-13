from pydantic import BaseModel


class HealthResult(BaseModel):
    status: bool
