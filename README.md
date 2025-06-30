# 🧾 Payroll Discrepancy Audit Tool

This Python-based tool is designed to perform a detailed audit and reconciliation of payroll records between two distinct systems — **TABS** and **SAP**. Payroll teams often extract reports from multiple systems that are supposed to track employee hours worked, but discrepancies can occur due to manual entry errors, timing issues, or system differences. This tool automates the detection of those discrepancies by comparing total hours logged per employee per date and flags mismatches for further investigation.

---

## 🔍 Project Overview

### Purpose

The goal of this project is to help payroll analysts and finance teams quickly identify inconsistencies in recorded employee hours between two separate payroll data exports. By automating the comparison process, the tool reduces the risk of human error, accelerates audits, and ensures payroll accuracy, ultimately helping prevent overpayments or underpayments.

### How it Works

- Users provide two CSV files exported from the **TABS** and **SAP** payroll systems.
- The tool loads these datasets, normalizes the key comparison columns, and performs an outer merge on the combination of `Date` and `Employee_ID`.
- It calculates the difference in total hours worked between the two systems for each matched record.
- Records where the difference exceeds a small tolerance threshold (default: 0.01 hours) are flagged as mismatches.
- The tool produces a summary report printed in the terminal and exports all discrepancies into a CSV file for audit follow-up.

### Mock Data

This project includes **mock data** generated to simulate typical payroll exports from TABS and SAP systems. This synthetic dataset allows you to test and validate the tool’s functionality without requiring sensitive or proprietary payroll information.

---

## 📤 Output

After running the audit tool, you will receive:

### 1. Terminal Summary

A concise summary printed to the terminal showing:

- Total records compared between the two systems
- Number of mismatches detected
- A preview of the first few mismatched records

### 2. Discrepancy Report CSV

A detailed CSV file listing all mismatched records with the following columns:

| Date       | Employee_ID | TABS_Total_Hours | SAP_Total_Hours | Hour_Difference | Match  |
|------------|-------------|------------------|-----------------|-----------------|--------|
| 2024-06-10 | EMP002      | 7.5              | 8.0             | 0.5             | False  |

- **Date**: The date of the payroll record.
- **Employee_ID**: Unique identifier for the employee.
- **TABS_Total_Hours**: Hours recorded in the TABS payroll export.
- **SAP_Total_Hours**: Hours recorded in the SAP payroll export.
- **Hour_Difference**: The difference in hours (SAP - TABS).
- **Match**: Boolean indicating whether hours match within the tolerance.

### 3. Visual Examples

Here are example screenshots of the output and discrepancy report from the project:

- ![Report Output Example 1](https://github.com/SYSTM-JFill/PayrollDiscrepancyDetection/blob/main/Payroll_Detection/Report_Output_Example1.png)
- ![Report Output Example 2](https://github.com/SYSTM-JFill/PayrollDiscrepancyDetection/blob/main/Payroll_Detection/Report_Output_Example2.png)
- ![Report Output Example 3](https://github.com/SYSTM-JFill/PayrollDiscrepancyDetection/blob/main/Payroll_Detection/Report_Output_Example3.png)

These images illustrate typical mismatch records and the format of the exported CSV file, helping you quickly understand and investigate discrepancies.

---

