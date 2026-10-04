from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database import engine, get_db, Base
from app import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advertisement Service", version="1.0.0")


@app.post("/advertisement", response_model=schemas.AdvertisementResponse, status_code=201)
def create_advertisement(ad: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.create_advertisement(db, ad)


@app.get("/advertisement", response_model=list[schemas.AdvertisementResponse])
def search_advertisements(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None, ge=0),
    price_max: Optional[float] = Query(None, ge=0),
    author: Optional[str] = Query(None),
    created_at_from: Optional[datetime] = Query(
        None,
        description="Дата создания 'от' (включительно). ISO-формат, например 2026-10-01T00:00:00Z",
    ),
    created_at_to: Optional[datetime] = Query(
        None,
        description="Дата создания 'до' (включительно). ISO-формат, например 2026-10-05T23:59:59Z",
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.search_advertisements(
        db,
        title=title,
        description=description,
        price_min=price_min,
        price_max=price_max,
        author=author,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        skip=skip,
        limit=limit,
    )


@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    ad = crud.get_advertisement(db, advertisement_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementResponse)
def update_advertisement(
    advertisement_id: int, ad: schemas.AdvertisementUpdate, db: Session = Depends(get_db)
):
    updated = crud.update_advertisement(db, advertisement_id, ad)
    if not updated:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return updated


@app.delete("/advertisement/{advertisement_id}", status_code=204)
def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    if not crud.delete_advertisement(db, advertisement_id):
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return None