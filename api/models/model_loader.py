# TODO: remove unnecessary imports
from . import orders, order_details, recipes, sandwiches, resources
from . import customers, payments, reviews
from ..dependencies.database import engine


def index():
    # given in skeleton
    # TODO: remove unnecessary creations
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)

    customers.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
