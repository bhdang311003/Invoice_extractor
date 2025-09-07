import streamlit as st # type: ignore
from paddleocr import PaddleOCR # type: ignore
import re
from PIL import Image # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore

ocr = PaddleOCR(use_angle_cls=True, lang='en')

#========================================================

def extract_company(ocr_lines):
    # if full uppercase
    for line in ocr_lines:
        letters = re.sub(r"[^A-Z]", "", line.upper())
        if len(letters) > 0 and len(letters) / max(len(line),1) > 0.7:
            return line.strip()
    
    for line in ocr_lines:
        if "SDN BHD" in line.upper() or "SDN. BHD." in line.upper():
            return line.strip()
    
    return None

#========================================================

def extract_date(ocr_lines):
    pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

    # Find "DATE"
    for line in ocr_lines:
        if "DATE" in line.upper():
            match = re.search(pattern, line)
            if match:
                return match.group()

    # Fallback
    for line in ocr_lines:
        match = re.search(pattern, line)
        if match:
            return match.group()
    
    return None

#========================================================

def extract_address(ocr_lines, company):
    ignore_keywords = ["TEL", "CO NO", "GST", "TAX INVOICE", "FAX", "MOBILE", "WHATAPPS"]
    addr_keywords = ["KM", "JALAN", "ROAD", "LORONG", "RAYA", "STREET", "AVENUE", "NO"]

    # find company
    start = None
    for i, line in enumerate(ocr_lines):
        if company.upper() in line.upper():
            start = i + 1
            break
    if start is None:
        return None

    candidate_lines = []
    for l in ocr_lines[start:]:
        if any(kw in l.upper() for kw in ignore_keywords):
            break
        # skip if number/symbol
        if re.fullmatch(r"[\(\)\-\w\s]+", l) and re.search(r"\d", l) and not any(kw in l.upper() for kw in addr_keywords):
            continue
        candidate_lines.append(l)

    if not candidate_lines:
        return None

    # --- Step 1: keyword ---
    address_lines = []
    collecting = False
    for line in candidate_lines:
        if not collecting:
            if any(kw in line.upper() for kw in addr_keywords):
                collecting = True
                address_lines.append(line)
        else:
            address_lines.append(line)
            if re.search(r"\b\d{5}\b", line):  # postcode
                return " ".join(address_lines)

    # --- Step 2: fallback by postcode ---
    for i, line in enumerate(candidate_lines):
        if re.search(r"\b\d{5}\b", line):
            prev = candidate_lines[max(0, i-2):i]
            return " ".join(prev + [line])

    return " ".join(candidate_lines)

#========================================================

def extract_total(texts):
    candidate = None
    skip_keywords = ["ITEM", "QTY", "QUANTITY"]

    for i, t in enumerate(texts):
        if "TOTAL" in t.upper():
            if any(kw in t.upper() for kw in skip_keywords):
                continue
            # number after "total"
            pos = t.upper().find("TOTAL") + len("TOTAL")
            after_total = t[pos:]
            numbers = re.findall(r"\d+(?:[.,]\d+)*", after_total)
            if numbers:
                candidate = numbers[0]
            else:
                if i + 1 < len(texts):
                    next_text = texts[i+1]
                    numbers = re.findall(r"\d+(?:[.,]\d+)*", next_text)
                    if numbers:
                        candidate = numbers[0]
    return candidate


# Streamlit UI

st.title("🧾 Invoice Information Extractor")
uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="🖼️ Uploaded Invoice", width=400)

    if st.button("🔍 Information Extractor"):
        with st.spinner("🔄 Processing..."):
            results = ocr.predict(np.array(image))
            texts = results[0]['rec_texts']

        # with st.expander("Show OCR Texts"):
        #     st.write(texts)

        company = extract_company(texts)
        date = extract_date(texts)
        addr = extract_address(texts, company)
        total = extract_total(texts)


        data = {
            "Field": ["🏢 Company", "📅 Date", "🏠 Address", "💰 Total"],
            "Value": [company, date, addr, total]
        }
        df = pd.DataFrame(data)

        st.subheader("📝 Extracted Entities")
        st.table(df)

