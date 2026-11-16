from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_password_hash
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/users', tags=['UserProfile'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy.exc import IntegrityError


@user_router.post('/create/', response_model=UserProfileOutSchema)
def user_create(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    if db.query(UserProfile).filter(UserProfile.username == user.username).first():
        raise HTTPException(status_code=400, detail='Такой username уже существует')

    if db.query(UserProfile).filter(UserProfile.email == user.email).first():
        raise HTTPException(status_code=400, detail='Такой email уже существует')

    user_data = user.model_dump()
    user_data['password'] = get_password_hash(user_data['password'])
    user_db = UserProfile(**user_data)
    db.add(user_db)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Пользователь уже существует')

    db.refresh(user_db)
    return user_db


@user_router.get('/', response_model=List[UserProfileOutSchema])
def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=404)
    return user_db


@user_router.put('/{user_id}', response_model=dict)
def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Мындай маалымат жок')

    user_data = user.model_dump()
    user_data['password'] = get_password_hash(user_data['password'])

    for key, value in user_data.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Профайл озгорулду'}


@user_router.delete('/{user_id}/', response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Мындай профайл жок')

    db.delete(user_db)
    db.commit()
    return {'message': 'Профайл удалена'}