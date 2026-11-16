from sqladmin import ModelView
from mysite.database.models import (
    UserProfile, RefreshToken, Category, Store, Product, Review, City, Order)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.last_name,
                   UserProfile.username, UserProfile.email, UserProfile.status,
                   UserProfile.created_date]
    column_searchable_list = [UserProfile.username, UserProfile.email]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_date]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    column_searchable_list = [Category.category_name]


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name, Store.category_id, Store.store_image]
    column_searchable_list = [Store.store_name]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.store_id, Product.price,
                   Product.is_original, Product.create_date]
    column_searchable_list = [Product.product_name]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.store_id, Review.user_id, Review.stars,
                   Review.text, Review.created_date]


class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.city_name, City.city_image]
    column_searchable_list = [City.city_name]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id, Order.product_id, Order.city_id,
                   Order.quantity, Order.total_price, Order.order_status, Order.created_date]