"""Generate shared Quarto includes from the reviewed professional profile."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
profile = json.loads((root / "data/profile.json").read_text(encoding="utf-8"))
output = root / "_generated"
output.mkdir(exist_ok=True)
summary = f'**{profile["headline"]}**\n\n{profile["summary"]}\n'
education = "## Education\n\n" + "\n\n".join(
    f'**{item["school"]}**  \n{item["degree"]} | {item["date"]}'
    for item in profile["education"]
) + "\n"
experience = "## Professional Experience\n\n" + "\n\n".join(
    f'### {item["title"]}\n\n**{item["company"]}** | {item["location"]}  \n'
    f'{item["dates"]}\n\n' + "\n".join(f'- {point}' for point in item["highlights"])
    for item in profile["experience"]
) + "\n"
current = profile["experience"][0]
current_role = (
    f'My current role is **{current["title"]} at {current["company"]}**. '
    'I work across system architecture, digital-thread practices, and AI-enabled '
    'engineering to help teams turn complex requirements into models they can use.\n'
)
for name, content in {"summary.md": summary, "education.md": education, "experience.md": experience, "current-role.md": current_role}.items():
    (output / name).write_text(content, encoding="utf-8")
resume = (
    f'# {profile["name"]}\n\n{summary}\n'
    f'[Email](mailto:{profile["email"]}) | [LinkedIn]({profile["linkedin"]})\n\n'
    f'{experience}\n{education}\n## Areas of Focus\n\n'
    + "\n".join(f'- {skill}' for skill in profile["skills"])
    + f'\n\n_Profile data reviewed: {profile["reviewed_on"]}_\n'
)
(output / "resume.md").write_text(resume, encoding="utf-8")
print("Generated homepage and resume content from data/profile.json")
