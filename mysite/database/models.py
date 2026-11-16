from .db import Base
from sqlalchemy import (String, Integer, Enum, Date, ForeignKey, DateTime,
    Text, Boolean, Numeric)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from enum import Enum as PyEnum


class StatusChoices(str, PyEnum):
    buyer = 'buyer'
    seller = 'seller'
    manager = 'manager'
    courier = 'courier'

class OrderStatus(str, PyEnum):
    pending = 'pending'
    delivered = 'delivered'
    cancelled = 'cancelled'

class UserProfile(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.buyer)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user', cascade="all, delete-orphan")
    user_reviews: Mapped[List['Review']] = relationship(back_populates='review_user', cascade="all, delete-orphan")
    user_orders: Mapped[List['Order']] = relationship(back_populates='order_user', cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(64), unique=True)

    category_stores: Mapped[List['Store']] = relationship(back_populates='store_category', cascade="all, delete-orphan")


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    store_category: Mapped[Category] = relationship(Category, back_populates='category_stores')
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    store_products: Mapped[List['Product']] = relationship(back_populates='product_store', cascade="all, delete-orphan")
    store_reviews: Mapped[List['Review']] = relationship(back_populates='review_store', cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    product_store: Mapped[Store] = relationship(Store, back_populates='store_products')
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_original: Mapped[bool] = mapped_column(Boolean, default=True)
    create_date: Mapped[date] = mapped_column(Date, default=date.today)

    product_orders: Mapped[List['Order']] = relationship(back_populates='order_product')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    review_store: Mapped[Store] = relationship(Store, back_populates='store_reviews')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    review_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_reviews')
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    city_name: Mapped[str] = mapped_column(String(64), unique=True)
    city_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    city_orders: Mapped[List['Order']] = relationship(back_populates='order_city')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    order_product: Mapped[Product] = relationship(Product, back_populates='product_orders')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    order_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_orders')
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    order_city: Mapped[City] = relationship(City, back_populates='city_orders')
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    order_status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)