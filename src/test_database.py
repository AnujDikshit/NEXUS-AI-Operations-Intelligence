from database import get_connection

connection = get_connection()

cursor = connection.cursor()

cursor.execute("SELECT * FROM business_kpi_summary;")

result = cursor.fetchone()

print("NEXUS KPI Summary:")
print(result)

cursor.close()
connection.close()