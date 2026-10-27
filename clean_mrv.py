"""
clean_mrv.py
Ship Fuel Efficiency Pipeline - Step 1: load and clean EU MRV data.

Reads the raw EU MRV "Publication of information" Excel file,
keeps the columns we need, fixes data quality issues and saves
a clean CSV ready for analysis.

Usage:
    python clean_mrv.py <input.xlsx> <output.csv>
"""

import sys
import pandas as pd

# The raw column names are long, so we map them to short, simple names.
COLUMNS = {
    "IMO Number": "imo_number",
    "Name": "ship_name",
    "Ship type": "ship_type",
    "Reporting Period": "reporting_year",
    "Port of Registry": "port_of_registry",
    "Total fuel consumption [m tonnes]": "total_fuel_t",
    "Total CO₂ emissions [m tonnes]": "total_co2_t",
    "Annual Time spent at sea [hours]": "time_at_sea_h",
    "Annual average Fuel consumption per distance [kg / n mile]": "fuel_per_nm_kg",
    "Annual average CO₂ emissions per distance [kg CO₂ / n mile]": "co2_per_nm_kg",
}

NUMERIC_COLUMNS = [
    "reporting_year",
    "total_fuel_t",
    "total_co2_t",
    "time_at_sea_h",
    "fuel_per_nm_kg",
    "co2_per_nm_kg",
]


def load_raw(path: str) -> pd.DataFrame:
    """Issue 1: the real headers are on row 3, so skip the first two rows."""
    return pd.read_excel(path, header=2, dtype=str)


def select_and_rename(df: pd.DataFrame) -> pd.DataFrame:
    """Issue 4: keep only the columns we need and give them short names."""
    return df[list(COLUMNS)].rename(columns=COLUMNS)


def fix_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """Issue 2: turn text like 'N/A' and 'Division by zero!' into proper nulls."""
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["reporting_year"] = df["reporting_year"].astype("Int64")
    return df


def tidy_text(df: pd.DataFrame) -> pd.DataFrame:
    """Trim stray spaces and issue 5: merge the two passenger ship labels."""
    for col in ["imo_number", "ship_name", "ship_type", "port_of_registry"]:
        df[col] = df[col].str.strip()
    df["ship_type"] = df["ship_type"].replace(
        {"Passenger ship (Cruise Passenger ship)": "Passenger ship"}
    )
    return df


def flag_inactive(df: pd.DataFrame) -> pd.DataFrame:
    """Issue 3: ships with zero fuel or zero time at sea probably didn't sail.

    We flag them instead of deleting them, so nothing is lost and
    later steps can choose to filter them out.
    """
    df["is_active"] = (df["total_fuel_t"] > 0) & (df["time_at_sea_h"] > 0)
    return df


def report(raw: pd.DataFrame, clean: pd.DataFrame) -> None:
    """Print a short summary so you can see what the cleaning did."""
    print(f"Rows loaded:            {len(raw):,}")
    print(f"Rows saved:             {len(clean):,}")
    print(f"Inactive ships flagged: {(~clean['is_active']).sum():,}")
    print(f"Missing fuel per nm:    {clean['fuel_per_nm_kg'].isna().sum():,}")
    print(f"Ship types:             {clean['ship_type'].nunique()}")


def main(input_path: str, output_path: str) -> None:
    raw = load_raw(input_path)
    clean = select_and_rename(raw.copy())
    clean = fix_numbers(clean)
    clean = tidy_text(clean)
    clean = flag_inactive(clean)
    clean.to_csv(output_path, index=False)
    report(raw, clean)
    print(f"Saved clean data to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_mrv.py <input.xlsx> <output.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
