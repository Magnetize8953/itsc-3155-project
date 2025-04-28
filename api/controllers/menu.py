from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import menu as menu_model, resources as resources_model
from sqlalchemy.exc import SQLAlchemyError
import json

def create(db: Session, request):
    new_item = menu_model.Menu(
        name=request.name,
        cost=request.cost,
        calories=request.calories,
        category=request.category,
        resources=request.resources
    )


    try:
        json_resources = json.loads(new_item.resources)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON given for Resources")

    resource_list = [i[0] for i in db.query(resources_model.Resource.name).all()]
    print(resource_list)
    for key in json_resources:
        print(key)
        if key not in resource_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource not found: {key}")

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
        result = db.query(menu_model.Menu).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(menu_model.Menu).filter(menu_model.Menu.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id, request):
    try:
        item = db.query(menu_model.Menu).filter(menu_model.Menu.id == item_id)
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
        item = db.query(menu_model.Menu).filter(menu_model.Menu.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)