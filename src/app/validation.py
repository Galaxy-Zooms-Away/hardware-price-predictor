"""
validation.py
-------------
Quality Assurance Gatekeeper

Contains all data validation checks (Completeness, Consistency, Sanity) 
and the master runner function to enforce data health before processing.
"""
import pandas as pd

def validate_completeness(merged_df: pd.DataFrame):
    missing_rows = merged_df[['country', 'tax_rate', 'currency_rate']].isna().any(axis=1).sum()
    if missing_rows == 0:
        return
    else:
        raise ValueError(f"Validation failed.\n" 
                         f"Found {missing_rows} rows.\n"
                         f"Check lookup columns 'country', 'tax_rate', 'currency_rate' for missing values.")

def validate_consistency(raw_df: pd.DataFrame, region_df: pd.DataFrame ,merged_df:pd.DataFrame):
    raw_region_count = raw_df['region'].value_counts()
    split_region_count = region_df['region'].value_counts()
    expected_rows = raw_region_count.mul(split_region_count, fill_value=1).sum()
    actual_rows = merged_df.shape[0]
    raw_kitid_count, merged_kitid_count = raw_df['kit_id'].nunique(dropna=False), merged_df['kit_id'].nunique(dropna=False)

    if expected_rows != actual_rows:
        raise ValueError(f"Validation failed.\n"
                         f"Expected row count: {expected_rows}, Actual row count(merged data): {actual_rows}.\n"
                         f"Check the regional mapping table for duplicate/missing keys.")
    if raw_kitid_count != merged_kitid_count:
        raise ValueError(f"Validation failed.\n"
                         f"Expected unique kit_id count(raw data): {raw_kitid_count}, Actual unique kit_id count(merged data): {merged_kitid_count}.\n"
                         f"Check if the merge type is a Left join in the code.")
    return

def validate_sanity(merged_df: pd.DataFrame):
    invalid_price_count = merged_df['final_local_price'].le(0, fill_value=-1).sum()          # Using fill_value=-1 so missing values (NaN) also trigger a sanity failure.
    if invalid_price_count > 0:
        raise ValueError(f"Validation failed.\n"
                         f"{invalid_price_count} rows have invalid local prices.\n"
                         f"Check if 'price_usd', 'tax_rate', 'currency_rate' columns have negative/zero values.")
    return

def run_pipeline_validations(raw_df:pd.DataFrame, region_df:pd.DataFrame, merged_df:pd.DataFrame):
    validate_completeness(merged_df)
    validate_consistency(raw_df, region_df, merged_df)
    validate_sanity(merged_df)
    return