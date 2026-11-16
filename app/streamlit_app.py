import streamlit as st

st.title("Mandi Saathi")
st.write("Maharashtra ke mandi bhav yahan dikhaye jayenge.")
st.info("Abhi official mandi data add nahi hua hai.")
crop = st.selectbox("Fasal chuno", ["Soybean", "Cotton", "Tur (Arhar)", "Onion", "Turmeric"])
st.write("Tumne chuna:", crop)