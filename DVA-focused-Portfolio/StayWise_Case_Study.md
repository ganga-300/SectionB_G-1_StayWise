# StayWise Portfolio Case Study

## Problem Statement and Stakeholder Context
The hospitality industry faces significant challenges with booking cancellations, which lead to lost revenue and suboptimal resource allocation. This project aims to analyze historical booking data for City and Resort hotels to uncover key drivers of cancellations, customer behavior patterns, and seasonal demand. The insights are intended to support stakeholders (e.g., hotel managers, marketing teams) in optimizing pricing strategies and targeted promotions.

## Dataset Source and Scope
- **Source**: Hotel Bookings Dataset (`hotel_bookings_Raw.csv`)
- **Scope**: Contains 119,209 booking records with 49 features spanning from 2015 to 2017. The data includes reservation status, lead time, guest demographics, and booking channels.

## Cleaning and Transformation Summary
- **Data Quality**: Addressed missing values (e.g., `children`, `country`), removed duplicates, and handled outliers (e.g., capping extreme `average_daily_rate`).
- **Feature Engineering**: Created multiple derived fields for analysis including `total_nights`, `total_guests`, `total_revenue`, `season`, `is_peak_season`, and `clv_proxy`.

## KPI Framework
- **Cancellation Rate %**: Measures the severity of booking fall-throughs. Computed as `sum(is_canceled) / count(total_bookings) * 100`.
- **Total Revenue**: Measures gross financial value generated per booking period. Computed as `(weekend_nights + week_nights) * ADR`.
- **Revenue per Guest**: Evaluates relative profitability of different demographic segments. Computed as `total_revenue / total_guests`.
- **CLV Proxy**: Estimates realized economic value, netting out revenue lost to cancellations. Computed as `total_revenue * (1 - is_canceled)`.

## 3-5 Key Insights
1. **Cancellation Rates**: City Hotels experience a significantly higher cancellation rate compared to Resort Hotels.
2. **Lead Time Impact**: Bookings with a longer lead time (especially >180 days) show a proportionately higher risk of cancellation.
3. **Seasonal Trends**: Summer months (July/August) represent the peak season for both bookings and total revenue.
4. **Booking Channels**: Direct bookings exhibit lower cancellation rates compared to those made through Travel Agents/Tour Operators.

## Tableau Dashboard

**Screenshots**:
![StayWise Dashboard Screenshot](../tableau/screenshots/StayWise.pdf)

**Dashboard Link**:
- [Dashboard 1: Executive Summary View](https://public.tableau.com/app/profile/soumen.dass/viz/StayWise-new1/StayWise-1)
- [Dashboard 2: Operational Drill-Down View](https://public.tableau.com/app/profile/soumen.dass/viz/StayWise-new2/StayWise-2)

## Recommendations and Expected Impact
- **Deposit Strategies**: Implement stricter non-refundable deposit policies for long lead-time bookings or specific high-risk market segments.
- **Targeted Promotions**: Offer incentives for direct bookings to reduce reliance on third-party channels and decrease overall cancellation rates.
- **Resource Allocation**: Scale operational staff and inventory dynamically based on derived seasonal trends.
