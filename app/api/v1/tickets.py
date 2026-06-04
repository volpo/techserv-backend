import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.core.security import EstadoTicket, UrgenciaTicket, UserRole
from app.models import Ticket, User
from app.schemas.ticket import TicketRead, TicketCreate

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("", response_model=list[TicketRead])
async def list_tickets(
    _: Annotated[User, Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.AREA_ADMINISTRATIVA))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Ticket]:
    result = await db.execute(select(Ticket).order_by(Ticket.fecha_creacion.desc()))
    return list(result.scalars().all())

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: TicketCreate,
    _: Annotated[User, Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.AREA_ADMINISTRATIVA))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    ticket = Ticket(
        id=payload.id or uuid.uuid4(),
        titulo=payload.titulo,
        descripcion=payload.descripcion,
        estado=payload.estado,
        urgencia=payload.urgencia,
        cliente_id=payload.cliente_id,
        tecnico_id=payload.tecnico_id,
        equipo_id=payload.equipo_id
    )
    db.add(ticket)
    await db.flush()
    await db.refresh(ticket)
    return ticket