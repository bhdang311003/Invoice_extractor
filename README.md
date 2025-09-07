# 🧾 Invoice Information Extraction 🧾


## 📌 Overview  
This project demonstrates Invoice Information Extraction using OCR.
It takes scanned or photographed invoices as input and automatically extracts key fields such as:

🏢 Company name

📅 Date

🏠 Address

💰 Total

The system is built with PaddleOCR for text recognition and simple rule-based extraction (regex and keyword matching).
It serves as a lightweight proof-of-concept for real-world document understanding tasks.

<p align="center">
  <img width="604" height="814" alt="image" src="https://github.com/user-attachments/assets/b9d44cce-f7ac-4519-a923-93d2bcbcd074" />
</p>


## 🔑 Key points:
- Built an OCR pipeline with PaddleOCR to extract text from invoices.
- Extracted key fields (company, date, address, total) using regex + rule-based logic.
- Prepared and handled annotated data in JSON/TXT format.
- Deployed a simple Streamlit app for interactive demo.

## Project Structure
```
📂 Project Root
├── 📂 Data
│   ├── 📂 box
│   │       ├── x.txt
│   │       └── ....
│   ├── 📂 entities
│   │       ├── x.txt
│   │       └── ....
│   └── 📂 img
│           ├── x.jpg
│           └── ....
├── invoice_extractor.py
├── requirements.txt
└── README.md
```
## Dataset
### The dataset used in this project is publicly available on Kaggle
**Download Instructions**
1. Go to the Kaggle dataset page: [SROIE datasetv2 (Kaggle)](https://www.kaggle.com/datasets/urbikn/sroie-datasetv2).
3. Download the dataset ZIP file.
4. Extract the Test folder into the Data/ folder of this repository.


### Requirements
Modules and dependencies in `requirements.txt`
  ```
  pip install -r requirements.txt
  ```

### Deploy web application:

- If testing streamlit successfully, open terminal and run:
```
streamlit run invoice_extractor.py
```
- Open browser and go to http://localhost:8501/

- Then, launch the app 😍










