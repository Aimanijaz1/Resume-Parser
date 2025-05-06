from flask import Flask, render_template, request, redirect, url_for
import os
import re
import spacy
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load skills from skills.txt
with open('skills.txt', 'r') as f:
    skills_list = [line.strip() for line in f.readlines()]

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_contact_number_from_resume(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills_from_resume(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        if re.search(pattern, text, re.IGNORECASE):
            skills.append(skill)
    return skills

def extract_education_from_resume(text):
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    return [match.strip() for match in matches]

def extract_name(resume_text):
    # Look at the first few lines only (first 5 lines)
    lines = resume_text.strip().split('\n')[:5]

    for line in lines:
        line = line.strip()
        # Match a likely name pattern: two capitalized words
        match = re.match(r'^([A-Z][a-z]+ [A-Z][a-z]+)$', line)
        if match:
            name_candidate = match.group(1)
            # Filter out common false positives
            if name_candidate.lower() not in ['sql injection', 'top skills', 'resume', 'curriculum vitae']:
                return name_candidate

    # fallback: use spaCy to try from whole text
    doc = nlp(resume_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()

    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            text = extract_text_from_pdf(filepath)
            name = extract_name(text)
            contact_number = extract_contact_number_from_resume(text)
            email = extract_email_from_resume(text)
            skills = extract_skills_from_resume(text, skills_list)
            education = extract_education_from_resume(text)

            return render_template('index.html', name=name, contact_number=contact_number, email=email, skills=skills, education=education)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
