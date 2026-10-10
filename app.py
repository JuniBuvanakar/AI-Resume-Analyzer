import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_roles, analyze_roles
from roadmap_generator import generate_roadmap
from report_generator import make_report

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("AI Resume Analyzer & Job Recommendation System")
st.caption("Educational career guidance based on resume evidence. Scores are estimates, not hiring decisions.")

with st.sidebar:
    st.header("About this tool")
    st.write("Upload a PDF or DOCX resume to inspect detected skills, compare job roles, and identify learning priorities.")
    st.info("Resume text is processed in this app session. Do not upload documents you are not authorized to use.")

uploaded = st.file_uploader(
    "Upload your resume (PDF or DOCX, maximum 5 MB)",
    type=["pdf", "docx"],
    help="Upload a text-based PDF or a DOCX file. Maximum file size: 5 MB."
)
roles_path = "data/job_roles.csv"
skills_path = "data/skill_dictionary.csv"

try:
    roles_df = load_roles(roles_path)
    skills_df = load_skill_dictionary(skills_path)
except Exception as exc:
    st.error(f"Could not load project datasets: {exc}")
    st.stop()

if uploaded:
    max_bytes = 5 * 1024 * 1024
    if uploaded.size > max_bytes:
        st.error("The file is larger than the 5 MB limit. Please upload a smaller resume.")
        st.stop()

    try:
        raw_text = extract_resume_text(uploaded, uploaded.name)
        cleaned = clean_text(raw_text)
    except Exception as exc:
        st.error(f"Could not read this file. Please check that it is a valid, text-based PDF or DOCX. Details: {exc}")
        st.stop()

    if len(cleaned.strip()) < 40:
        st.warning("Very little text was extracted. If this is a scanned PDF, this version may not be able to read its embedded images. Try a text-based PDF or DOCX.")
        st.stop()

    st.success(f"Processed: {uploaded.name}")
    with st.expander("Review extracted text"):
        st.text_area("Extracted resume text", raw_text, height=220)

    found = extract_skills(cleaned, skills_df)
    st.subheader("Detected skills")
    if found:
        found_df = skills_df[skills_df["canonical_skill"].isin(found)][["category", "canonical_skill"]].drop_duplicates()
        st.dataframe(found_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No dictionary skills were detected. Review the extracted text and remember that only skills in the current dictionary are recognized.")

    results = analyze_roles(cleaned, found, roles_df)
    st.subheader("Job-role match analysis")
    selected_role = st.selectbox("Choose a target role for skill-gap analysis", results["role"].tolist())
    selected = results[results["role"] == selected_role].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Selected-role match estimate", f'{selected["match_score"]:.1f}%')
    c2.metric("Required skills detected", f'{int(selected["found_required_count"])} / {int(selected["required_count"])}')
    c3.metric("Detected skills", str(len(found)))

    st.caption("Score method: 70% required-skill coverage + 30% TF-IDF cosine similarity. This is a transparent project-defined estimate, not a hiring probability.")
    chart = px.bar(results.head(3), x="role", y="match_score", title="Top 3 recommended roles", range_y=[0, 100], labels={"role":"Job role", "match_score":"Match estimate (%)"})
    st.plotly_chart(chart, use_container_width=True)
    st.dataframe(results[["role", "match_score", "skill_coverage", "text_similarity"]].round(1), use_container_width=True, hide_index=True)

    role_row = roles_df[roles_df["role"] == selected_role].iloc[0]
    required = [x.strip() for x in role_row["required_skills"].split("|") if x.strip()]
    found_required = [s for s in required if s in found]
    missing = [s for s in required if s not in found]

    left, right = st.columns(2)
    with left:
        st.subheader("Required skills detected")
        st.write(", ".join(found_required) if found_required else "No required skills detected from the dictionary.")
    with right:
        st.subheader("Skills not detected")
        st.write(", ".join(missing) if missing else "All listed required skills were detected.")
        st.caption("A skill not detected in the resume is not proof that you lack that ability.")

    st.subheader("Suggested learning roadmap")
    roadmap = generate_roadmap(missing)
    if roadmap:
        st.dataframe(pd.DataFrame(roadmap), use_container_width=True, hide_index=True)
    else:
        st.success("No undetected required skills for this role based on the current dictionary.")

    report = make_report(uploaded.name, selected_role, selected, found, found_required, missing, results, roadmap)
    st.download_button("Download analysis report (.txt)", report, file_name="resume_analysis_report.txt", mime="text/plain")
else:
    st.markdown("### What you will get")
    st.markdown("- Extracted resume text\n- Categorized skills detected from the resume\n- Match estimates for at least five job roles\n- Top-three role recommendations\n- Target-role skill gaps\n- A rule-based learning roadmap\n- A downloadable text report")
