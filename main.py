from fastapi import FastAPI
import uvicorn
from mysite.api import users, auth, category, city, store, product, review, order,ai


glovo_app = FastAPI(title='GoodLogistic')
glovo_app.include_router(users.user_router)
glovo_app.include_router(auth.auth_router)
glovo_app.include_router(category.category_router)
glovo_app.include_router(city.city_router)
glovo_app.include_router(store.store_router)
glovo_app.include_router(product.product_router)
glovo_app.include_router(review.review_router)
glovo_app.include_router(order.order_router)
glovo_app.include_router(ai.ai_router)


if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8000)