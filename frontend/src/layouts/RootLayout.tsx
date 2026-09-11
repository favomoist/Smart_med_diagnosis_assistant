import { Outlet } from "react-router"
import { AuthProvider } from "../context/AuthContext"
import { TriageProvider } from "../context/TriageContext"

export function RootLayout() {
  return (
    <AuthProvider>
      <TriageProvider>
        <div className="min-h-screen bg-background text-foreground selection:bg-teal-100 selection:text-teal-900 font-sans">
          <main className="mx-auto max-w-md bg-white shadow-xl min-h-screen relative overflow-hidden sm:max-w-xl md:max-w-3xl xl:max-w-5xl">
            <Outlet />
          </main>
        </div>
      </TriageProvider>
    </AuthProvider>
  )
}
