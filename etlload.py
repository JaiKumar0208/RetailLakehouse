from etl.load.build_fact_dimensions import build_gold_sales_model
from etl.load.Dim import *
from etl.load.Fact import *


def main():
    try:
        build_dim_product()
        build_dim_customers()
        build_dim_calendar()
        build_dim_supplier()
        build_dim_Category()
        build_dim_store()
        build_dim_employee()

        build_fact_category_performance()
        build_fact_customer_summary()
        build_fact_daily_kpis()
        build_fact_inventory_snapshot()
        build_fact_payment_summary()
        build_fact_product_performance()
        build_gold_sales_summary()
        build_fact_store_performance()
        print("✅ Load completed successfully!")
    except Exception as e:
        print("❌ Error during transform:", e)



if __name__ == "__main__":
    main()