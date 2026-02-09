from ServiceLayer.master.CategoryService import CategoryService
from ServiceLayer.master.CustomerService import CustomerService
from ServiceLayer.master.EmployeeService import EmployeeService
from ServiceLayer.master.ProductService import ProductService
from ServiceLayer.master.StoreService import StoreService
from ServiceLayer.master.SupplierService import SupplierService
from ServiceLayer.database import SessionLocal

def seed_master_data():
    session = SessionLocal()
    try:
        CategoryService.create_category(category_name="Category 1", description="this is the best category" )
        CategoryService.create_category( category_name="Category 2", description="this is the 2nd best category" )

        CustomerService.create_customer( first_name="Manoj Kumar "
                        , last_name="Singh"
                        , gender ="Male"
                        , city ="Bangalore"
                        , signup_date="2020-09-22"
                        )
        CustomerService.create_customer( first_name="Chandan Kumar"
                    , last_name="Yadav"
                    , gender="Male"
                    , city="New Delhi"
                    , signup_date="2020-09-22"
                    )
        StoreService.create_store(session
                     , store_name="Store 1"
                     , city="New Delhi"
                     , state="New Delhi"
                     , open_date="2020-09-22"
                     )
        StoreService.create_store(session
                                  , store_name="Store 1"
                                  , city="New Delhi"
                                  , state="New Delhi"
                                  , open_date="2020-09-22"
                                  )
        SupplierService.create_supplier(session, supplier_name="Supplier 1", city="new delhi")
        SupplierService.create_supplier(session, supplier_name="TVS Ltd.", city="Noida")

        EmployeeService.create_employee(session
                        , employee_name="Chandan Kumar"
                        , store_id = 1
                        , salary =234561
                        , dob="2020-09-22")
        EmployeeService.create_employee(session
                        , employee_name="Chandan Kumar"
                        , store_id=1
                        , salary=234561
                        , dob="2020-09-22"
                        )
        ProductService.create_product(session
                       , product_name ="Telivision"
                       , category = "Electronics"
                       , sub_category ="TV"
                       , price = 1500
                       )
        ProductService.create_product(session
                       , product_name="Mobile Phone"
                       , category="Phone"
                       , sub_category="Mobile"
                       , price=25000
                       )



        session.commit()
        print("✅ Master data seeded successfully!")

    except Exception as e:
        session.rollback()
        print("❌ Error seeding master data:", e)

    finally:
        session.close()

if __name__ == "__main__":
    seed_master_data()


