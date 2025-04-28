from . import orders, resources, customers, payments, reviews, menu, promotions, restaurant
from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    menu.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    restaurant.Base.metadata.create_all(engine)
