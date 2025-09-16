import streamlit as st
import fitz  # PyMuPDF
import csv

st.set_page_config(page_title="ICD-10 Medical Coder", page_icon="🩺", layout="centered")
st.title("🩺 المرمّز الطبي ICD-10")

st.write("✨ ارفع تقرير طبي (PDF) وسيتم استخراج النص ومطابقته مع الأكواد من ملف ICD-10.")

# تحميل ملف ICD-10
def load_icd10(file_path):
    codes = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # تخطي العناوين
        for row in reader:
            if len(row) >= 2:
                disease = row[0].strip().lower()
                code = row[1].strip()
                codes[disease] = code
    return codes

icd10 = load_icd10("icd10.csv")

# رفع PDF
pdf = st.file_uploader("📂 ارفع التقرير الطبي (PDF)", type=["pdf"])

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.lower()

if pdf:
    text = extract_text_from_pdf(pdf.read())
    found = {}
    for disease, code in icd10.items():
        if disease in text:
            found[disease] = code
    
    if found:
        st.success("✅ الأكواد المطابقة:")
        for d, c in found.items():
            st.write(f"📌 {d} → {c}")
    else:
        st.warning("🚫 لا توجد مطابقة في التقرير المرفوع.")
