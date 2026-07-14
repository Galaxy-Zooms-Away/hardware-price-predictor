import pandas as pd

# read the file
dfile = pd.read_csv("data/raw/Ultimate_Memory_Shortage_Crisis_Dataset_10k.csv")
# Checking unique region names
print(f"Unique regions in data: {dfile['region'].unique()}")
# check and see if price_usd has null values
print(dfile['price_usd'].isna().sum())

# The regions are split into some countries with their corresponding tax rates. 
# For the project, this data is going to a CSV file.
regional_market_map = {
    'North America': [
        {'country': 'United States', 'code': 'US', 'tax_rate': 1.00, 'currency_rate': 1.00, 'currency_code': 'USD'},
        {'country': 'Canada', 'code': 'CA', 'tax_rate': 1.12, 'currency_rate': 1.37, 'currency_code': 'CAD'}
    ],
    'Europe': [
        {'country': 'Germany', 'code': 'DE', 'tax_rate': 1.19, 'currency_rate': 0.92, 'currency_code': 'EUR'},
        {'country': 'United Kingdom', 'code': 'GB', 'tax_rate': 1.20, 'currency_rate': 0.78, 'currency_code': 'GBP'}
    ],
    'Asia-Pacific': [
        {'country': 'India', 'code': 'IN', 'tax_rate': 1.18, 'currency_rate': 83.50, 'currency_code': 'INR'},
        {'country': 'Japan', 'code': 'JP', 'tax_rate': 1.10, 'currency_rate': 160.00, 'currency_code': 'JPY'}
    ],
    'Greater China': [
        {'country': 'China', 'code': 'CN', 'tax_rate': 1.13, 'currency_rate': 7.25, 'currency_code': 'CNY'},
        {'country': 'Taiwan', 'code': 'TW', 'tax_rate': 1.05, 'currency_rate': 32.50, 'currency_code': 'TWD'}
    ],
    'Latin America': [
        {'country': 'Brazil', 'code': 'BR', 'tax_rate': 1.20, 'currency_rate': 5.50, 'currency_code': 'BRL'},
        {'country': 'Mexico', 'code': 'MX', 'tax_rate': 1.16, 'currency_rate': 18.20, 'currency_code': 'MXN'}
    ],
    'EMEA': [
        {'country': 'United Arab Emirates', 'code': 'AE', 'tax_rate': 1.05, 'currency_rate': 3.67, 'currency_code': 'AED'},
        {'country': 'South Africa', 'code': 'ZA', 'tax_rate': 1.15, 'currency_rate': 18.00, 'currency_code': 'ZAR'}
    ]
}
# The following code is for converting a nested dictionary like the above to a DataFrame.

# to_normalize_map = [{'region': region, 'countries':countries} for region, countries in regional_market_map.items()]
# ^ List comprehension to get a format friendly for json_normalize to read.
# For pd.json_normalize() to map these parameters successfully, it expects a list of dictionaries 
# as its primary input, where each dictionary represents a distinct group. 
# For example, it wants a structure that looks like this:
# Python

# data_for_normalize = [
#     {
#         'region': 'North America', 
#         'countries': [
#             {'country': 'United States', 'code': 'US', ...},
#             {'country': 'Canada', 'code': 'CA', ...}
#         ]
#     },
#     {
#         'region': 'Europe', 
#         'countries': [
#             {'country': 'Germany', 'code': 'DE', ...}
#         ]
#     }
# ]

# If you hand Pandas a list structured exactly like data_for_normalize above, you can simply tell it:

# “Hey Pandas, look inside the 'countries' list to make my rows (record_path),
# and make sure to bring the 'region' string along as a separate column for each of those rows (meta).”
# marketmap_df = pd.json_normalize(to_normalize_map, record_path='countries', meta='region')
