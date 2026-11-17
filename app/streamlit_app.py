import pandas as pd
import streamlit as st

st.set_page_config(page_title="Mandi Saathi", page_icon="🌾")

st.title("🌾 Mandi Saathi")
st.write("Buldhana ke mandi bhav dekhein.")
st.caption("Source: data.gov.in / AGMARKNET")

# App ke liye taiyaar ki gayi CSV file padho
prices = pd.read_csv("data/processed/mandi_prices_app.csv")

# CSV ki date ko Python ki date mein badlo
prices["Arrival_Date"] = pd.to_datetime(
    prices["Arrival_Date"],
    dayfirst=True,
    errors="coerce",
)

# Fasal ke naam ke aage-peeche ke extra spaces hatao
prices["Commodity"] = prices["Commodity"].astype(str).str.strip()

crop_names = {
    "Soybean": "Soyabean",
    "Cotton": "Cotton",
    "Tur (Arhar)": "Tur",
    "Onion": "Onion",
    "Turmeric": "Turmeric",
}

crop = st.selectbox("Fasal chuno", list(crop_names.keys()))
data_crop_name = crop_names[crop]

# Chuni hui fasal ka data rakho
crop_prices = prices[
    prices["Commodity"].str.casefold() == data_crop_name.casefold()
].copy()

if crop_prices.empty:
    st.info(
        f"{crop} ka data abhi file mein nahi hai. "
        "Filhal Buldhana ka Soybean data available hai."
    )
    st.stop()

# Is fasal ke liye available mandi chuno
markets = sorted(crop_prices["Market_Clean"].dropna().unique())
market = st.selectbox("Mandi chuno", markets)

# Chuni hui mandi ke records, latest date pehle
market_prices = crop_prices[
    crop_prices["Market_Clean"] == market
].sort_values("Arrival_Date", ascending=False)

latest = market_prices.iloc[0]

st.subheader(market)
st.caption(
    "Is mandi ka aakhri available record: "
    + latest["Arrival_Date"].strftime("%d-%m-%Y")
)

col1, col2, col3 = st.columns(3)
col1.metric("Modal bhav", f"₹{int(latest['Modal_Price']):,}")
col2.metric("Minimum bhav", f"₹{int(latest['Min_Price']):,}")
col3.metric("Maximum bhav", f"₹{int(latest['Max_Price']):,}")

# Mandi ke purane bhav ki table
history = market_prices[
    ["Arrival_Date", "Grade", "Variety", "Min_Price", "Max_Price", "Modal_Price"]
].copy()

history["Arrival_Date"] = history["Arrival_Date"].dt.strftime("%d-%m-%Y")

history = history.rename(
    columns={
        "Arrival_Date": "Tarikh",
        "Grade": "Grade",
        "Variety": "Variety",
        "Min_Price": "Minimum bhav",
        "Max_Price": "Maximum bhav",
        "Modal_Price": "Modal bhav",
    }
)

st.subheader("Pichhle mandi bhav")
st.dataframe(history, use_container_width=True, hide_index=True)