import pymysql
from dagster import Definitions, ScheduleDefinition, asset, define_asset_job
import logging

logger = logging.getLogger()


@asset
def transfer_data_api_calls(context):
    # Database connection parameters
    db_config = {
        "host": "mysql_db_analytics",
        "user": "admin_analytics",
        "password": "password_analytics",
        "database": "analytics",
    }

    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:

            # TODO: date is hardcoded but should be modified so that it takes last day or last week for example
            select_query = "SELECT customer_id, member_id, member_dob, timestamp FROM coverage_raw where timestamp > '2023-03-01'"

            cursor.execute(select_query)

            rows = cursor.fetchall()
            context.log.info("Show rows")
            context.log.info(rows)

            # Upsert is necessary to have idempotency
            # This is achieved with INSERT IGNORE and the UNIKE KEY in the definition
            insert_query = "INSERT IGNORE INTO api_calls (customer_id, member_id, member_dob, timestamp) VALUES (%s, %s, %s, %s)"

            for row in rows:
                cursor.execute(insert_query, row)

            conn.commit()
            context.log.info("Data transfer complete.")

    finally:
        conn.close()


@asset
def transfer_data_members(context):
    # Database connection parameters
    db_config = {
        "host": "mysql_db_analytics",
        "user": "admin_analytics",
        "password": "password_analytics",
        "database": "analytics",
    }

    conn = pymysql.connect(**db_config)
    try:
        with conn.cursor() as cursor:

            # TODO: date is hardcoded but should be modified so that it takes last day or last week for example
            select_query = "select customer_id, member_id, member_dob, payer_id, sum(overriden) as overriden_times from coverage_raw where timestamp > '2023-03-01' group by customer_id, member_id, member_dob, payer_id"

            cursor.execute(select_query)

            rows = cursor.fetchall()
            context.log.info("Show rows")
            context.log.info(rows)

            # Upsert is necessary to have idempotency
            # This is achieved with INSERT IGNORE and the UNIKE KEY in the definition
            insert_query = "INSERT IGNORE INTO members (customer_id, member_id, member_dob, payer_id, overriden_times) VALUES (%s, %s, %s, %s, %s)"

            for row in rows:
                cursor.execute(insert_query, row)

            conn.commit()
            context.log.info("Data transfer complete.")

    finally:
        conn.close()


defs = Definitions(
    assets=[transfer_data_api_calls, transfer_data_members],
    jobs=[
        define_asset_job(
            name="api_calls_job",
            selection=[transfer_data_api_calls, transfer_data_members],
        )
    ],
    schedules=[
        ScheduleDefinition(
            name="api_calls_schedule",
            job_name="api_calls_job",
            cron_schedule="@daily",  # Cron schedule should be modified according to specs
        )
    ],
)
