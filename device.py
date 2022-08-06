from redis_om import (EmbeddedJsonModel, Field, HashModel, JsonModel)
from pydantic import PositiveInt
from typing import Optional, List

class DeviceLog(JsonModel):
    # Indexed for exact text matching
    device_fk_id: int = Field(index=True)
    latitude: float = Field(index=True)

    # Indexed for numeric matching
    longitude: float = Field(index=True)

    time_stamp: str = Field(index=True)

    sts: str = Field(index=True)

    speed: int = Field()


