# Resume Parser Web App (Dark Theme)

This is a Flask-based web application that parses uploaded PDF resumes and extracts key information using Natural Language Processing (NLP).

---

## Features

- Upload PDF resumes
- Extracted Information:
  - Name
  - Contact Number
  - Email Address
  - Skills (from a predefined list)
  - Education qualifications
- Dark-themed, modern user interface
- Background image support for enhanced UI

---

## Technologies Used

- Python
- Flask
- spaCy (en_core_web_sm)
- pdfminer.six
- HTML, CSS, Bootstrap
- Regular Expressions (Regex)

---

## How to Run

1. Clone the repository:
   git clone https://github.com/your-username/resume-parser.git

2. Navigate to the folder:
   cd resume-parser

3. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  (Windows: venv\Scripts\activate)

4. Install required packages:
   pip install -r requirements.txt

5. Download spaCy language model:
   python -m spacy download en_core_web_sm

6. Run the app:
   python app.py

7. Open in browser:
   http://127.0.0.1:5000

---

## Folder Structure

- app.py → Main Flask application
- templates/index.html → HTML interface
- static/style.css → Custom CSS
- static/background.jpg → Background image
- skills.txt → Skill keywords
- uploads/ → Folder for uploaded resumes

---

## NLP Concepts Used

- Tokenization (via spaCy)
- Named Entity Recognition (NER) for name extraction
- Regular Expressions for:
  - Contact number
  - Email address
  - Skill and education pattern matching

---
