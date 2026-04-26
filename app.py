import streamlit as st
import json
import re
from groq import Groq

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SkillBridge",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI-Powered Skill Assessment & Personalised Learning Plan Agent")

# --------------------------------------------------
# CLIENT
# --------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "skills" not in st.session_state:
    st.session_state.skills = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "chat" not in st.session_state:
    st.session_state.chat = []

if "results" not in st.session_state:
    st.session_state.results = []

if "questions" not in st.session_state:
    st.session_state.questions = {}

if "learning_plan" not in st.session_state:
    st.session_state.learning_plan = None

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
jd_text = st.text_area("📄 Job Description")
resume_text = st.text_area("📄 Resume")

# --------------------------------------------------
#  JSON
# --------------------------------------------------
def get_json(text):
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
# 1️⃣ MATCH ENGINE
# ==================================================
def match_engine(jd, resume):

    prompt = f"""
Compare JD and Resume semantically.

Return JSON:
{{
  "skill_match_percent": 0-100,
  "experience_match_percent": 0-100,
  "overall_fit_percent": 0-100,
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
# 2️⃣ SKILL EXTRACTION
# ==================================================
def extract_skills(jd):

    prompt = f"""
Extract ALL skills (technical + soft + domain).

Return JSON:
{{ "skills": ["skill1", "skill2"] }}

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
# 3️⃣ QUESTION
# ==================================================
def generate_question(skill, jd):

    prompt = f"""
You are an interviewer.

Ask ONE real interview question for:
Skill: {skill}

Context: {jd}

Return only question.
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return res.choices[0].message.content

# ==================================================
# 4️⃣ EVALUATION
# ==================================================
def evaluate(skill, question, answer):

    prompt = f"""
Evaluate response.

Skill: {skill}
Q: {question}
A: {answer}

Return JSON:
{{
  "score": 0-10,
  "level": "Beginner|Intermediate|Strong|Expert",
  "reason": "short explanation"
}}
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return get_json(res.choices[0].message.content)

# ==================================================
# 5️⃣ LEARNING PLAN
# ==================================================
def learning_plan(results, skills):

    prompt = f"""
You are a career coach.

Create learning plan based on weak skills (<6 score).

Return JSON:

{{
  "weak_skills": ["..."],
  "30_day_plan": ["..."],
  "60_day_plan": ["..."],
  "90_day_plan": ["..."],
  "resources": {{
    "skill": ["links or topics"]
  }},
  "adjacent_skills": {{
    "skill": ["adj1", "adj2"]
  }},
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
# TABS UI
# ==================================================
tab1, tab2, tab3 = st.tabs([
    "📊 JD-Resume Match",
    "🎤 Interview",
    "📚 Learning Plan"
])

# --------------------------------------------------
# TAB 1 - MATCH
# --------------------------------------------------
with tab1:

    if st.button("Run Match Analysis"):

        if jd_text and resume_text:

            result = match_engine(jd_text, resume_text)

            if result:

                st.metric("Skill Match %", result["skill_match_percent"])
                st.metric("Experience Match %", result["experience_match_percent"])
                st.metric("Overall Fit %", result["overall_fit_percent"])

                st.write("### Matches")
                st.write(result["matches"])

                st.write("### Gaps")
                st.write(result["gaps"])

                st.write("### Summary")
                st.write(result["summary"])

# --------------------------------------------------
# TAB 2 - INTERVIEW 
# --------------------------------------------------

with tab2:

    if st.button("Start Interview"):

        data = extract_skills(jd_text)
        st.session_state.skills = (data.get("skills") or [])[:5]
        st.session_state.index = 0
        st.session_state.chat = []
        st.session_state.results = []
        st.rerun()

    if st.session_state.skills:

        i = st.session_state.index
        skills = st.session_state.skills

        if i < len(skills):

            skill = skills[i]

            if skill not in st.session_state.questions:
                st.session_state.questions[skill] = generate_question(skill, jd_text)

            question = st.session_state.questions[skill]

            st.markdown(
                f"## 🎯 Skill : {skill}"
            )

            st.info(question)

            answer = st.text_area("Your Answer", key=f"ans_{skill}")

            if st.button("Evaluate & Next"):

                result = evaluate(skill, question, answer)

                if result:
                    st.session_state.results.append(result)

                st.session_state.index += 1
                st.rerun()

        else:

            st.success("Interview Completed 🎉")

            scores = [r["score"] for r in st.session_state.results]
            avg = sum(scores) / len(scores)

            st.metric("Final Score", f"{avg:.1f} / 10")


# --------------------------------------------------
# TAB 3 - LEARNING PLAN
# --------------------------------------------------
with tab3:

    if st.button("Generate Learning Plan"):

        if st.session_state.results and st.session_state.skills:

            plan = learning_plan(
                st.session_state.results,
                st.session_state.skills
            )

            st.session_state.learning_plan = plan

    if st.session_state.learning_plan:

        p = st.session_state.learning_plan

        st.write("### Weak Skills")
        st.write(p.get("weak_skills"))

        st.write("### 30 Day Plan")
        st.write(p.get("30_day_plan"))

        st.write("### 60 Day Plan")
        st.write(p.get("60_day_plan"))

        st.write("### 90 Day Plan")
        st.write(p.get("90_day_plan"))

        st.write("### Resources")
        st.write(p.get("resources"))

        st.write("### Adjacent Skills")
        st.write(p.get("adjacent_skills"))

      
