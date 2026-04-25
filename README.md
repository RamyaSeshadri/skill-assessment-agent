# AI-Powered Skill Assessment & Personalized Learning Plan Agent

AI-powered agent that analyzes a Job Description and candidate resume, assesses real skill proficiency through dynamic questions, identifies skill gaps, and generates a personalized learning plan with recommended resources, time estimates, and a 30/60/90-day upskilling roadmap.

## Problem Statement

A resume shows what a candidate claims to know — but not how well they actually know it.

This project solves that problem by building an AI-powered agent that takes a Job Description and a candidate’s resume, conversationally assesses real skill proficiency, identifies gaps, and generates a personalized learning plan focused on adjacent, realistically achievable skills.

The goal is to move beyond resume screening and enable smarter hiring decisions with explainable AI-driven evaluation.

---

## Solution Overview

The agent analyzes:

* Job Description (JD)
* Candidate Resume

It then:

* extracts required skills
* compares JD skills vs resume skills
* identifies matching and missing skills
* generates dynamic interview questions based on weak areas
* scores skill proficiency using explainable levels
* creates a personalized 30/60/90-day learning roadmap
* recommends free learning resources
* suggests portfolio-building project ideas

This helps recruiters assess actual capability and helps candidates improve strategically.

---

## Key Features

### Skill Extraction

Automatically identifies required skills from the Job Description.

### Resume vs JD Gap Analysis

Compares candidate profile against role expectations.

### Conversational Skill Assessment

Generates dynamic interview questions based on actual missing skills.

### Explainable Skill Scoring

Uses proficiency levels:

* Beginner
* Intermediate
* Strong
* Expert

### Personalized Learning Plan

Creates realistic upskilling recommendations including:

* adjacent skills
* learning priorities
* time estimates
* curated resources
* project suggestions

### 30/60/90-Day Roadmap

Provides structured learning progression for practical growth.

---

## Technology Stack

### Frontend

* Streamlit

### LLM

* Groq API
* Llama 3.3 70B Versatile

### Core Logic

* Prompt-driven evaluation
* Dynamic question generation
* Explainable scoring engine
* Personalized learning roadmap generation

---

## Architecture Flow

Architecture Diagram is available in:
architecture-diagram.png

---

## Local Setup Instructions

### Clone Repository

```bash
git clone https://github.com/RamyaSeshadri/skill-assessment-agent.git
cd skill-assessment-agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add API Key

Update your `app.py` file with your Groq API Key:

```python
client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)
```

### Run the Application

```bash
python -m streamlit run app.py
```

---

## Sample Input

### Job Description

Data Governance Analyst with SQL, metadata management, Collibra, stakeholder communication, policy documentation, and data quality experience.

### Candidate Resume

Candidate with experience in SQL, reporting, stakeholder collaboration, and data quality, but limited exposure to metadata management and governance tools.

---

## Sample Output

### Matching Skills

* SQL
* Data Quality
* Stakeholder Communication

### Missing Skills

* Metadata Management
* Collibra
* Data Lineage
* Governance Framework Design

### Dynamic Interview Questions

* Explain how you handled data quality issues in your previous role.
* Describe your experience with metadata management tools.
* How have you used SQL to improve reporting decisions?

### Learning Plan

* Learn metadata fundamentals
* Study Collibra basics
* Practice governance documentation
* Build a mini governance portfolio project

Estimated Time:

30–45 hours

Roadmap:

30 / 60 / 90 Days

---

## Demo Video

Demo video link.

---

## Live Project URL

Deployment link.

---

## GitHub Repository

https://github.com/RamyaSeshadri/skill-assessment-agent

---

## Future Improvements

* add scoring dashboard
* support multiple candidate comparisons

---

