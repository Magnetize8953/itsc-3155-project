from . import orders, menu, customers


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(menu.router)
    app.include_router(customers.router)
