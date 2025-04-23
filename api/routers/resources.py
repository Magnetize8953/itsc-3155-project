from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import engine, get_db


router = APIRouter(
    tags=['Resources'],
    prefix="/resources"
)


@router.get("/", response_model=list[schema.Resource])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Resource)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=schema.Resource)
def create(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_resource(resource_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, resource_id)

@router.put("/{item_id}", response_model=schema.Resource)
def update(item_id: int, request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)