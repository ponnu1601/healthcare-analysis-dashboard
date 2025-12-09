# Healthcare Analysis Dashboard

## 1. Background and Overview

### Project Context
This project presents a comprehensive data analysis of a synthetic healthcare dataset. The original dataset contained 55,500 patient records spanning 5 years (May 2019 - May 2024). After data quality assessment, 108 records with negative billing amounts were removed, resulting in a final clean dataset of 55,392 records. As a data analyst, the objective of this project is to transform raw healthcare data into actionable insights that can inform operational and strategic decision-making.

### Project Goals
- **Data Exploration:** Understand the structure, quality, and characteristics of healthcare data
- **Pattern Identification:** Discover trends and correlations across patient demographics, medical conditions, and treatment outcomes
- **Performance Analysis:** Evaluate how different factors (insurance, admission type, medications) impact patient care and costs
- **Decision Support:** Provide stakeholders with interactive tools to explore data and make informed decisions

### Deliverables
A user-friendly web-based dashboard built with Streamlit that enables business stakeholders to independently explore and visualize healthcare metrics. The dashboard implements the following Streamlit features:

**Streamlit Features & Libraries Used:**
- **Interactive Components:** Multi-select dropdowns and session state management for dynamic filtering across all analysis sections
- **Data Visualization:** Plotly charts (pie charts, bar charts) integrated with Streamlit for interactive visualizations that respond to user filters in real-time
- **Multi-page Interface:** Tabbed interface using Streamlit buttons styled with custom CSS for seamless navigation between dataset overview and five analysis sections (Demographics, Medical Conditions, Insurance, Admission Type, Medication)
- **Database Integration:** SQLAlchemy ORM for secure MySQL database connections with efficient query execution and caching using @st.cache_resource
- **Responsive Layout:** Two-column layouts with dynamic content that adjusts based on user interactions and filter selections
- **Data Handling:** Pandas DataFrames for data manipulation, transformation, and presentation in interactive Streamlit tables with custom styling
- **Real-time Updates:** Query results dynamically update based on sidebar filter selections, providing immediate feedback to users

**Technical Architecture:**
The dashboard processes over 40 optimized SQL queries against a MySQL database containing 55,392 patient records. Each analysis section includes interactive filters (Medical Condition, Insurance Provider, Admission Type, Gender) that dynamically construct WHERE clauses and re-execute queries in real-time, enabling users to drill down into specific patient segments without any technical knowledge.

---

## 2. Data Structure Overview

### Dataset Composition
The original dataset contained 55,500 records. During data quality assessment, 108 records (0.19%) with negative billing amounts were identified and removed as data errors, resulting in a clean dataset of 55,392 patient admissions for analysis.

- **Total Records:** 55,392 patient admissions (after cleaning)
- **Time Period:** May 8, 2019 - May 7, 2024 (5 years)
- **Data Quality:** 100% complete (no missing values)

**Data Source:**
[Healthcare Dataset](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)

### Key Fields (15 Columns)

| Category | Fields |
|----------|--------|
| **Patient Demographics** | Patient ID, Name, Age (13-89 years), Gender (Male/Female), Blood Type (8 types) |
| **Medical Information** | Medical Condition (6 types), Medication (5 types), Test Results (Normal/Abnormal/Inconclusive) |
| **Admission Details** | Date of Admission, Discharge Date, Admission Type (Emergency/Elective/Urgent) |
| **Healthcare Provider** | Doctor (40,341 unique), Hospital (39,876 unique) |
| **Financial** | Billing Amount ($9.24 - $52,764.28), Room Number |

### Data Quality Metrics
- **Age Range:** 13 to 89 years (Average: 51.5 years)
- **Gender Distribution:** 50.2% Male, 49.8% Female (nearly balanced)
- **Medical Conditions:** 6 distinct conditions evenly distributed
- **Insurance Providers:** 5 major providers with balanced patient distribution
- **Test Results:** Fairly even distribution across all three outcome types

**Data Characteristics:**
This analysis uses a synthetic dataset generated for educational purposes. As synthetic data, it exhibits more uniformity than typical real-world healthcare data. Real healthcare datasets typically show greater cost variation across conditions (5-15% vs 2.5% in this dataset), more pronounced demographic skews, uneven admission type distribution, and stronger condition-based cost differences. The analysis demonstrates competency with real-world methodologies and tools, but findings should be understood within the context of synthetic data characteristics.

---

## 3. Executive Summary

### Critical Business Insights

**1. Healthcare Costs Are Surprisingly Standardized Across All Dimensions**

Despite analyzing multiple variables (medical condition, gender, admission type, insurance provider, medication), billing costs show remarkable consistency with variations of less than 1% in most categories. This indicates either highly effective standardized protocols or insufficient variation in treatment complexity to impact costs. The implication is that cost management in this healthcare system is driven by operational efficiency rather than patient mix variation.

**2. Gender Bias May Exist in Treatment Protocols**

Male patients incur $137 higher average billing (0.5% difference), which while small, is consistent across the dataset. This warrants investigation as it could indicate different treatment pathways, procedure selection, or severity assessment by gender—representing a potential equity and quality concern.

**3. Current Data Collection May Have Gaps**

Cancer treatment costs ($25,162) are unexpectedly low compared to obesity ($25,806) and other conditions, contradicting industry knowledge that cancer treatment is typically among the most expensive. This suggests either exceptional cost management in cancer care, data collection issues, or incomplete cost capture.

**4. Operational Processes Are Highly Consistent**

Hospital stay duration (15-16 days), test result distribution, and patient outcomes are uniform across conditions and demographics. This consistency is operationally valuable as it enables predictable resource planning and budget forecasting, but it also suggests limited customization of care pathways.

**5. Insurance Type Does Not Drive Cost Variation**

With less than 1% variation in costs across five insurance providers, the data indicates that insurance type is not a driver of healthcare costs in this system. This suggests internal healthcare delivery processes, not insurance leverage, determine pricing.

**6. Medication Selection Correlates with Treatment Costs**

The $394 difference in billing between Ibuprofen and Lipitor treatments (1.5% variation) is the highest among comparable categories, suggesting medication choice may be a cost driver or indicator of treatment complexity.

---

## 4. Insights Deep Dive

### Deep Dive 1: The Cost Standardization Pattern

**What the Data Reveals:**
Across 55,392 patient records and six distinct medical conditions, billing costs vary by only $644 (2.5% spread). Even when segmented by gender ($137 difference), insurance provider ($227 difference), and admission type ($105 difference), the variation remains under 1%. This is exceptionally tight for a healthcare system treating diverse conditions.

**Why This Matters:**
Typically, healthcare costs vary significantly based on condition severity, treatment complexity, and patient comorbidities. The uniformity suggests either:
- Highly effective standardization of care protocols and pricing
- Limited capture of true treatment costs (potential data gaps)
- Homogeneous patient severity across conditions

**Operational Implications:**
The standardized costs make budgeting predictable but may mask underlying cost drivers. A patient with obesity costs virtually the same as one with diabetes or hypertension, despite potentially different treatment requirements. This pattern indicates that pricing may not reflect actual resource consumption or there may be hidden costs in certain patient populations.

---

### Deep Dive 2: Gender-Based Treatment Pathways

**What the Data Reveals:**
One gender consistently incurs $137 higher billing across all conditions, insurance types, and admission types. This is not a statistical anomaly—it appears consistently when compared across genders in every data segment analyzed. The 50.2%-49.8% gender split eliminates sampling bias as an explanation.

**Detailed Analysis:**
- Average billing: Higher gender $25,608 vs Lower gender $25,471 ($137 difference, 0.54%)
- This difference persists across all 6 medical conditions
- It appears in both emergency and elective admissions
- It exists uniformly across all 5 insurance providers
- Gender distribution by condition shows no significant skew

**Why This Matters:**
While the percentage difference is small, the consistency is striking. In healthcare, gender-based differences often reflect:
1. **Clinical severity differences:** One gender may present with more advanced disease at diagnosis, requiring more expensive treatment
2. **Protocol differences:** Different diagnostic or treatment pathways between genders
3. **Procedure selection:** Different types or frequencies of procedures by gender
4. **Documentation differences:** Variation in billing documentation completeness between genders

**Equity and Quality Concerns:**
Gender-based treatment differences can indicate unequal access to certain treatments, different clinical assessment standards, or potential bias in resource allocation. Understanding whether this cost difference reflects clinical necessity or systematic differences in care delivery is critical for ensuring equitable healthcare delivery.

---

### Deep Dive 3: Cancer Treatment Cost Anomaly

**What the Data Reveals:**
Cancer treatment shows the lowest average billing ($25,162) despite obesity having the highest ($25,806). This $644 difference, while small in absolute terms, is significant because cancer is typically one of the most expensive conditions to treat in healthcare systems.

**What This Means for the Dataset:**
The low cancer costs suggest several possibilities:
1. **Data Collection Gap:** Cancer-related costs may not be fully captured in billing records
2. **Population Difference:** This dataset's cancer patients may have early-stage, low-cost cancers
3. **Treatment Limitation:** Only certain cancer treatments may be included in the dataset
4. **Exceptional Efficiency:** This healthcare system may have unusually efficient cancer care protocols

**Critical Data Quality Issue:**
The observed cancer treatment cost ($25,162) is inconsistent with typical healthcare patterns where cancer is among the most expensive conditions to treat. This significant discrepancy suggests potential issues with data completeness or population representation that must be resolved before cost conclusions can be trusted for decision-making.

---

## 5. Recommendations

### Short-term Action Plan (Next 3 months)

- Investigate gender-based billing differences to determine if the $137 variance reflects clinical necessity or protocol variations, and standardize treatment protocols accordingly
- Verify cancer treatment costs ($25,162) against industry benchmarks and analyze medication selection patterns to understand the $394 cost difference between Ibuprofen and Lipitor treatments
- Implement protocols to standardize hospital stay duration for similar conditions
- Validate high-cardinality data fields (40,341 doctors, 39,876 hospitals) for accuracy and consolidation of duplicates

### Medium-term Action Plan (3-6 months)

- Build predictive models to forecast patient outcomes based on demographics and medical conditions while identifying high-risk patient populations
- Develop detailed insurance-specific analyses to track quality metrics alongside costs and uncover best practices
- Expand the dataset to include additional variables such as comorbidities, treatment procedures, and readmission rates
- Create real-time monitoring dashboards for operations teams and implement automated data quality controls for future entries

### Long-term Strategic Plan (6-12 months)

- Integrate external benchmarks for performance comparison and establish automated monthly/quarterly reporting infrastructure
- Develop stakeholder-specific dashboard views and implement predictive dashboards for capacity planning with automated alert systems for anomalies
- Train clinical and operational teams on dashboard usage and establish regular review cycles to track progress on improvement initiatives
- Document and share best practices discovered through analysis to drive organizational learning and evidence-based decision-making

---

## Technical Stack

- **Database:** MySQL
- **Data Analysis:** Python (Pandas)
- **Visualization:** Plotly
- **Web Framework:** Streamlit
- **Database ORM:** SQLAlchemy
- **SQL Queries:** 40+ optimized queries

## How to Use the Dashboard

1. Navigate to the Overview section to understand dataset composition
2. Explore Column Details to understand individual data fields
3. Use analysis sections (Demographics, Medical Conditions, Insurance, etc.) with interactive filters
4. Apply filters to drill down into specific patient segments
5. Export insights for reporting and decision-making
