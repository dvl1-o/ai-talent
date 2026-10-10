# AI Talent

AI-powered B2B SaaS recruitment platform — a portfolio project demonstrating full-stack engineering, multi-tenant SaaS architecture, and practical LLM integration.

## Overview

AI Talent lets companies manage their recruitment pipeline end-to-end: post jobs, receive applications, and get AI-assisted candidate evaluation — from raw CV to a structured, explainable match score.

**Core workflow:** Organization → Job → Candidate applies → CV uploaded → AI parses CV → AI scores candidate against job → Recruiter reviews.

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Auth:** JWT (djangorestframework-simplejwt), custom User model (email-based)
- **AI:** Google Gemini via LangChain — structured CV parsing and candidate/job matching
- **Frontend (in progress):** Next.js, TypeScript, Tailwind CSS

## Key Architecture Decisions

- **Multi-tenant RBAC**: organization role lives on a `Membership` model (`User → Membership → Organization`), never directly on `User` — allows one user to belong to multiple organizations with different roles.
- **Tenant isolation enforced server-side**: every organization-scoped queryset filters by the requesting user's memberships — never relies on frontend filtering.
- **AI output is always validated**: LLM responses are constrained to a strict Pydantic schema before being saved — never trusted blindly.
- **Incremental development**: each layer (models → API → AI → frontend) was built, tested via Postman, and committed before moving to the next.

## Features implemented so far

- JWT authentication (register / login / refresh / me)
- Multi-tenant organizations with role-based membership (Admin, Recruiter, Hiring Manager)
- Jobs CRUD, scoped to organization membership
- Candidate profiles, resume upload (validated: type + size), skills
- Applications workflow with dual access control (candidate vs. recruiter)
- **AI CV parsing**: extracts structured data (skills, experience, education, languages) from an uploaded PDF via an LLM, with strict schema validation
- **AI matching engine**: weighted score (skills / experience / education / semantic) with a recruiter-readable explanation, strengths, weaknesses, and missing skills

## Running locally

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env   # then fill in your own values
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Roadmap

- [x] Custom auth, multi-tenant RBAC
- [x] Jobs, Candidates, Applications CRUD API
- [x] CV upload with validation
- [x] AI CV parsing (LLM + structured output)
- [x] AI matching engine
- [ ] Frontend dashboard (Next.js) — in progress
- [ ] RAG chatbot for recruiter Q&A on candidates
- [ ] Async CV processing (Celery + Redis)
- [ ] Automated tests, Docker, CI/CD, deployment

## Author

Built by Mohamed Ali GATRI as a portfolio project.
