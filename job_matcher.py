import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_roles(path: str) -> pd.DataFrame:
    df = pd.read_csv(path).fillna("")
    required = {"role", "description", "required_skills", "preferred_skills"}
    if not required.issubset(df.columns):
        raise ValueError(f"Job roles file must contain columns: {sorted(required)}")
    if len(df) < 5:
        raise ValueError("At least five job roles are required.")
    return df

def analyze_roles(resume_text: str, found_skills: list[str], roles_df: pd.DataFrame) -> pd.DataFrame:
    role_texts = (roles_df["description"].astype(str) + " " +
                  roles_df["required_skills"].astype(str).str.replace("|", " ", regex=False) + " " +
                  roles_df["preferred_skills"].astype(str).str.replace("|", " ", regex=False)).tolist()
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = vectorizer.fit_transform([resume_text] + role_texts)
        similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    except ValueError:
        similarities = [0.0] * len(roles_df)

    rows = []
    found_set = set(found_skills)
    for idx, (_, role_row) in enumerate(roles_df.iterrows()):
        required = [x.strip() for x in str(role_row["required_skills"]).split("|") if x.strip()]
        found_required = [s for s in required if s in found_set]
        coverage = len(found_required) / len(required) if required else 0.0
        similarity = float(similarities[idx]) if idx < len(similarities) else 0.0
        score = (0.70 * coverage + 0.30 * similarity) * 100
        rows.append({
            "role": role_row["role"],
            "match_score": round(score, 1),
            "skill_coverage": coverage * 100,
            "text_similarity": similarity * 100,
            "found_required_count": len(found_required),
            "required_count": len(required)
        })
    return pd.DataFrame(rows).sort_values(["match_score", "role"], ascending=[False, True]).reset_index(drop=True)
