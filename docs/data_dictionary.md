# Data Dictionary

This file documents the important fields in the dataset used for analysis and dashboarding. It includes raw columns, data cleaning steps, and derived KPIs.

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | Hotel Bookings Dataset |
| Source | Raw CSV (`hotel_bookings_Raw.csv`) |
| Raw file name | `hotel_bookings_Raw.csv` |
| Final file name | `final_dataset.csv` |
| Granularity | One row per booking / reservation |

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `hotel` | string | Type of hotel (Resort Hotel or City Hotel) | `Resort Hotel` | EDA / Tableau | Standardized string |
| `is_canceled` | int | Indicates if the booking was canceled (1) or not (0) | `0` | EDA / KPI | - |
| `lead_time` | float | Number of days between booking and arrival | `342.0` | EDA / Tableau | - |
| `arrival_date_year` | int | Year of arrival date | `2015` | EDA / Tableau | - |
| `arrival_date_month` | string | Month of arrival date | `July` | EDA / Tableau | - |
| `arrival_date_week_number` | int | Week number of arrival date | `27` | EDA / Tableau | - |
| `arrival_date_day_of_month` | int | Day of arrival date | `1` | EDA / Tableau | - |
| `stays_in_weekend_nights` | int | Number of weekend nights stayed or booked | `0` | EDA / Tableau | - |
| `stays_in_week_nights` | int | Number of week nights stayed or booked | `0` | EDA / Tableau | - |
| `adults` | int | Number of adults | `2` | EDA / Tableau | - |
| `children` | float | Number of children | `0.0` | EDA | Missing values filled |
| `babies` | int | Number of babies | `0` | EDA | - |
| `country` | string | Country of origin (ISO code) | `PRT` | EDA / Tableau | Missing values handled |
| `market_segment` | string | Market segment designation | `Direct` | EDA / Tableau | - |
| `distribution_channel` | string | Booking distribution channel | `Direct` | EDA / Tableau | - |
| `is_repeated_guest` | int | Value indicating if the guest is repeated (1) or not (0) | `0` | EDA / KPI | - |
| `previous_cancellations` | int | Number of previous bookings canceled | `0` | EDA | - |
| `previous_bookings_not_canceled`| int | Number of previous bookings not canceled | `0` | EDA | - |
| `reserved_room_type` | string | Code of room type reserved | `C` | EDA | - |
| `assigned_room_type` | string | Code for the type of room assigned | `C` | EDA | - |
| `booking_changes` | int | Number of changes/amendments made to the booking | `3` | EDA | - |
| `deposit_type` | string | Type of deposit made | `No Deposit` | EDA / Tableau | - |
| `agent` | float | ID of the travel agency | `9.0` | EDA | Missing values handled |
| `days_in_waiting_list` | int | Number of days the booking was in the waiting list | `0` | EDA | - |
| `customer_type` | string | Type of booking | `Transient` | EDA / Tableau | - |
| `average_daily_rate` | float | Average Daily Rate (ADR) | `75.0` | EDA / KPI | Outliers capped |
| `required_car_parking_spaces` | int | Number of car parking spaces required | `0` | EDA | - |
| `total_of_special_requests` | int | Number of special requests made | `0` | EDA | - |
| `reservation_status` | string | Last reservation status (Canceled, Check-Out, No-Show) | `Check-Out` | EDA / Tableau | - |
| `reservation_status_date` | date | Date at which the last status was set | `2015-07-01` | EDA | Standardized to date |

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `meal_type` | Mapped from `meal` | Clearer labels for meal packages |
| `country_name` | Mapped from `country` | Full country names for easier geographic analysis |
| `total_nights` | `stays_in_weekend_nights` + `stays_in_week_nights` | Total duration of the stay |
| `total_guests` | `adults` + `children` + `babies` | Total number of individuals per booking |
| `total_revenue` | `total_nights` * `average_daily_rate` | Total estimated revenue for the booking |
| `has_children` | 1 if `children` + `babies` > 0, else 0 | Identifies family bookings |
| `is_weekend_stay` | 1 if `stays_in_weekend_nights` > 0, else 0 | Identifies bookings that include weekends |
| `has_special_requests`| 1 if `total_of_special_requests` > 0, else 0 | Indicates guests with specific needs |
| `is_direct_booking` | 1 if `distribution_channel` == 'Direct', else 0 | Indicates direct sales without intermediaries |
| `lead_time_category` | Binned `lead_time` | Groupings for booking window analysis |
| `stay_duration_category`| Binned `total_nights` | Groupings for length of stay analysis |
| `price_tier` | Binned `average_daily_rate` | Segments bookings by price range (Economy, Standard, etc) |
| `customer_segment` | Logic based on guest composition | Differentiates Families from Couples/Singles |
| `booking_type` | Derived duration and type classification | Identifies Quick Trips vs Standard Bookings |
| `season` | Mapped from `arrival_date_month` | Maps months to Summer, Winter, Spring, Autumn |
| `is_peak_season` | 1 if `season` == 'Summer', else 0 | Identifies high-demand periods |
| `revenue_per_guest` | `total_revenue` / `total_guests` | Metric of profitability per individual |
| `average_night_value` | `total_revenue` / `total_nights` | Similar to ADR but applied to derived revenue |
| `clv_proxy` | Proxy metric | Custom Customer Lifetime Value approximation |

## Data Quality Notes

- **Missing Values:** Addressed during cleaning (e.g., `children`, `country`, `agent` have specific fill values).
- **Outliers:** `average_daily_rate` may have extreme values that are treated during the EDA and Cleaning phases.
- **Derived Fields:** Multiple business logic flags (like `total_revenue`, `total_guests`, `is_weekend_stay`) were created to simplify dashboarding.