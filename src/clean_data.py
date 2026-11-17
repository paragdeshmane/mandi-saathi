import pandas as pd

prices = pd.read_csv("data/raw/mandi_prices_sample.csv")

prices["Market_Clean"] = (
    prices["Market"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)
prices_clean = prices.copy()
prices_clean["Market"] = prices_clean["Market_Clean"]

rows_before = len(prices_clean)
prices_clean = prices_clean.drop_duplicates()

print("Exact duplicates removed:", rows_before - len(prices_clean))
print("Rows remaining:", len(prices_clean))

print("Rows and columns:", prices.shape)
print("Column names:", list(prices.columns))
print(prices.head())

print("Crop names and row counts:")
print(prices["Commodity"].value_counts())

date_values = pd.to_datetime(prices["Arrival_Date"], dayfirst=True, errors="coerce")
print("Date range:", date_values.min(), "to", date_values.max())

important_columns = [
    "Arrival_Date",
    "Commodity",
    "Market",
    "Min_Price",
    "Max_Price",
    "Modal_Price",
]

print("Missing values per column:")
print(prices[important_columns].isna().sum())
print("Invalid dates:", date_values.isna().sum())

key_columns = ["Arrival_Date", "Market_Clean", "Commodity", "Variety", "Grade"]
duplicate_count = prices.duplicated(subset=key_columns).sum()

print("Duplicate rows:", duplicate_count)

duplicate_rows = prices[
    prices.duplicated(subset=key_columns, keep=False)
]

show_columns = ["Arrival_Date", "Market", "Grade", "Min_Price", "Max_Price", "Modal_Price"]
duplicate_sample = duplicate_rows.sort_values(key_columns)
print(duplicate_sample[show_columns].head(20).to_string(index=False))

print("Exact duplicate rows:", prices.duplicated().sum())

outside_range = prices[
    (prices["Modal_Price"] < prices["Min_Price"])
    | (prices["Modal_Price"] > prices["Max_Price"])
]

print("Modal price outside min/max:", len(outside_range))
outside_range = prices[
    (prices["Modal_Price"] < prices["Min_Price"])
    | (prices["Modal_Price"] > prices["Max_Price"])
]
print("Modal price outside min/max:", len(outside_range))

non_positive_prices = prices[
    (prices["Min_Price"] <= 0)
    | (prices["Max_Price"] <= 0)
    | (prices["Modal_Price"] <= 0)
]
print("Rows with zero/negative prices:", len(non_positive_prices))

non_positive_prices = prices[
    (prices["Min_Price"] <= 0)
    | (prices["Max_Price"] <= 0)
    | (prices["Modal_Price"] <= 0)
]
print("Rows with zero/negative prices:", len(non_positive_prices))

print("Market names and row counts:")
print(prices["Market"].value_counts().to_string())

print("Names after space cleanup:")
print(prices["Market_Clean"].value_counts().to_string())

exact_after_clean = prices.drop(columns=["Market"]).duplicated().sum()
print("Exact duplicates after market cleanup:", exact_after_clean)

prices_clean.to_csv("data/processed/mandi_prices_clean.csv", index=False)
print("Clean file saved. Rows:", len(prices_clean))

key_columns = [
    "Arrival_Date",
    "Commodity",
    "Market_Clean",
    "Grade",
    "Variety",
]

review_rows = prices_clean[
    prices_clean.duplicated(subset=key_columns, keep=False)
]

review_rows.to_csv("data/processed/records_to_review.csv", index=False)
print("Records to review:", len(review_rows))

prices_for_app = prices_clean.drop_duplicates(
    subset=key_columns,
    keep=False
)
prices_for_app.to_csv("data/processed/mandi_prices_app.csv", index=False)
print("Rows for app:", len(prices_for_app))