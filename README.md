# StayWise
### Hotel Booking Analytics for Revenue & Cancellation Optimization

---

## 📌 Project Overview
The hospitality industry depends heavily on occupancy rates, pricing strategies, and customer retention. However, frequent cancellations, seasonal fluctuations, and inefficient channel strategies can reduce profitability.
**StayWise** uses data analytics to study hotel booking behavior and uncover patterns related to:

- Booking cancellations  
- Revenue generation  
- Seasonal demand shifts  
- Customer segmentation  
- Channel performance  
- Repeat guest behavior  

The project combines **Python-based analytics** and **Tableau dashboards** to help hotel decision-makers improve operational and financial performance.

---

## 🎯 Problem Statement
Hotels often struggle with:

- High cancellation rates leading to lost revenue
- Uncertain seasonal demand forecasting
- Ineffective pricing during peak/off-peak periods
- Low repeat customer retention
- Poor channel optimization (OTA vs Direct bookings)

### Our Goal

Use historical booking data to answer:

1. Why do customers cancel bookings?
2. Which customer types generate the most revenue?
3. What seasons drive maximum bookings?
4. Which booking channels are most effective?
5. How can hotels improve occupancy and profitability?

---

## 📊 Dataset
### Source

Hotel Booking Demand Dataset (Kaggle / Open Public Dataset)

### Original Size

- **119,000+ booking records**

### Final Processed Dataset

- **87,219 records**
- **29 cleaned & engineered features**

### Includes Data About:

- Resort vs City Hotels  
- Lead Time  
- Booking Channels  
- Deposit Type  
- ADR (Average Daily Rate)  
- Customer Type  
- Country  
- Stay Duration  
- Revenue  
- Cancellation Status

---

## 🛠 Tools & Technologies
| Category | Tools |
|--------|------|
| Language | Python |
| Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Dashboarding | Tableau Public |
| Notebook Environment | Jupyter Notebook |
| Version Control | Git & GitHub |

---

## 👥 Team Members
- Deepak Mishra
- Ganga Raghuwanshi
- Kunal Dev Sahu
- Lakshay Yadav
- Musthyala Sadhvik
- Sarthak Mishra
- Soumen Dass

---

# 📁 Project Structure

```bash
StayWise/
│── README.md
│── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── hotel_bookings_Raw.csv
│   ├── processed/
│   │   ├── hotel_bookings_cleaned.csv
│   │   └── eda_final_dataset.csv
│   └── final/
│       ├── final_dataset.csv
│       ├── cancellation_summary.csv
│       ├── revenue_summary.csv
│       └── season_summary.csv
│
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
│
├── docs/
│   └── data_dictionary.md
│
└── tableau/
    ├── dashboard_links.md
    └── screenshots/
```

---
