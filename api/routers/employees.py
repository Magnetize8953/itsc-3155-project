from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import employees as controller
from ..schemas import employees as schema
from ..dependencies.database import engine, get_db


router = APIRouter(
    tags=['Employees'],
    prefix="/employees"
)


@router.get("/", response_model=list[schema.Employee])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Employee)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.post("/", response_model=schema.Employee)
def create(request: schema.EmployeeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_employee(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)

@router.put("/{item_id}", response_model=schema.Employee)
def update(item_id: int, request: schema.EmployeeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)