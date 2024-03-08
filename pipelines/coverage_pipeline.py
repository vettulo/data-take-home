import pymysql
from dagster import asset
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

            insert_query = "INSERT INTO api_calls (customer_id, member_id, member_dob, timestamp) VALUES (%s, %s, %s, %s)"

            for row in rows:
                cursor.execute(insert_query, row)

            conn.commit()

    finally:
        conn.close()

    context.log.info("Data transfer complete.")
