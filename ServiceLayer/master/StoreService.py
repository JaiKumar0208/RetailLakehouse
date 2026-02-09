from typing import Optional, List
from sqlalchemy.orm import Session
from models.master.Store import Store
from datetime import datetime

class StoreService:

    @staticmethod
    def create_store(
        db: Session,
        store_name: str,
        city: str = None,
        state: str = None,
        open_date=None
    ) -> Store:
        """Create a new store"""
        store = Store(
            store_name=store_name,
            city=city,
            state=state,
            open_date=open_date
        )
        db.add(store)
        db.commit()
        db.refresh(store)
        return store

    @staticmethod
    def get_by_id_store(db: Session, store_id: int) -> Optional[Store]:
        """Get a store by ID"""
        return db.query(Store).filter(Store.store_id == store_id).first()

    @staticmethod
    def get_all_store(db: Session) -> List[Store]:
        """Get all stores"""
        return db.query(Store).all()

    @staticmethod
    def get_by_city_store(db: Session, city: str) -> List[Store]:
        """Get stores in a specific city"""
        return db.query(Store).filter(Store.city == city).all()

    @staticmethod
    def update_store(
        db: Session,
        store_id: int,
        store_name: str = None,
        city: str = None,
        state: str = None,
        open_date=None
    ) -> Optional[Store]:
        """Update store details"""
        store = db.query(Store).filter(Store.store_id == store_id).first()
        if not store:
            return None

        if store_name is not None:
            store.store_name = store_name
        if city is not None:
            store.city = city
        if state is not None:
            store.state = state
        if open_date is not None:
            store.open_date = open_date

        db.commit()
        db.refresh(store)
        return store

    @staticmethod
    def delete_store(db: Session, store_id: int) -> bool:
        """Delete a store"""
        store = db.query(Store).filter(Store.store_id == store_id).first()
        if not store:
            return False

        db.delete(store)
        db.commit()
        return True

    @staticmethod
    def soft_delete_product(db: Session, store_id: int):
        store = db.query(Store).filter(Store.store_id == store_id).first()
        if store:
            store.deleted_at = datetime.now()
            db.commit()
