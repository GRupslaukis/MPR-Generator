import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import base64, os

# API raktai iš Streamlit secrets
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# Įkeliame taisykles iš PDF (supaprastintas tekstas)
with open("mpr_rules.txt", "r", encoding="utf-8") as f:
    MPR_RULES = f.read()

st.title("📐 WoodWOP MPR Generator (Gemini + DeepSeek)")

uploaded_file = st.file_uploader("Įkelk brėžinio screenshotą", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Įkeltas brėžinys", use_container_width=True)

    if st.button("Generuoti MPR"):
        # 1️⃣ Gemini – nuskaitymas
        image_bytes = uploaded_file.getvalue()
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")

        gemini_response = gemini_model.generate_content(
            [
                "Iš šio brėžinio ištrauk JSON su ruošinio dydžiu, storiu, skylėmis (X,Y, diametras, gylis) ir kišenėmis (X,Y, ilgis, plotis, spindulys, gylis). Jokio papildomo teksto.",
                {"mime_type": "image/png", "data": image_bytes}
            ],
            generation_config={"max_output_tokens": 1000}
        )

        geometry_json = gemini_response.text
        st.subheader("🔍 Atpažinta geometrija (JSON)")
        st.code(geometry_json, language="json")

        # 2️⃣ DeepSeek – MPR generacija
        deepseek_response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"Tu esi CNC WoodWOP MPR failų generatorius. Vadovaukis šiomis taisyklėmis:\n{MPR_RULES}"},
                {"role": "user", "content": f"Paversk šiuos duomenis į galutinį .mpr failo turinį:\n{geometry_json}"}
            ],
            max_tokens=1500
        )

        mpr_code = deepseek_response.choices[0].message.content

        st.subheader("📄 Sugeneruotas MPR kodas")
        st.code(mpr_code, language="plaintext")

        st.download_button(
            label="⬇️ Atsisiųsti MPR",
            data=mpr_code,
            file_name="detail.mpr",
            mime="text/plain"
        )
