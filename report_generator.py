from datetime import datetime

def make_report(filename, target_role, selected, found, found_required, missing, results, roadmap):
    lines = [
        "AI RESUME ANALYZER & JOB RECOMMENDATION SYSTEM",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Resume file: {filename}",
        f"Selected target role: {target_role}",
        f"Estimated match score: {selected['match_score']:.1f}%",
        f"Skill coverage: {selected['skill_coverage']:.1f}%",
        f"TF-IDF text similarity: {selected['text_similarity']:.1f}%",
        "",
        "DETECTED SKILLS",
        ", ".join(found) if found else "None detected from the current dictionary.",
        "",
        "REQUIRED SKILLS DETECTED FOR TARGET ROLE",
        ", ".join(found_required) if found_required else "None detected.",
        "",
        "REQUIRED SKILLS NOT DETECTED",
        ", ".join(missing) if missing else "None.",
        "",
        "TOP THREE ROLE RECOMMENDATIONS",
    ]
    for i, (_, row) in enumerate(results.head(3).iterrows(), start=1):
        lines.append(f"{i}. {row['role']} — {row['match_score']:.1f}% estimate")
    lines += ["", "SUGGESTED LEARNING ROADMAP"]
    if roadmap:
        for item in roadmap:
            lines.append(f"{item['Priority']}. {item['Skill to learn']}: {item['Topic']} — {item['Suggested activity']}")
    else:
        lines.append("No undetected required skills for this target role based on the current dictionary.")
    lines += [
        "",
        "IMPORTANT LIMITATION",
        "Scores are project-defined estimates for educational guidance, not hiring probabilities or recruiter decisions.",
        "A skill not detected in a resume is not proof that the candidate lacks that ability.",
        "Results depend on extracted text, the controlled skill dictionary, and the role dataset."
    ]
    return "\n".join(lines)
