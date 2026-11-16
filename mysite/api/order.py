from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Order, Product, UserProfile, OrderStatus
from mysite.database.schema import OrderOutSchema, OrderInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


order_router = APIRouter(prefix='/order', tags=['Order CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@order_router.post('/create/', response_model=OrderOutSchema)
async def create_order(
    order: OrderInputSchema,
    db: Session = Depends(get_db)
):
    user_db = db.query(UserProfile).filter(
        UserProfile.id == order.user_id
    ).first()

    if not user_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай колдонуучу жок'
        )

    product_db = db.query(Product).filter(
        Product.id == order.product_id
    ).first()

    if not product_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай продукт жок'
        )

    order_db = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        city_id=order.city_id,
        quantity=order.quantity,
        total_price=product_db.price * order.quantity,
        order_status=OrderStatus.pending
    )

    db.add(order_db)
    db.commit()
    db.refresh(order_db)

    return order_db


@order_router.get('/', response_model=List[OrderOutSchema])
async def order_list(
    db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/{order_id}', response_model=OrderOutSchema)
async def order_detail(
    order_id: int,
    db: Session = Depends(get_db)):
    order_db = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first())

    if not order_db:
        raise HTTPException(status_code=404, detail='Мындай заказ жок')
    return order_db


@order_router.put('/{order_id}', response_model=dict)
async def update_order(
    order_id: int,
    order: OrderInputSchema,
    db: Session = Depends(get_db)):
    order_db = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first())

    if not order_db:
        raise HTTPException(status_code=404, detail='Мындай заказ жок')

    product_db = db.query(Product).filter(Product.id == order.product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Мындай продукт жок')

    order_db.user_id = order.user_id
    order_db.product_id = order.product_id
    order_db.quantity = order.quantity
    order_db.total_price = product_db.price * order.quantity

    db.commit()
    db.refresh(order_db)
    return {'message': 'Заказ озгорулду'}


@order_router.patch('/{order_id}/status/', response_model=OrderOutSchema)
async def update_order_status(
    order_id: int,
    order_status: OrderStatus,
    db: Session = Depends(get_db)):
    order_db = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first())

    if not order_db:
        raise HTTPException(status_code=404, detail='Мындай заказ жок')

    order_db.order_status = order_status
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.delete('/{order_id}/', response_model=dict)
async def delete_order(
    order_id: int, db: Session = Depends(get_db)):
    order_db = (db.query(Order).filter(Order.id == order_id).first())

    if not order_db:
        raise HTTPException(status_code=404, detail='Мындай заказ жок')

    db.delete(order_db)
    db.commit()

    return {'message': 'Заказ удалена'}