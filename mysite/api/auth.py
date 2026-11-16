from fastapi import APIRouter, HTTPException, Depends, status
from mysite.database.models import UserProfile, RefreshToken
from mysite.database.schema import CurrentUserSchema, UserProfileInputSchema, UserProfileLoginSchema,UserProfileMeSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from mysite.config import (
    SECRET_KEY, ALGORITHM,
    ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
)
from datetime import timedelta, datetime
from typing import Optional, Annotated
from jose import jwt, JWTError


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


auth_router = APIRouter(prefix='/auth', tags=['Authorization'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))




def get_token_data(user: UserProfile):
    return {'sub': str(user.id), 'username': user.username}


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserProfile).filter(UserProfile.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@auth_router.post('/login/', response_model=dict)
async def login(user: UserProfileLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмес', status_code=401)

    token_data = get_token_data(user_db)

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Мындай username же email бар экен', status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=hash_password
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Сиз ийгиликтуу регистрация болдунуз'}


@auth_router.post('/logout/', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()

    return {'message': "Ийгиликтуу чыгып кеттиниз"}


from fastapi import Body

@auth_router.post('/refresh/', response_model=dict)
async def refresh(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    user_db = stored_token.token_user
    token_data = get_token_data(user_db)

    access_token = create_access_token(token_data)

    return {'access_token': access_token, 'token_type': 'Bearer'}

@auth_router.get('/verify/', response_model=CurrentUserSchema)
async def verify_access_token(current_user: UserProfile = Depends(get_current_user)):
    return current_user


@auth_router.get('/me/', response_model=UserProfileMeSchema)
async def get_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user

from mysite.database.schema import UserProfileUpdateSchema




@auth_router.put('/me/update/', response_model=UserProfileMeSchema)
async def update_me(
    data: UserProfileUpdateSchema,
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    update_data = data.dict(exclude_unset=True)

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@auth_router.delete('/me/delete/', response_model=dict)
async def delete_me(
    current_user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(RefreshToken).filter(RefreshToken.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()

    return {'message': 'Аккаунт ийгиликтуу очурулду'}