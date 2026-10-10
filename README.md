# AI Resume Analyzer and Job Recommendation System

A local Streamlit application that analyzes PDF and DOCX resumes, detects skills, estimates job-role matches, identifies skill gaps, and recommends a learning roadmap.

## Features

- PDF and DOCX resume upload
- Resume text extraction and cleaning
- Skill detection using a controlled dictionary
- Job-role matching using required-skill coverage and TF-IDF cosine similarity
- Top-three job recommendations
- Missing-skill identification and learning roadmap
- Downloadable formatted PDF analysis report

## Technologies Used

- Python
- Streamlit
- Pandas
- scikit-learn
- Plotly
- PDF and DOCX parsing libraries

## Requirements

- Python 3.10 or newer
- Internet connection to install dependencies
- No paid AI API required

## Installation and Setup (Windows)

Open Command Prompt in the project folder and run each command separately:

```bash
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Run Tests

```bash
pytest -q
```

## Scoring Method

The match estimate combines required-skill coverage (70%) and TF-IDF cosine similarity (30%). Scores are project-defined educational estimates, not hiring probabilities.

## Project Structure

- `app.py` — Streamlit interface
- `resume_parser.py` — PDF/DOCX text extraction
- `text_cleaner.py` — Text normalization
- `skill_extractor.py` — Skill detection
- `job_matcher.py` — Job-role scoring and ranking
- `roadmap_generator.py` — Learning roadmap
- `report_generator.py`— PDF report generation 
- `data/` — Job-role dataset and skill dictionary
- `tests/` — Automated tests and test cases
- `sample_resumes/` — Synthetic sample resume

## Limitations

- Scanned PDFs may require OCR, which is not included.
- Skill detection depends on the controlled dictionary and aliases.
- A missing detected skill does not prove that a person lacks that ability.
- Job roles and skill requirements come from a small curated dataset, not live job listings.
- Uploaded resumes are processed within the app session; hosting and browser environments may have their own data-handling policies.

## Responsible Use

This project is intended for educational career guidance. Its scores should not be used as the sole basis for hiring decisions.

## Author

V.A.JUNI BUVANAKAR

*junibuvanakar06@gmail.com*
