from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from .models import StatusChoices, OrderStatus

class UserProfileRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    status: StatusChoices


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


class UserProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[StatusChoices] = None


class UserProfileOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    status: StatusChoices
    created_date: date


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    status: StatusChoices


class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    status: StatusChoices


class UserProfileMeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    username: str
    email: str
    status: StatusChoices

class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str


class CityInputSchema(BaseModel):
    city_name: str
    city_image: Optional[str] = None


class CityOutSchema(BaseModel):
    id: int
    city_name: str
    city_image: Optional[str] = None


class StoreInputSchema(BaseModel):
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class StoreOutSchema(BaseModel):
    id: int
    store_name: str
    category_id: int
    store_image: Optional[str] = None


class ProductInputSchema(BaseModel):
    store_id: int
    product_name: str
    price: Decimal = Field(gt=0)
    description: Optional[str] = None
    is_original: bool = True


class ProductOutSchema(BaseModel):
    id: int
    store_id: int
    product_name: str
    price: Decimal
    description: Optional[str] = None
    is_original: bool
    create_date: date


class ReviewInputSchema(BaseModel):
    store_id: int
    text: Optional[str] = None
    stars: int = Field(ge=1, le=5)


class ReviewOutSchema(BaseModel):
    id: int
    store_id: int
    user_id: int
    text: Optional[str] = None
    stars: int
    created_date: datetime


class OrderInputSchema(BaseModel):
    user_id: int
    product_id: int
    city_id: int
    quantity: int = Field(default=1, ge=1)


class OrderOutSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    city_id: int
    quantity: int
    total_price: Decimal
    order_status: OrderStatus
    created_date: datetime


class SearchInputSchema(BaseModel):
    question: str = Field(min_length=2, max_length=500)


class SearchOutputSchema(BaseModel):
    answer: str
    items: list[dict] = []