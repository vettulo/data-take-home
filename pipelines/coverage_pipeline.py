import pymysql
from dagster import Definitions, ScheduleDefinition, asset, define_asset_job
import logging

logger = logging.getLogger()


@asset
def transfer_data(context):
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
            select_query = "SELECT customer_id, member_id, member_dob, timestamp FROM coverage_raw where timestamp < '2023-03-01'"

            cursor.execute(select_query)

            rows = cursor.fetchall()
            context.log.info("Show rows")
            context.log.info(rows)

            # Upsert is necessary to have idempotency - This is achieved with
            # "ON DUPLICATE KEY" in MySQL
            insert_query = "INSERT INTO api_calls (customer_id, member_id, member_dob, timestamp) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE member_id = VALUES(member_id), member_dob = VALUES(member_dob), timestamp = CURRENT_TIMESTAMP"

            for row in rows:
                cursor.execute(insert_query, row)

            conn.commit()

    finally:
        conn.close()

    context.log.info("Data transfer complete.")


defs = Definitions(
    assets=[transfer_data],
    jobs=[define_asset_job(name="api_calls_job", selection=[transfer_data])],
    schedules=[
        ScheduleDefinition(
            name="api_calls_schedule", job_name="api_calls_job", cron_schedule="@daily"
        )
    ],
)
