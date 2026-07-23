"""
pipeline.py
-----------
ETL Operations & Workflow Orchestrator

Handles end-to-end processing steps: loading raw CSVs, executing business 
logic/transformations, invoking quality checks, and exporting clean data.
"""
import pandas as pd
from src.app.validation import run_pipeline_validations

def run_pipeline():
    raw_df = pd.read_csv("data/raw/Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv")
    region_df = pd.read_csv("data/external/regional_market_map.csv")

    merged_df = pd.merge(raw_df, region_df, how='left', on='region')
    merged_df['final_local_price'] = ((merged_df['price_usd'] * merged_df['tax_rate']) * merged_df['currency_rate']).round(2)

    run_pipeline_validations(raw_df=raw_df, region_df=region_df, merged_df=merged_df)

    merged_df.to_csv("data/processed/hardware_prices_processed.csv",index=False)