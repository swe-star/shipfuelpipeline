import pandas as pd

df = pd.read_csv("mrv_2023_clean.csv")
active = df[df["is_active"]]

print("Ships by type:")
print(active["ship_type"].value_counts(), "\n")

print("Median fuel per nautical mile (kg) by type:")
print(active.groupby("ship_type")["fuel_per_nm_kg"].median().sort_values().round(1), "\n")

print("Top 5 ships by total fuel used:")
print(active.nlargest(5, "total_fuel_t")[["ship_name", "ship_type", "total_fuel_t"]])

