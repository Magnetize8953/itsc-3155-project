from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import employees as model
from sqlalchemy.exc import SQLAlchemyError


def read_all(db: Session):
    try:
        return db.query(model.Employee).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )

def read_one(db: Session, item_id):
    try:
        item = db.query(model.Employee).filter(model.Employee.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def create(db: Session, request):
    new_item = model.Employee(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address,
        hours_worked=request.hours_worked
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error)
    return new_item


def delete(db: Session, item_id: int):
    try:
        query = db.query(model.Employee).filter(model.Employee.id == item_id)
        if not query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee not found")
        query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error)

def update(db: Session, item_id, request):
    try:
        item = db.query(model.Employee).filter(model.Employee.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()
