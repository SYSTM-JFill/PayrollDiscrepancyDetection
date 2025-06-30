import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from tkinter import filedialog, Tk
from fpdf import FPDF
import os
import tempfile
from datetime import datetime
import textwrap

# === Font Fix for Plot Emojis ===
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
sns.set(style='whitegrid', palette='muted')

# === Tk GUI Setup ===
root = Tk()
root.withdraw()

# === Prompt user to select input CSV files ===
print("📂 Select CURRENT TABS payroll CSV")
tabs_path = filedialog.askopenfilename(title="Select CURRENT TABS Payroll CSV")
tabs_df = pd.read_csv(tabs_path)

print("📂 Select SAP payroll CSV")
sap_path = filedialog.askopenfilename(title="Select SAP Payroll CSV")
sap_df = pd.read_csv(sap_path)

print("📂 Select DISCREPANCY CSV (SAP vs TABS)")
mismatch_path = filedialog.askopenfilename(title="Select Discrepancy CSV")
mismatches = pd.read_csv(mismatch_path)

print("📂 (Optional) Select PREVIOUS TABS payroll CSV (for comparison)")
prev_tabs_path = filedialog.askopenfilename(title="Select Previous TABS Payroll CSV (optional)")
prev_tabs_df = pd.read_csv(prev_tabs_path) if prev_tabs_path else None

# === Convert date columns to datetime ===
for df in [tabs_df, sap_df, mismatches]:
    df['Date'] = pd.to_datetime(df['Date'])

if prev_tabs_df is not None:
    prev_tabs_df['Date'] = pd.to_datetime(prev_tabs_df['Date'])

# === Create temp directory to hold chart images ===
tmp_dir = tempfile.mkdtemp()
image_paths = []

def save_plot(fig, filename):
    path = os.path.join(tmp_dir, filename)
    fig.savefig(path, bbox_inches='tight')
    image_paths.append(path)
    plt.close(fig)

# === Generate Summary Text ===
summary_txt = []
summary_txt.append(f"Payroll Report Summary ({datetime.now().strftime('%Y-%m-%d')})")
summary_txt.append(f"Employees in TABS: {tabs_df['Employee_ID'].nunique()}")
summary_txt.append(f"Total TABS Records: {len(tabs_df)}")
summary_txt.append(f"Job Codes: {tabs_df['Job_Code'].nunique()} | Projects: {tabs_df['Project_ID'].nunique()}")
summary_txt.append(f"Total TABS Hours: {tabs_df['Total_Hours'].sum():,.2f}")
summary_txt.append(f"Total Discrepancies: {len(mismatches)}")

# Project hours breakdown
if 'Project_ID' in tabs_df.columns:
    project_hours = tabs_df.groupby('Project_ID')['Total_Hours'].sum().sort_values(ascending=False)
    top_projects = project_hours.head(5)
    summary_txt.append("Top Projects by Total Hours:")
    for proj, hours in top_projects.items():
        summary_txt.append(f"  - {proj}: {hours:,.2f} hrs")

# Period comparison
if prev_tabs_df is not None:
    curr_total = tabs_df['Total_Hours'].sum()
    prev_total = prev_tabs_df['Total_Hours'].sum()
    delta = curr_total - prev_total
    delta_pct = (delta / prev_total) * 100 if prev_total != 0 else 0
    summary_txt.append(f"Period-to-Period Change: {delta:+,.2f} hrs ({delta_pct:+.1f}%)")

# === Create Plots ===
# 1. Mismatches by Date
fig, ax = plt.subplots(figsize=(10, 4))
mismatches_by_date = mismatches.groupby('Date').size()
mismatches_by_date.plot(kind='bar', color='steelblue', ax=ax)
ax.set_title("Mismatched Records by Date")
ax.set_xlabel("Date")
ax.set_ylabel("Count")
ax.tick_params(axis='x', rotation=45)
save_plot(fig, "mismatches_by_date.png")

# 2. Top Employees by Discrepancy
top_emp_diff = mismatches.groupby('Employee_ID')['Hour_Difference'].sum().abs().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(8, 5))
top_emp_diff.sort_values().plot(kind='barh', color='firebrick', ax=ax)
ax.set_title("Top 10 Employees by Hour Discrepancy")
ax.set_xlabel("Absolute Hour Difference")
ax.set_ylabel("Employee ID")
save_plot(fig, "top_employees.png")

# 3. Distribution of Hour Differences
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(mismatches['Hour_Difference'], bins=20, kde=True, color='orange', ax=ax)
ax.set_title("Distribution of Hour Differences (SAP - TABS)")
ax.set_xlabel("Hour Difference")
ax.set_ylabel("Frequency")
save_plot(fig, "hour_diff_histogram.png")

# 4. Net Discrepancy Over Time
net_by_date = mismatches.groupby('Date')['Hour_Difference'].sum()
fig, ax = plt.subplots(figsize=(10, 4))
net_by_date.plot(marker='o', color='purple', ax=ax)
ax.axhline(0, linestyle='--', color='gray')
ax.set_title("Net Hour Difference by Date (SAP - TABS)")
ax.set_xlabel("Date")
ax.set_ylabel("Net Hour Difference")
ax.tick_params(axis='x', rotation=45)
save_plot(fig, "net_hour_trend.png")

# 5. Total Hours by Job Code
job_summary = tabs_df.groupby('Job_Code')['Total_Hours'].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
job_summary.plot(kind='barh', color='slateblue', ax=ax)
ax.set_title("Total Hours by Job Code")
ax.set_xlabel("Total Hours Worked")
ax.set_ylabel("Job Code")
save_plot(fig, "total_hours_by_job.png")

# 6. Mismatches by Job Code
if 'Job_Code' in sap_df.columns:
    mismatch_job = pd.merge(mismatches, sap_df[['Date', 'Employee_ID', 'Job_Code']], on=['Date', 'Employee_ID'], how='left')
    job_diff = mismatch_job.groupby('Job_Code')['Hour_Difference'].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    job_diff.plot(kind='barh', color='darkorange', ax=ax)
    ax.set_title("Mismatched Hours by Job Code")
    ax.set_xlabel("Net Hour Discrepancy (SAP - TABS)")
    ax.set_ylabel("Job Code")
    save_plot(fig, "mismatches_by_job.png")

# 7. Mismatches by Project
if 'Project_ID' in sap_df.columns:
    mismatch_proj = pd.merge(mismatches, sap_df[['Date', 'Employee_ID', 'Project_ID']], on=['Date', 'Employee_ID'], how='left')
    proj_diff = mismatch_proj.groupby('Project_ID')['Hour_Difference'].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    proj_diff.plot(kind='barh', color='mediumseagreen', ax=ax)
    ax.set_title("Mismatched Hours by Project")
    ax.set_xlabel("Net Hour Discrepancy")
    ax.set_ylabel("Project ID")
    save_plot(fig, "mismatches_by_project.png")

# === Create PDF ===
pdf = FPDF()
left_margin = 15
right_margin = 15
pdf.set_left_margin(left_margin)
pdf.set_right_margin(right_margin)
pdf.set_auto_page_break(auto=True, margin=15)

pdf.add_page()
pdf.set_font("Helvetica", size=8)

page_width = pdf.w
usable_width = page_width - left_margin - right_margin
line_height = 7
approx_chars_per_line = int(usable_width / 2.5)

# Add summary lines
for line in summary_txt:
    clean_line = ''.join(ch for ch in line if 32 <= ord(ch) <= 126).strip()
    wrapped_lines = textwrap.wrap(clean_line, width=approx_chars_per_line)
    for wline in wrapped_lines:
        pdf.set_x(left_margin)
        pdf.multi_cell(w=usable_width, h=line_height, txt=wline, align='L')

# === Append top mismatches ===
pdf.set_font("Helvetica", 'B', size=8)
pdf.ln(5)
pdf.set_x(left_margin)
pdf.multi_cell(usable_width, line_height, txt="Top Mismatches (Date, Employee, Hours):", align='L')
pdf.set_font("Helvetica", size=8)

top_mismatches = (
    mismatches
    .copy()
    .assign(Hour_Diff_Abs=lambda df: df['Hour_Difference'].abs())
    .sort_values(by='Hour_Diff_Abs', ascending=False)
    .head(15)
)

for _, row in top_mismatches.iterrows():
    line = f"{row['Date'].strftime('%Y-%m-%d')} | EmpID: {row['Employee_ID']} | {row['Hour_Difference']:+.2f} hrs"
    wrapped_lines = textwrap.wrap(line, width=approx_chars_per_line)
    for wline in wrapped_lines:
        pdf.set_x(left_margin)
        pdf.multi_cell(w=usable_width, h=line_height, txt=wline, align='L')

# === Add Chart Pages ===
for img_path in image_paths:
    pdf.add_page()
    pdf.image(img_path, x=10, y=20, w=190)

# === Save PDF ===
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
default_filename = f"Payroll_Audit_Report_{timestamp}.pdf"
pdf_filename = filedialog.asksaveasfilename(
    title="Save PDF Report As...",
    defaultextension=".pdf",
    initialfile=default_filename,
    filetypes=[("PDF files", "*.pdf")]
)

if pdf_filename:
    pdf.output(pdf_filename)
    print(f"📄 PDF report saved to: {pdf_filename}")
else:
    print("❌ PDF not saved.")
