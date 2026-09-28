from database import get_connection


def get_kpi_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM business_kpi_summary;")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result