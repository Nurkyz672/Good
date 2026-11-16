from .views import (UserProfileAdmin, RefreshTokenAdmin, CategoryAdmin, StoreAdmin,
                    ProductAdmin, ReviewAdmin, CityAdmin, OrderAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(myproject: FastAPI):
    admin = Admin(myproject, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(OrderAdmin)