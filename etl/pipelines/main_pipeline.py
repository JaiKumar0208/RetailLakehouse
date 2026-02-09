import sys

from etl.utils.etl_logging import setup_logger
from ServiceLayer.database import SessionLocal
from ServiceLayer.etl.etl_run_log_service import ETLRunLogService
from ServiceLayer.etl.etl_step_run_log_service import ETLStepRunLogService

from etl.load.Dim import *
from etl.load.Fact import *
from etl.transform import *
from etl.extract import *


logger = setup_logger()

db = SessionLocal()

def run_extract_step(step_name, function, run_id):
    """Run a pipeline step with logging + error handling"""

    run = ETLRunLogService.start_run(db, 'EXTRACT_PIPELINE')
    step = ETLStepRunLogService.start_step(db, run_id, step_name)
    try:
        logger.info(f"Starting: {step_name}")
        records = function(db)
        ETLRunLogService.complete_run(db, run.RunID)
        ETLStepRunLogService.complete_step(db, step.StepRunID, records)
        logger.info(f"Completed: {step_name}\n")
    except Exception as e:
        ETLRunLogService.fail_run(db, run.RunID, str(e))
        ETLStepRunLogService.fail_step(db, step.StepRunID, str(e))
        logger.error(f"Failed: {step_name}")
        logger.exception(f"Error Details: {str(e)}")
        raise

def run_transform_load_step(step_name, function, run_id):
    """Run a pipeline step with logging + error handling"""
    run = ETLRunLogService.start_run(db, 'TRANSFORM_PIPELINE')
    step = ETLStepRunLogService.start_step(db, run_id, step_name)
    try:
        logger.info(f"Starting: {step_name}")
        records = function()
        ETLRunLogService.complete_run(db, run.RunID)
        ETLStepRunLogService.complete_step(db, step.StepRunID, records)
        logger.info(f"Completed: {step_name}\n")
    except Exception as e:
        ETLRunLogService.fail_run(db, run.RunID, str(e))
        ETLStepRunLogService.fail_step(db, step.StepRunID, str(e))
        logger.error(f"Failed: {step_name}")
        logger.exception(f"Error Details: {str(e)}")
        raise

def run_extract_pipeline():
    logger.info("RetailLakehouse Pipeline Started\n")

    run = ETLRunLogService.start_run(db, "EXTRACT_PIPELINE")

    run_extract_step("extract_inventory_movements_to_parquet", extract_inventory_movements_to_parquet, run.RunID)
    run_extract_step("extract_master_data", extract_master_data, run.RunID)
    run_extract_step("extract_payment_to_parquet", extract_payment_to_parquet, run.RunID)
    run_extract_step("extract_purchase_orders_to_parquet", extract_purchase_orders_to_parquet, run.RunID)
    run_extract_step("extract_sales_return_to_parquet", extract_sales_return_to_parquet, run.RunID)
    run_extract_step("extract_sales_transaction_to_parquet", extract_sales_transaction_to_parquet, run.RunID)

    logger.info("Pipeline Finished Successfully!")


def run_transform_load_pipeline():
    logger.info("RetailLakehouse Pipeline Started\n")
    run = ETLRunLogService.start_run(db, "TRASFORM_PIPELINE")
    # Transform
    run_transform_load_step(transform_sales_data, transform_sales_data, run.RunID)
    run_transform_load_step("transform_purchase_data", transform_purchase_data, run.RunID)
    run_transform_load_step("transform_inventory_movement_data", transform_inventory_movement_data, run.RunID)
    run_transform_load_step("transform_sales_return_data", transform_sales_return_data, run.RunID)
    run_transform_load_step("transform_payment_data", transform_payment_data, run.RunID)
    run_transform_load_step("transform_calendar_data", transform_calendar_data, run.RunID)
    run_transform_load_step("transform_category_data", transform_category_data, run.RunID)
    run_transform_load_step("transform_product_data", transform_product_data, run.RunID)
    run_transform_load_step("transform_store_data", transform_store_data, run.RunID)
    run_transform_load_step("transform_supplier_data", transform_supplier_data, run.RunID)
    run_transform_load_step("transform_customer_data", transform_customer_data, run.RunID)
    run_transform_load_step("transform_employee_data", transform_employee_data, run.RunID)

    # Load
    run_load = ETLRunLogService.start_run(db, "LOAD_PIPELINE")
    run_transform_load_step("build_dim_product", build_dim_product, run_load.RunID)
    run_transform_load_step("build_dim_customers", build_dim_customers, run_load.RunID)
    run_transform_load_step("build_dim_calendar", build_dim_calendar, run_load.RunID)
    run_transform_load_step("build_dim_supplier", build_dim_supplier, run_load.RunID)
    run_transform_load_step("build_dim_Category", build_dim_Category, run_load.RunID)
    run_transform_load_step("build_dim_store", build_dim_store, run_load.RunID)
    run_transform_load_step("build_dim_employee", build_dim_employee, run_load.RunID)
    run_transform_load_step("build_fact_category_performance", build_fact_category_performance, run_load.RunID)
    run_transform_load_step("build_fact_customer_summary", build_fact_customer_summary, run_load.RunID)
    run_transform_load_step("build_fact_daily_kpis", build_fact_daily_kpis, run_load.RunID)
    run_transform_load_step("build_fact_inventory_snapshot", build_fact_inventory_snapshot, run_load.RunID)
    run_transform_load_step("build_fact_payment_summary", build_fact_payment_summary, run_load.RunID)
    run_transform_load_step("build_fact_product_performance", build_fact_product_performance, run_load.RunID)
    run_transform_load_step("build_gold_sales_summary", build_gold_sales_summary, run_load.RunID)
    run_transform_load_step("build_fact_store_performance", build_fact_store_performance, run_load.RunID)



    logger.info("Pipeline Finished Successfully!")


if __name__ == "__main__":
    try:
        run_extract_pipeline()
        run_transform_load_pipeline()
    except Exception:
        logger.critical("PIPELINE STOPPED DUE TO ERROR")
        sys.exit(1)
