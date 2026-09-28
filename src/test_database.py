from database import get_connection


def test_database_connection():
    connection = get_connection()

    assert connection is not None

    cursor = connection.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()

    assert result[0] == 1

    cursor.close()
    connection.close()
