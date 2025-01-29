import streamlit as st
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_bytes
import os

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin" 

def get_gemini_response(image, prompt):
    response = model.generate_content([image, prompt])
    return response.text

st.set_page_config(page_title="CNE", layout="wide")
st.header("Container Number Extractor (CNE)")


uploaded_file = st.file_uploader("Upload Image or PDF", type=['jpg', 'png', 'jpeg', 'webp', 'pdf'])

col1, col2 = st.columns([1, 1]) 

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf": 
        st.write("Processing PDF file...")
        try:
            
            images = convert_from_bytes(uploaded_file.read(), poppler_path=POPPLER_PATH)
            if images:
                with col1:
                    st.image(images[0], caption="First Page of Uploaded PDF", use_column_width=True)
                image = images[0]
            else:
                st.error("No pages found in the PDF.")
        except Exception as e:
            st.error(f"Failed to process PDF: {e}")
    else:  
        image = Image.open(uploaded_file)
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Start the Extraction")

prompt = (
    "Give me the output of the Container details in structured JSON format " 
)

if submit and uploaded_file is not None:
    try:
        response = get_gemini_response(image, prompt)
        with col2: 
            st.markdown(response, unsafe_allow_html=False)

        file_name = "container_details.json"
        st.download_button(
            label="Download JSON",
            data=response,  
            file_name=file_name, 
            mime="application/json"  
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown(""" *Developed by: Sarawin* """)