# System Workflow

## AI Resume Analyzer and Job Recommendation System

### Workflow Steps

1. **Resume Upload:** The user uploads a resume in PDF or DOCX format.
2. **File Validation:** The application checks the supported file type and enforces a 5 MB file-size limit.
3. **Text Extraction:** The application extracts text from the uploaded resume.
4. **Text Cleaning:** Extracted text is normalized for skill detection and job matching.
5. **Skill Detection:** The system identifies skills using a predefined skill dictionary and its aliases.
6. **Job-Role Matching:** The resume is compared against available job roles using required-skill coverage and TF-IDF cosine similarity.
7. **Role Ranking:** Job roles are sorted by their estimated match scores, and the top three recommendations are displayed.
8. **Skill-Gap Analysis:** The system compares detected skills against the selected role's required skills.
9. **Learning Roadmap:** A rule-based roadmap is generated for required skills that were not detected.
10. **Report Generation:** The application generates a downloadable text report containing the analysis results.

### Scoring Formula

Match Estimate = (0.70 × Required-Skill Coverage + 0.30 × TF-IDF Similarity) × 100

Both coverage and similarity are represented as values between 0 and 1 before calculating the final score.

### Technology Stack

- Python
- Streamlit
- Pandas
- scikit-learn
- Plotly
- PDF and DOCX parsing libraries

### Important Limitation

The match score is an educational estimate, not a hiring probability. A skill that is not detected in a resume is not proof that the candidate lacks that skill.
