from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as order_model, menu as menu_model, promotions as promo_model, customers as customer_model, resources as resource_model
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json, decimal

#still need to update payment info and declining balance subtraction
def create(db: Session, request):
    new_item = order_model.Order(
        status=request.status,
        customer_id=request.customer_id,
        items=request.items,
        promo=request.promo
    )

    #get all menu items
    menu_list = [i[0] for i in db.query(menu_model.Menu.name).all()]
    #change the string given to a json
    try:
        json_menu = json.loads(new_item.items)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON given for Menu")
    #check each item is an existing menu item
    for key in json_menu:
        if key not in menu_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item not found: {key}")

    new_item.total = 0.0

    for key in json_menu:
        #getting the menu item
        menu_item = db.query(menu_model.Menu).filter(menu_model.Menu.name == key).first()
        menu_item_resources = json.loads(menu_item.resources)
        for innerkey in menu_item_resources:
            #reducing resource
            resource = db.query(resource_model.Resource).filter(resource_model.Resource.name == innerkey).first()
            resource.amount -= menu_item_resources[innerkey] * json_menu[key]

        #set the total
        cost = menu_item.cost
        new_item.total += float(cost) * json_menu[key]

    # promotions
    all_promotions = db.query(promo_model.Promotion).all()
    for promotion in all_promotions:
        if new_item.promo == promotion.code:
            if promotion.expire_date > datetime.now():
                new_item.total = float(new_item.total) * (1 - (int(promotion.discount) / 100))

    #add total to customer account
    try:
        customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == request.customer_id).first()
        customer.amount_owed += decimal.Decimal(new_item.total)
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

def read_by_status(db: Session, status):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.status == status).all()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def read_by_date(db: Session, begin_date, end_date):
    try:
        item_list = db.query(order_model.Order).filter(order_model.Order.date >= begin_date).filter(order_model.Order.date <= end_date).all()
        if not item_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found in that date range!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item_list


def update(db: Session, item_id, request):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        item = item.first()
        item.date = datetime.now()
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    # try:
    #     item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
    #     if not item.first():
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    #     item.delete(synchronize_session=False)
    #     db.commit()
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    try:
        #find the item
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item = item.first()

        #change the status
        item.status = "cancelled"

        #load the json
        try:
            json_menu = json.loads(item.items)
        except json.decoder.JSONDecodeError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON given for Menu")

        #update resources
        for key in json_menu:
            # getting the menu item
            menu_item = db.query(menu_model.Menu).filter(menu_model.Menu.name == key).first()
            menu_item_resources = json.loads(menu_item.resources)
            for innerkey in menu_item_resources:
                # reducing resource
                resource = db.query(resource_model.Resource).filter(resource_model.Resource.name == innerkey).first()
                resource.amount += json_menu[key]

        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_202_ACCEPTED)
