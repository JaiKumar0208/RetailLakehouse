from ServiceLayer.database import SessionLocal
from models.master.Customer import Customer
from datetime import datetime


class CustomerService:

    @staticmethod
    def create_customer(first_name, last_name, gender, city, signup_date):
        session = SessionLocal()
        customer = Customer(first_name=first_name
                            , last_name=last_name
                            , gender= gender
                            , city=city
                            , signup_date=signup_date
                            )
        session.add(customer)
        session.commit()
        session.close()

    @staticmethod
    def get_all_customer():
        session = SessionLocal()
        data = session.query(Customer).all()
        session.close()
        return data

    @staticmethod
    def update_customer(customer_id,first_name, last_name, gender, city, signup_date):
        session = SessionLocal()
        customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer:
            customer.first_name = first_name
            customer.last_name = last_name
            customer.gender = gender
            customer.city = city
            customer.signup_date = signup_date
            session.commit()
        session.close()

    @staticmethod
    def delete_customer(customer_id):
        session = SessionLocal()
        customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
        session.close()

    @staticmethod
    def soft_delete_customer(customer_id: int):
        session = SessionLocal()
        customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer:
            customer.deleted_at = datetime.now()
            session.commit()