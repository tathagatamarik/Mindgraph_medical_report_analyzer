import streamlit as st
import requests
from PIL import Image
import fitz
from io import BytesIO

st.set_page_config(page_title="🩺 Medical Report Explainer", layout="centered")
st.title("🧠 AI-Powered Medical Report Summarizer")
st.markdown("Upload any medical report (PDF or image), and AI will summarize it in plain language.")

uploaded_file = st.file_uploader("📤 Upload Report (Image or PDF)", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        st.markdown("#### 📄 PDF Preview:")
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pix = page.get_pixmap()
            img = Image.open(BytesIO(pix.tobytes("png")))
            st.image(img, use_column_width=True)
        uploaded_file.seek(0)  # reset file pointer
    else:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

    st.markdown("---")
    if st.button("🧠 Analyze with AI"):
        with st.spinner("Analyzing report using GPT-4 Vision..."):
            files = {"file": uploaded_file.getvalue() if hasattr(uploaded_file, 'getvalue') else uploaded_file}
            try:
                res = requests.post("http://localhost:5000/analyze", files=files)
                result = res.json()
                if "summary" in result:
                    st.success("✅ Summary Generated")
                    st.markdown(result["summary"])
                else:
                    st.error(result.get("error", "Something went wrong"))
            except Exception as e:
                st.error(f"Error: {e}")
