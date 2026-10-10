import pandas as pd
import re

def load_skill_dictionary(path: str) -> pd.DataFrame:
    df = pd.read_csv(path).fillna("")
    required = {"canonical_skill", "category", "aliases"}
    if not required.issubset(df.columns):
        raise ValueError(f"Skill dictionary must contain columns: {sorted(required)}")
    return df

def _contains_phrase(text: str, phrase: str) -> bool:
    phrase = phrase.strip().lower()
    if not phrase:
        return False
    # Normalize flexible whitespace; use boundaries to reduce accidental substring hits.
    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    return re.search(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", text.lower()) is not None

def extract_skills(cleaned_text: str, skills_df: pd.DataFrame) -> list[str]:
    found = []
    for _, row in skills_df.iterrows():
        canonical = str(row["canonical_skill"]).strip()
        aliases = [canonical] + [a.strip() for a in str(row["aliases"]).split("|") if a.strip()]
        if any(_contains_phrase(cleaned_text, alias) for alias in aliases):
            found.append(canonical)
    return sorted(set(found), key=str.lower)
