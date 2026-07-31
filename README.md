# Enterprise Revenue Leakage & Time-Tracking Audit System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite)
![Scikit--Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Google%20Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)

An automated multi-source reconciliation and anomaly detection pipeline engineered in Python and SQL. Designed for enterprise call centers, BPOs, and service organizations to eliminate **revenue leakage**—discrepancies between planned shift schedules, active system login activity, and client invoicing records.

---

## 🎯 Executive Summary & Business Problem

Large workforce organizations lose millions annually through operational revenue leakage. Key leakage vectors include:
* **Ghost Billing:** Invoicing clients for planned agent shifts where zero active system work was logged.
* **Unbilled Activity:** High active agent workload missing from billing logs, representing uncollected revenue.
* **Excessive Inactivity:** Billable hours inflated by extended agent system idle periods.

This pipeline reconciles disjointed logs from Workforce Management (WFM), Telephony/SSO SSO logins, and ERP billing systems to flag anomalies using **statistical Z-scores**, **unsupervised Machine Learning (Isolation Forest)**, and **business rule matrices**. Verified findings are rendered into formatted local Excel workbooks and continuously synced to live **Google Sheets cloud dashboards**.

---

## 🏗️ System Architecture
