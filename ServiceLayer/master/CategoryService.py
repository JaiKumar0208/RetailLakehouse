from ServiceLayer.database import SessionLocal
from models.master.Category  import Category
from datetime import datetime


class CategoryService:

    @staticmethod
    def create_category(category_name, description):
        session = SessionLocal()
        category = Category(category_name= category_name, description = description)
        session.add(category)
        session.commit()
        session.close()

    @staticmethod
    def get_all_category():
        session = SessionLocal()
        data = session.query(Category).all()
        session.close()
        return data

    @staticmethod
    def update_category(category_id, name, description):
        session = SessionLocal()
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category:
            category.name = name
            category.description = description
            session.commit()
        session.close()

    @staticmethod
    def delete_category(category_id):
        session = SessionLocal()
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category:
            session.delete(category)
            session.commit()
        session.close()

    @staticmethod
    def soft_delete_category(category_id: int):
        session = SessionLocal()
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category:
            category.deleted_at = datetime.now()
            session.commit()
