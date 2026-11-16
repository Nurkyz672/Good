from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Product
from mysite.database.schema import ProductOutSchema, ProductInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_router = APIRouter(prefix='/product', tags=['Product CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/create/', response_model=ProductOutSchema)
async def create_product(
    product: ProductInputSchema,
    db: Session = Depends(get_db)):
    product_db = Product(
        store_id=product.store_id,
        product_name=product.product_name,
        price=product.price,
        description=product.description,
        is_original=product.is_original
    )

    db.add(product_db)
    db.commit()
    db.refresh(product_db)

    return product_db


@product_router.get('/', response_model=List[ProductOutSchema])
async def product_list(
    db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}', response_model=ProductOutSchema)
async def product_detail(
    product_id: int,
    db: Session = Depends(get_db)):
    product_db = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first())

    if not product_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай продукт жок')
    return product_db


@product_router.put('/{product_id}', response_model=dict)
async def update_product(
    product_id: int,
    product: ProductInputSchema,
    db: Session = Depends(get_db)):
    product_db = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first())

    if not product_db:
        raise HTTPException(status_code=404, detail='Мындай продукт жок')

    product_db.store_id = product.store_id
    product_db.product_name = product.product_name
    product_db.price = product.price
    product_db.description = product.description
    product_db.is_original = product.is_original

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт озгорулду'}


@product_router.delete('/{product_id}/', response_model=dict)
async def delete_product(
    product_id: int, db: Session = Depends(get_db)):
    product_db = (db.query(Product).filter(Product.id == product_id).first())

    if not product_db:
        raise HTTPException(status_code=404, detail='Мындай продукт жок')

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт удален'}