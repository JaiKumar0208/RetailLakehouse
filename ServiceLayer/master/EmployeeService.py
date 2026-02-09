from sqlalchemy.orm import Session
from models.master.Employee import Employee
from typing import Optional
from datetime import datetime

class EmployeeService:

    @staticmethod
    def create_employee(
            db: Session,
            employee_name: str,
            store_id: int,
            salary: int,
            dob
    ) -> Employee:
        """Create a new employee record"""
        employee = Employee(
            employee_name=employee_name,
            store_id=store_id,
            salary=salary,
            dob=dob
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    @staticmethod
    def get_by_id_employee(db: Session, employee_id: int) -> Employee | None:
        """Get a single employee by ID"""
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()

    @staticmethod
    def get_all_employee(db: Session):
        """Get all employees"""
        return db.query(Employee).all()

    @staticmethod
    def get_by_store_employee(db: Session, store_id: int):
        """Get all employees for a specific store"""
        return db.query(Employee).filter(Employee.store_id == store_id).all()

    @staticmethod
    def update_employee(
            db: Session,
            employee_id: int,
            employee_name: str = None,
            store_id: int = None,
            salary: int = None,
            dob=None
    ) -> Optional[Employee]:

        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not employee:
            return None

        if employee_name is not None:
            employee.employee_name = employee_name
        if store_id is not None:
            employee.store_id = store_id
        if salary is not None:
            employee.salary = salary
        if dob is not None:
            employee.dob = dob

        db.commit()
        db.refresh(employee)
        return employee

    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        """Delete an employee"""
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not employee:
            return False

        db.delete(employee)
        db.commit()
        return True

    @staticmethod
    def soft_delete_employee(db: Session, employee_id: int):
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            employee.deleted_at = datetime.now()
            db.commit()




