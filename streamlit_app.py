import streamlit as st
from openai import OpenAI
import os, base64

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("📐 WoodWOP MPR Generator")

uploaded_file = st.file_uploader("Įkelk brėžinio screenshotą", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Įkeltas brėžinys", use_container_width=True)

    if st.button("Generuoti MPR"):
        image_base64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Tu esi CNC WoodWOP .mpr failų generatorius. Vadovaukis woodWOP MPR PDF specifikacija."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Sugeneruok tinkamą .mpr failą pagal šį brėžinį."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ]
                }
            ],
            max_tokens=1500
        )

        mpr_code = response.choices[0].message.content

        st.code(mpr_code, language="plaintext")

        st.download_button(
            label="⬇️ Atsisiųsti MPR",
            data=mpr_code,
            file_name="detail.mpr",
            mime="text/plain"
        )
