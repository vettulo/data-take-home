import logging

import pymysql
from models import CoverageRawModel

logger = logging.getLogger()

# TODO: read from environment variables
db_config = {
    "host": "mysql_db_analytics",
    "user": "admin_analytics",
    "password": "password_analytics",
    "database": "analytics",
}


def write_to_analytics(data: CoverageRawModel):
    query = """
    INSERT INTO coverage_raw (
        customer_id, member_id, member_dob, payer_id, response_copay, 
        response_coinsurance, response_deductible, response_oop_max, 
        ch_response_copay, ch_response_coinsurance, ch_response_deductible, 
        ch_response_oop_max, overriden
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data.customer_id,
        data.member_id,
        data.member_dob,
        data.payer_id,
        data.response_copay,
        data.response_coinsurance,
        data.response_deductible,
        data.response_oop_max,
        data.ch_response_copay,
        data.ch_response_coinsurance,
        data.ch_response_deductible,
        data.ch_response_oop_max,
        data.overriden,
    )

    try:
        with pymysql.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
        logger.info("Record successfully written to coverage_raw")
    except Exception as e:
        logger.error(f"Failed to write record to coverage_raw: {e}")
        raise
