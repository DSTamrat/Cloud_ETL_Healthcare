\# Cloud-Based ETL Pipeline for Healthcare Admissions



This project demonstrates a cloud‑ready ETL (Extract–Transform–Load) pipeline using synthetic healthcare admissions data.  

It simulates how real healthcare systems ingest, clean, transform, and prepare data for analytics, dashboards, and machine learning.



---



\## Project Overview



This ETL pipeline performs:



\### \*\*1. Ingest\*\*

Loads raw synthetic healthcare admissions data (1000 rows) generated programmatically.



\### \*\*2. Clean\*\*

\- Removes duplicates  

\- Handles missing values  

\- Fixes invalid values  

\- Standardizes data types  

\- Adds derived fields (year, month, elderly flag)



\### \*\*3. Transform\*\*

Creates aggregated metrics by:

\- Hospital unit  

\- Primary condition  



Metrics include:

\- Admissions count  

\- Average length of stay  

\- Readmission rate  

\- Average cost  



\### \*\*4. Load\*\*

Saves:

\- Cleaned dataset → `data\_processed/healthcare\_admissions\_clean.csv`  

\- Aggregated metrics → `data\_processed/healthcare\_aggregated\_metrics.csv`  



These outputs are ready for:

\- Power BI dashboards  

\- Tableau visualizations  

\- Machine learning models  



---



\##  📁 Folder Structure

```text
cloud_etl_healthcare/
├── data_raw/
├── data_processed/
├── etl/
│   ├── generate_healthcare_data.py
│   └── etl_healthcare.py
├── notebooks/
└── README.md






