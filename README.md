# SectionB_G-1_StayWise - Project Repository

> **Newton School of Technology | Data Visualization & Analytics**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

### Quick Start

If you are working locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

If you are working in Google Colab:

- Upload or sync the notebooks from `notebooks/`
- Keep the final `.ipynb` files committed to GitHub
- Export any cleaned datasets into `data/processed/`

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | StayWise: Hotel Booking Analytics for Revenue & Cancellation Optimization |
| **Sector** | Hospitality / Travel |
| **Team ID** | G-1 |
| **Section** | Section B |
| **Faculty Mentor** | _To be filled by team_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _To be filled by team_ |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Sarthak Mishra | `github-handle` |
| Data Lead | Ganga Raghuwanshi | `github-handle` |
| ETL Lead | Musthyala Sadhvik | `github-handle` |
| Analysis Lead | Kunal Dev Sahu | `github-handle` |
| Visualization Lead | Soumen Dass | `github-handle` |
| Strategy Lead | Deepak Mishra | `github-handle` |
| PPT and Quality Lead | Lakshay Yadav | `github-handle` |

---

## Business Problem

The hospitality industry depends heavily on occupancy rates, pricing strategies, and customer retention. However, frequent cancellations, seasonal fluctuations, and inefficient channel strategies lead to significant revenue loss and suboptimal resource allocation. This project aims to analyze historical booking data for City and Resort hotels to uncover key drivers of cancellations and characterize customer behavior. The insights will empower stakeholders—such as hotel managers and marketing teams—to optimize pricing strategies, scale operational staff dynamically, and reduce overall cancellation rates.

**Core Business Question**

> What are the primary drivers of hotel booking cancellations, and how can pricing and channel strategies be optimized to maximize revenue?

**Decision Supported**

> This analysis will enable stakeholders to implement targeted non-refundable deposit policies for high-risk bookings and allocate marketing budgets effectively toward lower-cancellation direct booking channels.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Hotel Booking Demand Dataset (Kaggle) |
| **Direct Access Link** | _[Dataset Link]_ |
| **Row Count** | 119,209 (Raw) / 87,219 (Processed) |
| **Column Count** | 49 (Raw) / 29 (Engineered) |
| **Time Period Covered** | 2015 to 2017 |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `is_canceled` | 1 if booking was canceled, 0 otherwise | Primary target variable for cancellation analysis |
| `lead_time` | Number of days between booking and arrival | Used to analyze booking behavior and cancellation risk |
| `average_daily_rate` | Average price per night | Used to compute revenue and price elasticity |
| `market_segment` | Channel through which the booking was made | Used to compare performance across OTAs vs. Direct |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| **Cancellation Rate %** | Percentage of bookings that are canceled | `sum(is_canceled) / count(total_bookings)` |
| **Total Revenue** | Total value generated from a completed booking | `(stays_in_weekend_nights + stays_in_week_nights) * average_daily_rate` |
| **Revenue per Guest** | Revenue normalized by the number of guests | `total_revenue / (adults + children + babies)` |
| **CLV Proxy** | Estimated customer lifetime value strictly from realized revenue | `total_revenue * (1 - is_canceled)` |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | [ ] |
| **Executive View** | High-level summary showing total revenue, cancellation rate, and occupancy trends over time. |
| **Operational View** | Drill-down into lead time categories, market segment performance, and deposit type correlations. |
| **Main Filters** | Hotel Type (City/Resort), Year/Month, Market Segment, Customer Type |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **City vs. Resort Cancellations**: City Hotels experience a significantly higher cancellation rate (approx. 41%) compared to Resort Hotels (approx. 27%).
2. **Lead Time Risk**: Bookings made with a lead time greater than 180 days show a disproportionately high risk of cancellation.
3. **Channel Performance**: Bookings originating from Travel Agents and Tour Operators (TA/TO) have higher cancellation rates than Direct bookings.
4. **Seasonal Peaks**: Summer months (July and August) represent the peak season for both the volume of bookings and total revenue generated.
5. **Deposit Impact**: Non-refundable deposits drastically lower the cancellation probability, whereas "No Deposit" bookings account for the majority of cancellations.
6. **Guest Demographics**: Families (bookings with children) tend to have longer stay durations and higher revenue per booking compared to single travelers.
7. **Repeat Customers**: Repeat guests have an extremely low cancellation rate compared to first-time bookers.
8. **Parking Requests**: Guests who require parking spaces are highly unlikely to cancel their reservations.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | Lead Time Risk | Implement stricter non-refundable deposit policies for bookings made >180 days in advance. | Reduce long-lead cancellations and secure early cash flow. |
| 2 | Channel Performance | Launch targeted loyalty incentives or discounts for Direct bookings. | Decrease reliance on third-party OTAs and improve overall retention. |
| 3 | Seasonal Peaks | Scale operational staff and adjust dynamic pricing models upward during Summer months. | Maximize revenue capture during high-demand periods while maintaining service quality. |
| 4 | Parking Requests | Bundle parking with premium room rates for guests traveling by car. | Increase auxiliary revenue and secure low-risk, high-intent bookings. |

---

## Repository Structure

```text
SectionB_G-1_StayWise/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   |-- 04_statistical_analysis.ipynb
|   `-- 05_final_load_prep.ipynb
|
|-- scripts/
|   |-- __init__.py
|   `-- etl_pipeline.py
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- README.md
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
|   `-- StayWise_Resume_Points.md
`-- DVA-focused-Portfolio/
    `-- StayWise_Case_Study.md
```

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Recommended Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Is the business question clear and well-scoped? |
| Data Quality and ETL | 15 | Is the cleaning pipeline thorough and documented? |
| Analysis Depth | 25 | Are statistical methods applied correctly with insight? |
| Dashboard and Visualization | 20 | Is the Tableau dashboard interactive and decision-relevant? |
| Business Recommendations | 20 | Are insights actionable and well-reasoned? |
| Storytelling and Clarity | 10 | Is the presentation professional and coherent? |
| **Total** | **100** | |

> Marks are awarded for analytical thinking and decision relevance, not chart quantity, visual decoration, or code length.

---

## Submission Checklist

**GitHub Repository**

- [x] Public repository created with the correct naming convention (`SectionName_TeamID_ProjectName`)
- [x] All notebooks committed in `.ipynb` format
- [x] `data/raw/` contains the original, unedited dataset
- [x] `data/processed/` contains the cleaned pipeline output
- [x] `tableau/screenshots/` contains dashboard screenshots
- [x] `tableau/dashboard_links.md` contains the Tableau Public URL
- [x] `docs/data_dictionary.md` is complete
- [x] `README.md` explains the project, dataset, and team
- [x] All members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] Cover page, executive summary, sector context, problem statement
- [ ] Data description, cleaning methodology, KPI framework
- [ ] EDA with written insights, statistical analysis results
- [ ] Dashboard screenshots and explanation
- [ ] 8-12 key insights in decision language
- [ ] 3-5 actionable recommendations with impact estimates
- [ ] Contribution matrix matches GitHub history

**Presentation Deck**

- [ ] Final presentation exported as PDF into `reports/`
- [ ] Title slide through recommendations, impact, limitations, and next steps

**Individual Assets**

- [x] DVA-oriented resume updated to include this capstone
- [x] Portfolio link or project case study added

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| Deepak Mishra | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Ganga Raghuwanshi | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Kunal Dev Sahu | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Lakshay Yadav | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Musthyala Sadhvik | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Sarthak Mishra | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| Soumen Dass | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** _____________________________

**Date:** _______________

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
