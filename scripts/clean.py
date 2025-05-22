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
        
def categorize_customer_tenure(months):
    if months <= 100:
        return 'New'
    elif months <= 200:
        return 'Recent'
    elif months <= 300:
        return 'Established'
    else:
        return 'Loyal'

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
    
    df['male'] = df['insured_sex'].map({'MALE': 1, 'FEMALE': 0})
    df.drop(columns=['insured_sex'], inplace=True)
    
    advanced_levels = ['PhD', 'MD', 'JD', 'Masters']
    df['education_advanced'] = df['insured_education_level'].apply(
        lambda x: 1 if x in advanced_levels else 0
    )
    df.drop(columns=['insured_education_level'], inplace=True)

    
    df['customer_tenure'] = df['months_as_customer'].apply(categorize_customer_tenure)
    #df.drop(columns=['months_as_customer'], inplace=True)
    
    dummies = pd.get_dummies(df['customer_tenure'], columns=['customer_tenure'], drop_first=True)
    df = pd.concat([df, dummies], axis=1)
    
    high_risk_models = ['X6', 'ML350', 'C300', 'Tahoe', 'Silverado', 'F150', 'Civic', 'A5', 'M5']
    df['auto_model_risk'] = df['auto_model'].apply(lambda x: 1 if x in high_risk_models else 0)

    if 'auto_year' in df.columns:
        df['auto_year'] = pd.to_numeric(df['auto_year'], errors='coerce')
        
    cat_vars = [
        'collision_type',
        'property_damage',
        'incident_severity',
        'authorities_contacted',
        'insured_relationship',
        'insured_occupation'
    ]
    df[cat_vars] = df[cat_vars].replace('?', 'UNKNOWN')
    dummies = pd.get_dummies(df[cat_vars], drop_first=True, prefix=cat_vars)
    df = pd.concat([df, dummies], axis=1)
    

    df.replace("?", np.nan, inplace=True)
    nonsense_values = ["unknown", "none", "n/a"]
    df.replace(nonsense_values, np.nan, inplace=True)



    df.drop_duplicates(inplace=True)

    return df