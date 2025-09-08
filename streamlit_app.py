import streamlit as st

st.title("📐 MPR Generator")

uploaded_file = st.file_uploader("Įkelk brėžinio screenshotą", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Įkeltas brėžinys", use_column_width=True)
    st.success("Failas įkeltas – čia vėliau bus MPR generacija.")
