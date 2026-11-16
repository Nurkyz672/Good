from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import City
from mysite.database.schema import CityOutSchema, CityInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


city_router = APIRouter(prefix='/city', tags=['City'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.post('/create/', response_model=CityOutSchema)
async def create_city(
    city: CityInputSchema,
    db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.city_name == city.city_name).first()
    if city_db:
        raise HTTPException(status_code=400, detail='Мындай шаар бар')

    city_db = City(
        city_name=city.city_name,
        city_image=city.city_image
    )

    db.add(city_db)
    db.commit()
    db.refresh(city_db)

    return city_db


@city_router.get('/', response_model=List[CityOutSchema])
async def city_list(
    db: Session = Depends(get_db)):
    return db.query(City).all()


@city_router.get('/{city_id}', response_model=CityOutSchema)
async def city_detail(
    city_id: int,
    db: Session = Depends(get_db)):
    city_db = (
        db.query(City)
        .filter(City.id == city_id)
        .first())

    if not city_db:
        raise HTTPException(status_code=404, detail='Мындай шаар жок')
    return city_db


@city_router.put('/{city_id}', response_model=dict)
async def update_city(
    city_id: int,
    city: CityInputSchema,
    db: Session = Depends(get_db)):
    city_db = (
        db.query(City)
        .filter(City.id == city_id)
        .first())

    if not city_db:
        raise HTTPException(status_code=404, detail='Мындай шаар жок')

    name_db = (
        db.query(City)
        .filter(City.city_name == city.city_name, City.id != city_id)
        .first())
    if name_db:
        raise HTTPException(status_code=400, detail='Мындай шаар бар')

    city_db.city_name = city.city_name
    city_db.city_image = city.city_image

    db.commit()
    db.refresh(city_db)
    return {'message': 'Шаар озгорулду'}


@city_router.delete('/{city_id}/', response_model=dict)
async def delete_city(
    city_id: int, db: Session = Depends(get_db)):
    city_db = (db.query(City).filter(City.id == city_id).first())

    if not city_db:
        raise HTTPException(status_code=404, detail='Мындай шаар жок')

    db.delete(city_db)
    db.commit()

    return {'message': 'Шаар очурулду'}