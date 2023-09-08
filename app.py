import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from langdetect import detect
import pyttsx3
from googletrans import Translator
import openai

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to extract text from a Word document
def extract_text_from_docx(docx_file):
    text = ""
    doc = Document(docx_file)
    for para in doc.paragraphs:
        text += para.text
    return text

def simplify_summary(summary):
    return summary


def simplify_and_translate_summary(summary, target_language):
    slan=target_language.lower()
    lan=["telugu","te","english","en","kannada","kn","malayalam","ml","hindi","hi","tamil","ta"]
    translator = Translator()

    translated_summary = translator.translate(summary, dest=lan[lan.index(slan) +1]).text
    return translated_summary


def summarize_wit(input_text, api_key):
    openai.api_key = api_key
    
    prompt = f"assume that you are third person, study the follow content and generate brief summary in a single para:\n\n{input_text}"
    
    max_tokens = 250 
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None
    )
    
    summary = response.choices[0].text.strip()
    return summary


api_key = "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"

def main():      
    st.image("klu.png", use_column_width=True)
    st.markdown("""<p align='center' style='font-size:45px; font-family: Georgia, serif'><b style='color:GREEN;'>P2F - SEMI</p>""",unsafe_allow_html=True)
    st.markdown("<h1 align='center' style='color:red; font-size:50px;'><ins>KARE-P2F CAMPUS <br>HACKATHON</ins></h1>",unsafe_allow_html=True)
    st.markdown("<h2 align='center'' style='font-size:45px; color:ORANGE'>Document Summarization App</h2>",unsafe_allow_html=True)
    st.markdown("<h5 align='center'' style='color:WHITE'>An app that simplifies PDFs/Word docs into kid-friendly summaries with text-to-speech and multi-language support.</h5>",unsafe_allow_html=True)
    st.markdown("---")
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF or Word document", type=["pdf", "docx"])

    if uploaded_file:
        # Check file type and extract text
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == "pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension == "docx":
            text = extract_text_from_docx(uploaded_file)

        # Generate a summary (simplified)
        words = text.split()
        summary = ' '.join(words)

        summary = summarize_wit(summary, api_key)
        
        simplified_summary = simplify_summary(summary)
        target_language = st.selectbox("Select Target Language", ["English", "Hindi", "Tamil", "Telugu","Kannada","Malayalam"])

        # Simplify and translate the summary
        translated_summary = simplify_and_translate_summary(simplified_summary, target_language)

        st.write("## Simplified and Translated Summary")
        st.write(translated_summary)

        st.write("## Download Simplified Summary")
        download_button = st.download_button(
            label="Download Summary",
            data=translated_summary.encode('utf-8'),
            file_name="simplified_summary.txt",
            key="download_button"
        )
        st.subheader("Guide :")
        a1,b1,c1=st.columns(3)
        b1.image("raja.jpeg",caption="R Raja Subramanian")

        st.subheader("Team Members : ")
        a,b,c,d=st.columns(4)
        a.image("yas.png",caption="MANCHALA YASWANTH")
        b.image("avi.jpg",caption="JINKA THE AVIRAJ")
        c.image("gautham.jpg",caption="GOUTHAM SANKAR S")
        d.image("sai.jpg",caption="ASAPU SAI KUMAR")

if __name__ == "__main__":
    main()
