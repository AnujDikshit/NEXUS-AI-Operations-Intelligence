from kpi_service import get_kpi_summary

kpi = get_kpi_summary()

print("NEXUS KPI Summary")
print("-----------------")
print("Total Revenue:", kpi[0])
print("Total Orders:", kpi[1])
print("Average Order Value:", kpi[2])
print("Returned Orders:", kpi[3])
print("Return Rate:", kpi[4], "%")