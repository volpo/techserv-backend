import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class Equipo(BaseModel):
    tipo: str = Field(min_length=1, max_length=255)
    marca: str = Field(min_length=1, max_length=255)
    modelo: str = Field(min_length=1, max_length=255)
    numero_serie: str = Field(min_length=1, max_length=255)
    cliente_id: uuid.UUID