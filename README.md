# AI-Powered Skill Assessment & Personalized Learning Plan Agent

AI-powered agent that analyzes a Job Description and candidate resume, assesses real skill proficiency through dynamic questions, identifies skill gaps, and generates a personalized learning plan with recommended resources and a 30/60/90-day upskilling roadmap.

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

💻 1. Software Development (Backend Developer)
📄 Job Description

We are looking for a Backend Developer with strong experience in Python-based web development.

The candidate should have hands-on experience in building REST APIs using Flask or Django and working with relational databases such as SQL or MySQL. Knowledge of Docker, microservices architecture, and cloud platforms like AWS is required.

Familiarity with Git, CI/CD pipelines, and system design is a plus.

Responsibilities:

Design and build scalable backend systems
Develop RESTful APIs
Work with cloud infrastructure (AWS)
Collaborate with frontend and DevOps teams
Optimize database performance

### Candidate Resume

Name: Arjun Kumar
Role: Backend Developer
Experience: 4.5 years

Summary

Backend developer with experience in Python, API development, and database systems. Worked in Agile teams building scalable web applications and integrating third-party services.

Skills
Python (Flask)
REST API development
SQL (MySQL)
Git & GitHub
Basic AWS (EC2, S3)
Docker (basic usage)
Agile / Scrum
Experience

Software Engineer – TechNova Solutions (2020–Present)

Built REST APIs using Flask for internal enterprise systems
Designed MySQL schemas and optimized queries
Worked with AWS EC2 for deployment
Participated in CI/CD pipeline setup using Jenkins (basic level)

Junior Developer – CodeWave (2018–2020)

Developed backend services in Python
Maintained database operations and API integration
Worked in Agile sprint teams
Education

B.Tech Computer Science

---

## Sample Output

Skill Match %

80

Experience Match %

70

Overall Fit %

75

Matches
[
0:"Backend Developer"
1:"Python"
2:"Flask"
3:"REST API development"
4:"SQL (MySQL)"
5:"Git & GitHub"
6:"AWS (EC2, S3)"
7:"Docker (basic usage)"
8:"Agile / Scrum"
]
Gaps
[
0:"Django"
1:"Microservices architecture"
2:"Cloud platforms (beyond AWS)"
3:"CI/CD pipeline setup (beyond Jenkins)"
4:"System design"
]

Summary
Arjun Kumar is a Backend Developer with 4.5 years of experience in Python, API development, and database systems. He has hands-on experience in building scalable web applications and integrating third-party services. However, he lacks experience in Django, microservices architecture, and cloud platforms beyond AWS.

### Dynamic Interview Questions

### Learning Plan

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

