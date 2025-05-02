from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as order_model, menu as menu_model, promotions as promo_model, customers as customer_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

#still need to update payment info and declining balance subtraction
def create(db: Session, request):
    new_item = order_model.Order(
        status=request.status,
        customer_id=request.customer_id,
        items=request.items,
        promo=request.promo
    )

    # promotions
    all_promotions = db.query(promo_model.Promotion).all()
    for promotion in all_promotions:
        if new_item.promo == promotion.code:
            if promotion.expire_date > datetime.now():
                new_item.total = new_item.total * (1 + (promotion.discount / 100))

    #get all menu items
    menu_items = db.query(menu_model.Menu.name).all()
    #change the string given to a json
    try:
        json_menu = json.loads(new_item.items)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON given for Menu")
    #check each item is an existing menu item
    for key in json_menu:
        if key not in menu_items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item not found: {key}")
    #set the total
    for key in json_menu:
        cost = db.query(menu_model.Menu.cost).filter(menu_model.Menu.name == key)
        new_item.total += float(cost) * json_menu[key]

    #add total to customer account
    try:
        customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == request.customer_id).first()
        customer.amount_owed += new_item.total
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    #add to database
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
