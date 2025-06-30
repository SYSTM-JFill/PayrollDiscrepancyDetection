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

## 📦 Requirements

- Python 3.7 or higher
- pandas library
- tkinter (usually included with Python standard library)
