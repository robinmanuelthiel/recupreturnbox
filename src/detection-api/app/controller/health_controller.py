
import logging
from model.health_model import HealthResult


log = logging.getLogger(__name__)


class HealthStatus:

    def __init__(self, status=True):
        self.status = status

    def unhealthy(self):
        self.status = False


class HealthController:

    def __init__(self):
        self.healthStatus = HealthStatus()

    def check(self):
        return HealthResult(status=self.healthStatus.status)
