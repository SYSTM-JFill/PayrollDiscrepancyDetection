import pandas as pd
from tkinter import filedialog, Tk
from datetime import datetime

# === Setup hidden Tk window ===
root = Tk()
root.withdraw()

# === Prompt user to select input files ===
print("📂 Select TABS Payroll CSV")
tabs_path = filedialog.askopenfilename(title="Select TABS Payroll CSV", filetypes=[("CSV Files", "*.csv")])
print("📂 Select SAP Payroll CSV")
sap_path = filedialog.askopenfilename(title="Select SAP Payroll CSV", filetypes=[("CSV Files", "*.csv")])

# === Load CSVs ===
tabs_df = pd.read_csv(tabs_path)
sap_df = pd.read_csv(sap_path)

# === Prepare DataFrames ===
tabs_comp = tabs_df[['Date', 'Employee_ID', 'Total_Hours']].copy()
tabs_comp.rename(columns={'Total_Hours': 'TABS_Total_Hours'}, inplace=True)

sap_comp = sap_df[['Date', 'Employee_ID', 'Total_Hours']].copy()
sap_comp.rename(columns={'Total_Hours': 'SAP_Total_Hours'}, inplace=True)

# === Convert Dates ===
tabs_comp['Date'] = pd.to_datetime(tabs_comp['Date'])
sap_comp['Date'] = pd.to_datetime(sap_comp['Date'])

# === Merge on Date + Employee_ID ===
merged = pd.merge(tabs_comp, sap_comp, on=['Date', 'Employee_ID'], how='outer')

# === Flag mismatches ===
merged['Hour_Difference'] = merged['SAP_Total_Hours'] - merged['TABS_Total_Hours']
merged['Match'] = merged['Hour_Difference'].apply(lambda x: abs(x) < 0.01 if pd.notnull(x) else False)

# === Filter to mismatches only ===
mismatches = merged[~merged['Match'] | merged['Match'].isnull()]

# === Display Results ===
print("\n=== Summary: SAP vs TABS Payroll Audit ===")
print(f"🔎 Total records compared: {len(merged)}")
print(f"❌ Mismatches found: {len(mismatches)}")
print("\n=== Mismatched Records ===")
print(mismatches[['Date', 'Employee_ID', 'TABS_Total_Hours', 'SAP_Total_Hours', 'Hour_Difference']].head(10))

# === Prompt user to save output ===
default_name = f"payroll_discrepancy_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
output_path = filedialog.asksaveasfilename(
    title="Save Discrepancy Report As...",
    defaultextension=".csv",
    initialfile=default_name,
    filetypes=[("CSV files", "*.csv")]
)

if output_path:
    mismatches.to_csv(output_path, index=False)
    print(f"\n📁 Discrepancy report saved to: {output_path}")
else:
    print("❌ Report not saved.")
