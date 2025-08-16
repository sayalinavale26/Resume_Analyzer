import pandas as pd
import re
import argparse
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def analyze_resume(resume_text, skills_file="skills.csv"):
    df = pd.read_csv(skills_file)
    required_skills = df['Skill'].str.lower().tolist()
    
    resume_text = resume_text.lower()
    found = []
    missing = []
    
    for skill in required_skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
            found.append(skill)
        else:
            missing.append(skill)
    
    score = round(len(found) / len(required_skills) * 100, 2)
    
    print("\n✅ Skills Found:", found)
    print("❌ Missing Skills:", missing)
    print(f"📊 Match Score: {score}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", help="Path to resume file (.txt or .pdf)")
    args = parser.parse_args()
    
    if args.resume.endswith(".pdf"):
        resume_text = extract_text_from_pdf(args.resume)
    else:
        with open(args.resume, "r", encoding="utf-8") as f:
            resume_text = f.read()
    
    analyze_resume(resume_text)
    