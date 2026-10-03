from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional


def create_advertisement(db: Session, ad: schemas.AdvertisementCreate) -> models.Advertisement:
    db_ad = models.Advertisement(**ad.model_dump())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad


def get_advertisement(db: Session, advertisement_id: int) -> Optional[models.Advertisement]:
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()


def search_advertisements(
    db: Session,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    author: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Advertisement]:
    query = db.query(models.Advertisement)

    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(models.Advertisement.description.ilike(f"%{description}%"))
    if author:
        query = query.filter(models.Advertisement.author.ilike(f"%{author}%"))
    if price_min is not None:
        query = query.filter(models.Advertisement.price >= price_min)
    if price_max is not None:
        query = query.filter(models.Advertisement.price <= price_max)

    return query.order_by(models.Advertisement.created_at.desc()).offset(skip).limit(limit).all()


def update_advertisement(
    db: Session, advertisement_id: int, ad: schemas.AdvertisementUpdate
) -> Optional[models.Advertisement]:
    db_ad = get_advertisement(db, advertisement_id)
    if not db_ad:
        return None
    update_data = ad.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ad, key, value)
    db.commit()
    db.refresh(db_ad)
    return db_ad


def delete_advertisement(db: Session, advertisement_id: int) -> bool:
    db_ad = get_advertisement(db, advertisement_id)
    if not db_ad:
        return False
    db.delete(db_ad)
    db.commit()
    return True