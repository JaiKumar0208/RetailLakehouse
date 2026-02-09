from etl.transform.transformSalesTransaction import transform_sales_data
from etl.transform.transformPurchaseOrder import transform_purchase_data
from etl.transform.transformInventoryMovement import transform_inventory_movement_data
from etl.transform.transformSalesReturn import transform_sales_return_data
from etl.transform.tranformPayment import  transform_payment_data

from etl.transform.transformCalendar import transform_calendar_data
from etl.transform.transformCategory  import transform_category_data
from etl.transform.transformCustomer  import transform_customer_data
from etl.transform.transformEmployee  import transform_employee_data
from etl.transform.transformProduct import transform_product_data
from etl.transform.transformStore  import transform_store_data
from etl.transform.transformSupplier  import transform_supplier_data


def main():
    try:
        transform_sales_data()
        transform_purchase_data()
        transform_inventory_movement_data()
        transform_sales_return_data()
        transform_payment_data()
        transform_calendar_data()
        transform_category_data()
        transform_product_data()
        transform_store_data()
        transform_supplier_data()
        transform_customer_data()
        transform_employee_data()
        print("✅ Transform completed successfully!")
    except Exception as e:
        print("❌ Error during transform:", e)


if __name__ == "__main__":
    main()
