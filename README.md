# AI Resume Analyzer and Job Recommendation System

A local Streamlit educational application that extracts text from PDF/DOCX resumes, detects skills using a controlled dictionary, compares the resume with job roles using skill coverage and TF-IDF cosine similarity, identifies skill gaps, and suggests a rule-based learning roadmap.

## Requirements
- Python 3.10 or newer
- Internet connection only for installing packages (the app itself does not require an external AI API)

## Windows setup
Open Command Prompt in this project folder:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Scoring method
`Match estimate = 70% × required-skill coverage + 30% × TF-IDF cosine similarity`, with both components scaled to 0–100. This is a documented project design choice, not a hiring probability and not a formula prescribed by the project guidance.

## Limitations
- Scanned/image-only PDFs may require OCR, which is not included in this baseline.
- Skill extraction depends on the controlled dictionary and aliases.
- Skills not detected in the resume may still be possessed by the person.
- Role requirements are a small manually curated educational dataset, not live job-market data.
- No uploaded resume is intentionally written to a permanent application folder by this code. Hosting providers and browser/session behavior may have their own data-handling policies.

## Project files
- `app.py`: Streamlit UI
- `resume_parser.py`: PDF/DOCX extraction
- `text_cleaner.py`: text normalization
- `skill_extractor.py`: controlled dictionary matching
- `job_matcher.py`: TF-IDF, cosine similarity, role scoring
- `roadmap_generator.py`: rule-based learning plan
- `report_generator.py`: downloadable text report
- `data/`: job roles and skill dictionary
- `tests/`: unit tests

## Run tests
```bat
pytest -q
```
