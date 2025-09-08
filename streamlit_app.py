import streamlit as st
import google.generativeai as genai
import os

# API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("📐 WoodWOP MPR Generator (Gemini Flash)")

uploaded_file = st.file_uploader("Įkelk brėžinio screenshotą", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Įkeltas brėžinys", use_container_width=True)

    if st.button("Generuoti MPR"):
        image_bytes = uploaded_file.getvalue()

        # Naudojam lengvesnį modelį
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            [
                "Sugeneruok tinkamą WoodWOP .mpr failą pagal šį brėžinį. Vadovaukis MPR PDF specifikacija.",
                {"mime_type": "image/png", "data": image_bytes}
            ],
            generation_config={"max_output_tokens": 1200}
        )

        mpr_code = response.text

        st.code(mpr_code, language="plaintext")

        st.download_button(
            label="⬇️ Atsisiųsti MPR",
            data=mpr_code,
            file_name="detail.mpr",
            mime="text/plain"
        )
