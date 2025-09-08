import streamlit as st
import openai
import os

# API raktas iš Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📐 WoodWOP MPR Generator")

uploaded_file = st.file_uploader("Įkelk brėžinio screenshotą", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Įkeltas brėžinys", use_column_width=True)

    if st.button("Generuoti MPR"):
        # Paverčiam failą į bytes
        image_bytes = uploaded_file.getvalue()

        # Siunčiam į GPT Vision
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Tu esi CNC WoodWOP .mpr failų generatorius. Vadovaukis woodWOP MPR PDF specifikacija."},
                {"role": "user", "content": "Sugeneruok tinkamą .mpr failą pagal šį brėžinį."}
            ],
            max_tokens=1500,
            # pridėtas paveikslas
            files=[{"name": "drawing.png", "bytes": image_bytes}]
        )

        mpr_code = response["choices"][0]["message"]["content"]

        # Rodyti kodą
        st.code(mpr_code, language="plaintext")

        # Duoti atsisiųsti
        st.download_button(
            label="⬇️ Atsisiųsti MPR",
            data=mpr_code,
            file_name="detail.mpr",
            mime="text/plain"
        )
