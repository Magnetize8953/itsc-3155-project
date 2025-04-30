from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import resources as model
from ..models.promotions import Promotion as ModelPromotion
from ..schemas.promotions import Promotion as SchemaPromotion, PromotionCreate, PromotionUpdate

def read_all(db: Session):
    try:
        return db.query(ModelPromotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def create(db: Session, request):
    new_promo = model.Promotion(
        id=request.id,
        code=request.code,
        expire_date=request.expire_date,
        discount=request.discount,
    )
    try:
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error)
    return new_promo


def update(db: Session, promo_id: int, request: PromotionUpdate):
    try:
        promo_query = db.query(ModelPromotion).filter(ModelPromotion.id == promo_id)
        if not promo_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        update_data = request.dict(exclude_unset=True)
        promo_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promo_query.first()


def delete(db: Session, promo_id: int):
    try:
        promo_query = db.query(ModelPromotion).filter(ModelPromotion.id == promo_id)
        if not promo_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        promo_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)