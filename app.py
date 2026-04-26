import streamlit as st
import json
import re
from groq import Groq

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI-Powered Skill Assessment & Personalised Learning Plan Agent")

# --------------------------------------------------
# CLIENT
# --------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------
def init_state():
    defaults = {
        "skills": [],
        "index": 0,
        "results": [],
        "questions": {},
        "learning_plan": None,
        "chat": [],
        "answers": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
jd_text = st.text_area("📄 Job Description", height=250)
resume_text = st.text_area("📄 Resume", height=250)

# --------------------------------------------------
# JSON PARSER
# --------------------------------------------------
def get_json(text):
    if not text:
        return None

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None

    return None

# ==================================================
# 1. JD RESUME MATCH
# ==================================================
def match_engine(jd, resume):
    prompt = f"""
Compare the Job Description and Resume.

Return STRICT JSON ONLY:
{{
  "skill_match_percent": 0,
  "experience_match_percent": 0,
  "overall_fit_percent": 0,
  "matches": ["..."],
  "gaps": ["..."],
  "summary": "short explanation"
}}

JD:
{jd}

Resume:
{resume}
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return get_json(res.choices[0].message.content)

# ==================================================
# 2. SKILL EXTRACTION
# ==================================================
def extract_skills(jd):
    prompt = f"""
Extract the top important technical skills from this JD.

Return STRICT JSON ONLY:
{{
  "skills": ["skill1", "skill2", "skill3"]
}}

JD:
{jd}
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return get_json(res.choices[0].message.content)

# ==================================================
# 3. QUESTION GENERATION
# ==================================================
def generate_question(skill, jd):
    prompt = f"""
You are a technical interviewer.

Ask ONE realistic interview question for this skill:
{skill}

Context:
{jd}

Return only the question. No explanation.
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content.strip()

# ==================================================
# 4. EVALUATION
# ==================================================
def evaluate(skill, question, answer):
    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate answer.

Skill: {skill}
Question: {question}
Answer: {answer}

Return STRICT JSON ONLY:
{{
  "score": 0,
  "level": "Beginner|Intermediate|Strong|Expert",
  "reason": "short explanation"
}}

Rules:
- No HTML
- No markdown
- Keep reason short
- Do not repeat the answer
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return get_json(res.choices[0].message.content)

# ==================================================
# 5. LEARNING PLAN
# ==================================================
def learning_plan(results, skills):
    prompt = f"""
Create a learning plan based on weak skills.

Return STRICT JSON ONLY:
{{
  "weak_skills": ["..."],
  "30_day_plan": ["..."],
  "60_day_plan": ["..."],
  "90_day_plan": ["..."],
  "resources": {{"skill": ["..."]}},
  "adjacent_skills": {{"skill": ["..."]}}
}}

Results:
{results}

Skills:
{skills}
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return get_json(res.choices[0].message.content)

# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3 = st.tabs([
    "📊 JD–Resume Match",
    "🎤 Interview",
    "📚 Learning Plan"
])

# ==================================================
# TAB 1
# ==================================================
with tab1:
    if st.button("Run Match Analysis"):
        if not jd_text or not resume_text:
            st.error("Please enter both JD and Resume")
        else:
            result = match_engine(jd_text, resume_text)

            if not isinstance(result, dict):
                st.error("Match analysis failed")
            else:
                st.metric("Skill Match %", result.get("skill_match_percent", 0))
                st.metric("Experience Match %", result.get("experience_match_percent", 0))
                st.metric("Overall Fit %", result.get("overall_fit_percent", 0))

                st.write("### Matches")
                st.write(result.get("matches", []))

                st.write("### Gaps")
                st.write(result.get("gaps", []))

                st.write("### Summary")
                st.write(result.get("summary", ""))

# ==================================================
# TAB 2
# ==================================================
with tab2:
    if st.button("Start Interview"):
        if not jd_text:
            st.error("Please enter Job Description first")
        else:
            data = extract_skills(jd_text)

            if not data or "skills" not in data:
                st.error("Skill extraction failed")
            else:
                st.session_state.skills = data["skills"][:5]
                st.session_state.index = 0
                st.session_state.chat = []
                st.session_state.results = []
                st.session_state.answers = []
                st.session_state.questions = {}
                st.rerun()

    if st.session_state.skills:
        i = st.session_state.index
        skills = st.session_state.skills

        if i >= len(skills):
            st.success("🎉 Interview Completed")
            st.markdown("## Final Evaluation Report")

            total_score = 0

            for idx, r in enumerate(st.session_state.results):
                score = r.get("score", 0)
                level = r.get("level", "N/A")
                reason = r.get("reason", "")
                total_score += score

                st.subheader(f"Skill {idx + 1}")
                st.write(f"**Score:** {score}/10")
                st.write(f"**Level:** {level}")
                st.write(f"**Reason:** {reason}")
                st.write(f"**Answer:** {st.session_state.answers[idx]}")
                st.divider()

            avg = total_score / len(st.session_state.results) if st.session_state.results else 0
            st.metric("Final Score", f"{avg:.1f} / 10")

        else:
            skill = skills[i]

            if skill not in st.session_state.questions:
                st.session_state.questions[skill] = generate_question(skill, jd_text)

            question = st.session_state.questions[skill]

            st.markdown("## Interview")
            st.write(f"### Skill: {skill}")
            st.info(question)

            answer = st.text_area("Your Answer", key=f"answer_{i}")

            if st.button("Next Question"):
                if not answer.strip():
                    st.warning("Please enter your answer")
                else:
                    result = evaluate(skill, question, answer)

                    if not isinstance(result, dict):
                        st.error("Evaluation failed")
                    else:
                        st.session_state.results.append(result)
                        st.session_state.answers.append(answer)
                        st.session_state.index += 1
                        st.rerun()

# ==================================================
# TAB 3
# ==================================================
with tab3:
    if st.button("Generate Learning Plan"):
        if not st.session_state.results:
            st.error("Complete the interview first")
        else:
            plan = learning_plan(
                st.session_state.results,
                st.session_state.skills
            )

            if not isinstance(plan, dict):
                st.error("Learning plan generation failed")
            else:
                st.session_state.learning_plan = plan

    if st.session_state.learning_plan:
        p = st.session_state.learning_plan

        st.write("### Weak Skills")
        st.write(p.get("weak_skills", []))

        st.write("### 30 Day Plan")
        st.write(p.get("30_day_plan", []))

        st.write("### 60 Day Plan")
        st.write(p.get("60_day_plan", []))

        st.write("### 90 Day Plan")
        st.write(p.get("90_day_plan", []))

        st.write("### Resources")
        st.write(p.get("resources", {}))

        st.write("### Adjacent Skills")
        st.write(p.get("adjacent_skills", {}))
