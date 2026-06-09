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
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.AREA_ADMINISTRATIVA, UserRole.TECNICO, UserRole.CLIENTE, UserRole.SUPERVISOR))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Ticket]:
    query = select(Ticket).order_by(Ticket.fecha_creacion.desc())

    if current_user.role == UserRole.CLIENTE:
        query = query.where(Ticket.cliente_id == current_user.id)

    if current_user.role == UserRole.TECNICO:
        query = query.where(Ticket.tecnico_id == current_user.id)
    
    result = await db.execute(query)
    return list(result.scalars().all())

@router.get("/{id}", response_model=TicketRead, status_code=status.HTTP_200_OK)
async def one_ticket(
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.AREA_ADMINISTRATIVA, UserRole.TECNICO, UserRole.CLIENTE, UserRole.SUPERVISOR))],
    id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[Ticket]:
    query = select(Ticket).where(Ticket.id == id)
    result = await db.execute(query)
    ticket = result.scalars().first()

    if not ticket: raise HTTPException(404, "Ticket not found")

    if current_user.role == UserRole.CLIENTE:
        if current_user.id != ticket.cliente_id : raise HTTPException(403, "Insufficient privileges")

    if current_user.role == UserRole.TECNICO:
        if current_user.id != ticket.tecnico_id : raise HTTPException(403, "Insufficient privileges")
    
    return ticket

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: TicketCreate,
    current_user: Annotated[User, Depends(require_roles(UserRole.ADMINISTRADOR, UserRole.SUPERVISOR, UserRole.CLIENTE))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    ticket = Ticket(
        id=payload.id or uuid.uuid4(),
        titulo=payload.titulo,
        descripcion=payload.descripcion,
        estado=payload.estado or EstadoTicket.ABIERTO,
        urgencia=payload.urgencia,
        direccion=payload.direccion,
        cliente_id=payload.cliente_id or current_user.id,
        tecnico_id=payload.tecnico_id,
        equipo_id=payload.equipo_id
    )
    db.add(ticket)
    await db.flush()
    await db.refresh(ticket)
    return ticket