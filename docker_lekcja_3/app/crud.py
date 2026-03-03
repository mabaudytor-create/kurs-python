from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models


def get_clients(db: Session):
    return db.query(models.Client).all()


def get_client_orders(db: Session, client_id: int):
    return (
        db.query(models.Order)
        .filter(models.Order.client_id == client_id)
        .all()
    )


def get_client_orders_sum(db: Session):
    """
    Zwraca listę:
    [
      {"client_id": ..., "name": ..., "email": ..., "total_amount": ...},
      ...
    ]
    """
    rows = (
        db.query(
            models.Client.id.label("client_id"),
            models.Client.name,
            models.Client.email,
            func.sum(models.Order.amount).label("total_amount"),
        )
        .join(models.Order, models.Client.id == models.Order.client_id)
        .group_by(models.Client.id, models.Client.name, models.Client.email)
        .all()
    )

    return [
        {
            "client_id": r.client_id,
            "name": r.name,
            "email": r.email,
            "total_amount": float(r.total_amount or 0),
        }
        for r in rows
    ]
