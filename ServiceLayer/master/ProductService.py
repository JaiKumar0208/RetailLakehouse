from typing import Optional, List
from sqlalchemy.orm import Session
from models.master.Product import Product
from datetime import datetime

class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        product_name: str,
        category: str,
        sub_category: str,
        price
    ) -> Product:
        """Create a new product"""
        product = Product(
            product_name=product_name,
            category=category,
            sub_category=sub_category,
            price=price
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_by_id_product(db: Session, product_id: int) -> Optional[Product]:
        """Get a product by its ID"""
        return db.query(Product).filter(Product.product_id == product_id).first()

    @staticmethod
    def get_all_product(db: Session) -> List[Product]:
        """Get all products"""
        return db.query(Product).all()

    @staticmethod
    def get_by_category_product(db: Session, category: str) -> List[Product]:
        """Get products by category"""
        return db.query(Product).filter(Product.category == category).all()

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_name: str = None,
        category: str = None,
        sub_category: str = None,
        price=None
    ) -> Optional[Product]:
        """Update product details"""
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return None

        if product_name is not None:
            product.product_name = product_name
        if category is not None:
            product.category = category
        if sub_category is not None:
            product.sub_category = sub_category
        if price is not None:
            product.price = price

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Delete a product"""
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return False

        db.delete(product)
        db.commit()
        return True

    @staticmethod
    def soft_delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.deleted_at = datetime.now()
            db.commit()
