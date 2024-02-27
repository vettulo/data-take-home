import logging
import pymysql

logger = logging.getLogger()

# TODO: read from environment variables
db_config = {
    'host': 'mysql_db',
    'user': 'admin',
    'password': 'password',
    'database': 'nirvana',
}


def get_overrides(member_id, member_dob):
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Execute a parameterized query
            query = "SELECT * FROM overrides WHERE member_id = %s AND member_dob = %s;"
            cursor.execute(query, (member_id, member_dob))

            # Fetch the results
            result = cursor.fetchone()

    logger.info("Found override: %s", result)
    return {
        "copay": result[2],
        "coinsurance": result[3],
        "deductible": result[4],
        "oop_max": result[5],
    }
