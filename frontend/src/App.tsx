import { RouterProvider } from 'react-router';
import { createBrowserRouter } from "react-router";
import { RootLayout } from "./layouts/RootLayout";
import { PatientLayout } from "./layouts/PatientLayout";
import { AdminLayout } from "./layouts/AdminLayout";
import { Login } from "./pages/Login";
import { SymptomIntake } from "./pages/SymptomIntake";
import { TriageResult } from "./pages/TriageResult";
import { PossibleConditions } from "./pages/PossibleConditions";
import { History } from "./pages/History";
import { ClinicianSummary } from "./pages/ClinicianSummary";
import { AdminPanel } from "./pages/AdminPanel";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <Login /> },
      {
        path: "patient",
        element: <PatientLayout />,
        children: [
          { index: true, element: <SymptomIntake /> },
          { path: "triage", element: <TriageResult /> },
          { path: "conditions", element: <PossibleConditions /> },
          { path: "history", element: <History /> },
          { path: "summary", element: <ClinicianSummary /> }
        ]
      },
      {
        path: "admin",
        element: <AdminLayout />,
        children: [
          { index: true, element: <AdminPanel /> }
        ]
      }
    ]
  }
]);

export default function App() {
  return <RouterProvider router={router} />;
}
