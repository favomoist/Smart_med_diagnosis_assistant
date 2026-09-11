import { useEffect } from "react"
import { Outlet, NavLink, useNavigate } from "react-router"
import { Home, ClipboardList, LogOut } from "lucide-react"
import { useAuth } from "../context/AuthContext"

export function PatientLayout() {
  const { isAuthenticated, logout, user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/")
    }
  }, [isAuthenticated, navigate])

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="flex flex-col h-screen h-[100dvh] bg-background">
      <div className="flex-1 overflow-y-auto pb-20">
        <Outlet />
      </div>
      
      <nav className="fixed bottom-0 w-full max-w-md sm:max-w-xl md:max-w-3xl xl:max-w-5xl mx-auto bg-white border-t border-border flex justify-around items-center p-3 z-50">
        <NavLink 
          to="/patient" 
          end
          className={({ isActive }) => `flex flex-col items-center gap-1 text-xs font-medium transition-colors ${isActive ? 'text-primary' : 'text-muted-foreground'}`}
        >
          <Home className="w-6 h-6" />
          <span>Home</span>
        </NavLink>
        <NavLink 
          to="/patient/history" 
          className={({ isActive }) => `flex flex-col items-center gap-1 text-xs font-medium transition-colors ${isActive ? 'text-primary' : 'text-muted-foreground'}`}
        >
          <ClipboardList className="w-6 h-6" />
          <span>History</span>
        </NavLink>
        <button 
          onClick={() => {
            logout()
            navigate("/")
          }}
          className="flex flex-col items-center gap-1 text-xs font-medium text-muted-foreground hover:text-destructive transition-colors"
        >
          <LogOut className="w-6 h-6" />
          <span>{user?.full_name?.split(" ")[0] || "Sign Out"}</span>
        </button>
      </nav>
    </div>
  )
}
