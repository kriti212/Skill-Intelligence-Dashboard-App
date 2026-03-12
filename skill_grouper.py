from data_processor import SKILL_HIERARCHY

def group_skills(skill_counts, threshold):
    """
    Groups extraction counts according to SKILL_HIERARCHY and a frequency threshold.
    Skills with count < threshold are merged into their parent category.
    Skills with count >= threshold remain specific, but their points still contribute to the parent.
    """
    general_skills = []
    merged_skills = {}

    for category, specifics in SKILL_HIERARCHY.items():
        total_xp = skill_counts.get(category.lower(), 0)
        retained_specifics = []

        for skill in specifics:
            count = skill_counts.get(skill, 0)
            if count > 0:
                if count >= threshold:
                    retained_specifics.append(skill)
                    total_xp += count
                else:
                    merged_skills[skill] = category
                    total_xp += count

        if total_xp > 0:
            general_skills.append({
                "skill": category,
                "experience_points": total_xp,
                "specific_skills": retained_specifics
            })

    return {
        "general_skills": general_skills,
        "merged_skills": merged_skills
    }

if __name__ == "__main__":
    sample_counts = {
        "qwen": 5,
        "gemma": 1,
        "chatgpt": 4,
        "int8": 2,
        "fp16": 3,
        "calculus": 10,
        "arithmetic": 1
    }
    
    print("Threshold 3:", group_skills(sample_counts, 3))
