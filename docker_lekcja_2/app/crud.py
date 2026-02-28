from sqlalchemy.orm import Session
from . import models

def get_clients(db: Session):
    return db.query(models.Client).all()

def get_client_orders(db: Session, client_id: int):
    return db.query(models.Order).filter(models.Order.client_id == client_id).all()

def get_client_orders_sum(db: Session):
    return db.query(models.Client.id, models.Client.name, models.Client.email,
                    models.Order.amount).join(models.Order, models.Client.id == models.Order.client_id).all()
