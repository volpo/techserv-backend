import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.security import EstadoTicket, UrgenciaTicket

class Ticket(BaseModel):
    titulo: str = Field(min_length=3, max_length=255)
    descripcion: str = Field(min_length=3, max_length=255)
    estado: EstadoTicket | None = None
    urgencia: UrgenciaTicket
    direccion: str = Field(min_length=1, max_length=255)
    fecha_creacion: datetime | None = None
    fecha_cierre: datetime | None = None
    cliente_id: uuid.UUID | None = None
    tecnico_id: uuid.UUID | None = None
    equipo_id: uuid.UUID | None = None

class TicketRead(Ticket):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class TicketCreate(Ticket):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = None