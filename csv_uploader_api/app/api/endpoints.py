from fastapi import (
    APIRouter, UploadFile, File, Depends, HTTPException,
    status, Query, Body
)
from fastapi.responses import PlainTextResponse, Response
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.data import Data
from app.schemas.data import DataOut
from sqlalchemy.orm import Session
import pandas as pd
from typing import List
from app.core.config import LOG_FILE

router = APIRouter()

@router.post("/upload", dependencies=[Depends(get_current_user)], status_code=201)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    df = pd.read_csv(file.file)
    if df.isnull().any().any():
        raise HTTPException(status_code=400, detail="CSV contains missing values.")
    expected_columns = {'name': str, 'age': int}
    for col, typ in expected_columns.items():
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Missing column: {col}")
        if not df[col].map(lambda x: isinstance(x, typ)).all():
            raise HTTPException(status_code=400, detail=f"Incorrect type in column: {col}")
    for _, row in df.iterrows():
        db_obj = Data(name=row['name'], age=row['age'])
        db.add(db_obj)
    db.commit()
    return {"message": "CSV uploaded and data stored successfully."}

@router.get("/data", response_model=List[DataOut], dependencies=[Depends(get_current_user)])
def get_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Data).offset(skip).limit(limit).all()

@router.get("/data/search", response_model=List[DataOut], dependencies=[Depends(get_current_user)])
def search_data(
    name: str = Query(None, description="Filter by name substring"),
    min_age: int = Query(None, description="Minimum age filter"),
    max_age: int = Query(None, description="Maximum age filter"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Data)
    if name:
        query = query.filter(Data.name.contains(name))
    if min_age is not None:
        query = query.filter(Data.age >= min_age)
    if max_age is not None:
        query = query.filter(Data.age <= max_age)
    return query.offset(skip).limit(limit).all()

@router.delete("/data/{data_id}", dependencies=[Depends(get_current_user)])
def delete_data(data_id: int, db: Session = Depends(get_db)):
    obj = db.query(Data).filter(Data.id == data_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(obj)
    db.commit()
    return {"message": f"Data with id {data_id} deleted successfully."}

@router.get("/logs", response_class=PlainTextResponse, dependencies=[Depends(get_current_user)])
def get_logs():
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read()
        return Response(content=content, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading log file: {str(e)}")
