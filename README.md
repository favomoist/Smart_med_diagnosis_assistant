# Smart Medical Diagnosis Assistant

## 1. Vision Document

### Project Name & Overview
**Smart Medical Diagnosis Assistant (SMDA)** is a cross-platform application that helps users understand possible causes of their symptoms, get triage guidance (e.g., self-care vs. see a doctor vs. emergency), and share a structured summary with a clinician. It is **not** a diagnostic replacement for a licensed physician — it is a decision-support and information tool.

- **Frontend:** React 19 (TypeScript, Vite, Tailwind CSS)
- **Backend:** Python (FastAPI)
- **Diagnosis Logic:** Starts as a rule-based/symptom-checker engine, with an extensible interface to plug in an ML model or an external LLM API later
- **Data Store:** PostgreSQL (structured data) + Redis (caching/session)
- **Infra:** Docker & Docker Compose locally; containerized deployment to a cloud host

### Problem It Solves
People often experience symptoms and don't know:
1. How urgent the situation is (self-care vs. urgent care vs. emergency).
2. What conditions might explain their symptoms, in plain language.
3. What information to bring to a doctor to make the consultation more efficient.

Search engines give overwhelming, unstructured, and sometimes alarmist results. SMDA gives a structured, guided, and calibrated experience instead.

### Target Users (Personas)

| Persona | Description | Needs |
|---|---|---|
| **Priya, the Concerned Patient** (28) | Has mild-to-moderate symptoms, wants quick clarity | Fast symptom input, clear triage advice, simple language |
| **Dr. Arjun, the Clinician** (40) | Reviews patient-submitted symptom summaries before an appointment | Structured, exportable patient history; confidence levels; red-flag alerts |
| **Meena, the Caregiver** (55) | Manages health of an elderly parent | Ability to log symptoms on behalf of another person, track history over time |
| **Admin/Ops** | Maintains the platform | Manage content (symptom/condition database), monitor system health, view usage analytics |

### Vision Statement
> To give anyone, anywhere, an accessible first step in understanding their health symptoms — through a fast, trustworthy, and clinically-informed digital assistant that empowers better decisions about when and how to seek care.

### Key Features / Goals
- Guided symptom intake (chat-like or form-based questionnaire)
- Triage engine that classifies urgency (Emergency / Urgent Care / Self-Care)
- Explainable "possible conditions" list with confidence indicators (not a definitive diagnosis)
- Patient history / symptom log over time
- Exportable summary (PDF/shareable link) for clinicians
- Admin panel to manage the symptom-condition knowledge base
- Authentication & role-based access (Patient, Clinician, Admin)
- Notifications/reminders (e.g., follow-up check-ins)

### Success Metrics
- **Adoption:** # of active users completing a symptom check per week
- **Engagement:** Average completion rate of symptom questionnaires (target > 80%)
- **Trust/Safety:** % of emergency-flagged cases correctly identified in test scenarios (target 100% recall on red-flag symptom sets)
- **Performance:** API p95 response time < 500ms for triage requests
- **Clinician value:** % of clinicians rating the shared summary as "useful" (target > 75%)

### Assumptions & Constraints
**Assumptions**
- Users have basic smartphone/web literacy.
- Initial symptom-condition mapping is built from publicly available, licensed medical datasets/guidelines, not proprietary clinical data.
- The system will clearly disclaim it is not a substitute for professional medical advice.

**Constraints**
- No real patient identifiable health data (PHI) will be stored during the academic project phase — only synthetic/test data.
- Limited to a rule-based or lightweight ML engine within the project timeline (full clinical-grade ML validation is out of scope).
- Single-team, time-boxed academic delivery — cloud deployment will use free/low-cost tiers.

---

## 2. Branching Strategy — GitHub Flow

This project follows **GitHub Flow**:

1. `main` is always deployable.
2. For any new work, create a feature branch off `main`:
   ```bash
   git checkout -b feature/<short-description>
   # e.g. git checkout -b feature/symptom-intake-form
   ```
3. Commit changes with clear messages, push the branch, and open a Pull Request into `main`.
4. Request review, address comments, then merge (squash or merge commit) once approved and checks pass.
5. Delete the feature branch after merging.

Example branches used in this project:
- `feature/backend-api-skeleton`
- `feature/docker-setup`
- `feature/vision-doc`

---

## 3. Quick Start – Local Development

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Node.js](https://nodejs.org/) (v20+ recommended) and [pnpm](https://pnpm.io/) or [npm](https://www.npmjs.com/)
- Git

### Run the backend + database with Docker

```bash
# From the repo root
docker compose build
docker compose up
```

This starts:
- `backend` — FastAPI app on http://localhost:8000 (docs at http://localhost:8000/docs)
- `db` — PostgreSQL on port 5432
- `cache` — Redis on port 6379

To stop:
```bash
docker compose down
```

### Run the frontend (React + Vite)

```bash
cd frontend
pnpm install    # or npm install
pnpm dev        # or npm run dev
```

The web application will be available at `http://localhost:5173`. Point API requests to the backend at `http://localhost:8000`.

---

## 4. Local Development Tools

| Tool | Purpose |
|---|---|
| **Docker Desktop** | Runs backend, database, and cache in containers |
| **VS Code** (or Android Studio) | Primary IDE, with Python and Flutter extensions |
| **Node.js + pnpm / npm** | Frontend runtime & package management |
| **Vite & React DevTools** | Frontend dev server, fast HMR, component inspection |
| **Postman / FastAPI Swagger UI** (`/docs`) | API testing |
| **pgAdmin / DBeaver** (optional) | Inspecting the PostgreSQL database |
| **Git + GitHub** | Version control, following GitHub Flow |
| **GitHub Projects** | Backlog and sprint tracking (user stories as Issues) |
| **Figma (free tier)** | Wireframes and UI mockups |
| **draw.io (diagrams.net)** | Architecture diagram |

---

## 5. Repository Structure

```
smart-med-diagnosis-assistant/
├── README.md
├── .gitignore
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
├── frontend/               # React + Vite web app (SmartyMed)
│   └── README.md
└── docs/
    ├── user-stories.md     # 25 user stories + MoSCoW
    └── architecture.drawio # Architecture diagram (import into draw.io)
```

## Disclaimer
This application is an educational project and provides general health information only. It is **not a substitute for professional medical diagnosis or advice**. Always consult a qualified healthcare provider.
