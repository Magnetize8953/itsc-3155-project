from . import orders, menu


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(menu.router)
