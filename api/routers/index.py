from . import orders, menu, customers, resources, reviews, restaurant


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(menu.router)
    app.include_router(customers.router)
    app.include_router(resources.router)
    app.include_router(restaurant.router)
    app.include_router(reviews.router)
