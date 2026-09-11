# SMDA Frontend Web Application (SmartyMed)

Modern, responsive web client for the **Smart Medical Diagnosis Assistant (SMDA)** built with **React 19**, **TypeScript**, **Vite**, and **Tailwind CSS v4**.

---

## 🛠️ Tech Stack

- **Framework**: [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/)
- **Bundler & Dev Server**: [Vite](https://vite.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Routing**: [React Router v8](https://reactrouter.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Data Visualization**: [Recharts](https://recharts.org/)
- **Component Primitives**: Radix UI Slot, `class-variance-authority`, `clsx`, `tailwind-merge`

---

## 📁 Project Structure

```text
frontend/
├── index.html              # HTML shell & root mount point
├── package.json            # Scripts & project dependencies
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration with React & Tailwind CSS
├── src/
│   ├── main.tsx            # React application entrypoint
│   ├── App.tsx             # Main router & routes configuration
│   ├── index.css           # Global Tailwind CSS imports & theme styling
│   ├── components/         # Shared UI components
│   │   └── ui.tsx          # Buttons, cards, badges, inputs, dialogs, alerts
│   ├── layouts/            # Application layout wrappers
│   │   ├── RootLayout.tsx      # Base layout
│   │   ├── PatientLayout.tsx   # Patient portal navigation & header
│   │   └── AdminLayout.tsx     # Admin / Clinician dashboard layout
│   └── pages/              # Primary view pages
│       ├── Login.tsx               # Authentication & role selection
│       ├── SymptomIntake.tsx       # Interactive symptom intake & questionnaire
│       ├── TriageResult.tsx        # Urgency classification (Self-Care / Urgent / Emergency)
│       ├── PossibleConditions.tsx  # Matched conditions with confidence scores
│       ├── ClinicianSummary.tsx    # Shareable clinical summary & export view
│       ├── History.tsx             # Patient symptom timeline & history
│       └── AdminPanel.tsx          # Knowledge base & symptom-condition manager
```

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v20+ recommended)
- [pnpm](https://pnpm.io/) or [npm](https://www.npmjs.com/)

### 1. Install Dependencies

```bash
# Using pnpm (recommended)
pnpm install

# Or using npm
npm install
```

### 2. Run the Development Server

```bash
# Using pnpm
pnpm dev

# Or using npm
npm run dev
```

The app will be accessible at `http://localhost:5173` (or the port specified by Vite).

### 3. Build for Production

```bash
pnpm build
# or
npm run build
```

To preview the production build locally:
```bash
pnpm preview
# or
npm run preview
```

---

## 🔌 Connecting to the Backend

The frontend connects to the SMDA FastAPI backend running at `http://localhost:8000`. Ensure the backend service is started via Docker or directly using Uvicorn.
