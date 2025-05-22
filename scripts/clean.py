import pandas as pd
import numpy as np

def convert_to_datetime(df):
    cols_to_convert = [col for col in df.columns if 'date' in col.lower()]
    if cols_to_convert:
        for col in cols_to_convert:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except Exception as e:
                print(f'Error during the conversion of the column {col}')
    else:
        print('No date columns detected')

def clean_data(df):
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    convert_to_datetime(df)

    numeric_cols = ['policy_annual_premium', 'total_claim_amount', 'injury_claim', 'property_claim', 'vehicle_claim']
    for num_col in numeric_cols:
        if num_col in df.columns:
            df[num_col] = df[num_col].astype(str).str.replace(',', '.', regex=False)
            df[num_col] = pd.to_numeric(df[num_col], errors='coerce')

    df['police_report_available'] = df['police_report_available'].str.replace('?', 'UNKNOWN')

    dummies = pd.get_dummies(df['police_report_available'], prefix='police_report_available')
    df = pd.concat([df, dummies], axis=1)

    df['police_report_available'] = df['police_report_available'].map({
        'YES': 1,
        'NO': 0,
        'UNKNOWN': -1
    })

    df['fraud_reported'] = df['fraud_reported'].apply(lambda x: x.upper()).map({
        'Y': 1,
        'N': 0
    })

    if 'auto_year' in df.columns:
        df['auto_year'] = pd.to_numeric(df['auto_year'], errors='coerce')

    df.drop_duplicates(inplace=True)

    return df