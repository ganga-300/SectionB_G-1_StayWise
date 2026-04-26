import argparse
from pathlib import Path
import pandas as pd
import numpy as np

def normalize_columns(df):
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result

def clean_missing_and_outliers(df):
    if 'company' in df.columns:
        df = df.drop(columns=['company'])
        
    if 'children' in df.columns:
        df['children'] = df['children'].fillna(0).astype(int)
    if 'country' in df.columns:
        df['country'] = df['country'].fillna('Unknown')
    if 'agent' in df.columns:
        df['agent'] = df['agent'].fillna(0)
        
    if 'adr' in df.columns:
        df = df.rename(columns={'adr': 'average_daily_rate'})
    
    if 'average_daily_rate' in df.columns:
        df.loc[df['average_daily_rate'] < 0, 'average_daily_rate'] = 0
        df.loc[df['average_daily_rate'] > 5000, 'average_daily_rate'] = 5000
        
    df = df.drop_duplicates().reset_index(drop=True)
    return df

def feature_engineering(df):
    if 'stays_in_weekend_nights' in df.columns and 'stays_in_week_nights' in df.columns:
        df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
        df['is_weekend_stay'] = (df['stays_in_weekend_nights'] > 0).astype(int)
        
    if 'adults' in df.columns and 'children' in df.columns and 'babies' in df.columns:
        df['total_guests'] = df['adults'] + df['children'] + df['babies']
        df['has_children'] = ((df['children'] + df['babies']) > 0).astype(int)
        
    if 'total_nights' in df.columns and 'average_daily_rate' in df.columns:
        df['total_revenue'] = df['total_nights'] * df['average_daily_rate']
        df['revenue_per_guest'] = np.where(df['total_guests'] > 0, df['total_revenue'] / df['total_guests'], 0)
        
    if 'arrival_date_month' in df.columns:
        summer_months = ['June', 'July', 'August']
        df['season'] = df['arrival_date_month'].apply(
            lambda x: 'Summer' if x in summer_months else 
                      'Winter' if x in ['December', 'January', 'February'] else
                      'Spring' if x in ['March', 'April', 'May'] else 'Autumn'
        )
        df['is_peak_season'] = df['season'].apply(lambda x: 1 if x == 'Summer' else 0)

    if 'total_revenue' in df.columns and 'is_canceled' in df.columns:
        df['clv_proxy'] = df['total_revenue'] * (1 - df['is_canceled'])

    return df

def build_clean_dataset(input_path):
    df = pd.read_csv(input_path)
    df = normalize_columns(df)
    df = clean_missing_and_outliers(df)
    df = feature_engineering(df)
    return df

def save_processed(df, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=False, default=Path("data/raw/hotel_bookings_Raw.csv"), type=Path)
    parser.add_argument("--output", required=False, default=Path("data/processed/hotel_bookings_cleaned.csv"), type=Path)
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"Loading dataset from {args.input}")
    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
