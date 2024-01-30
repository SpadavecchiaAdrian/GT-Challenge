from app.services.CRUD_base import CRUDBase
from app.models.vehicle import Vehicle as VehicleMD
from app.schemas.vehicle import Vehicle


class VehicleService(CRUDBase):
    pass


vehicle_service = VehicleService(VehicleMD, Vehicle)
