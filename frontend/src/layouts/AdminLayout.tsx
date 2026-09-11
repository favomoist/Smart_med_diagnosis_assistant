import { useEffect } from "react"
import { Outlet, NavLink, useNavigate } from "react-router"
import { LayoutDashboard, Database, Activity, LogOut } from "lucide-react"
import { useAuth } from "../context/AuthContext"

export function AdminLayout() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/")
    }
  }, [isAuthenticated, navigate])

  if (!isAuthenticated) {
    return null
  }

  const handleSignOut = () => {
    logout()
    navigate("/")
  }

  return (
    <div className="flex h-screen h-[100dvh] bg-muted/30">
      <aside className="w-20 md:w-64 bg-white border-r flex flex-col items-center md:items-start md:px-4 py-6 z-10 shrink-0">
        <div className="flex items-center gap-2 px-2 md:mb-8 text-primary font-display font-semibold">
          <Activity className="w-8 h-8" />
          <span className="hidden md:inline text-lg">HealthAdmin</span>
        </div>
        
        <nav className="flex-1 w-full flex flex-col gap-2 mt-8 md:mt-0">
          <NavLink 
            to="/admin" 
            end
            className={({ isActive }) => `flex items-center gap-3 p-3 rounded-lg transition-colors ${isActive ? 'bg-primary/10 text-primary font-medium' : 'text-muted-foreground hover:bg-muted'}`}
          >
            <LayoutDashboard className="w-6 h-6" />
            <span className="hidden md:inline">Dashboard</span>
          </NavLink>
          <div className="flex items-center gap-3 p-3 rounded-lg text-primary/80 font-medium">
            <Database className="w-6 h-6" />
            <span className="hidden md:inline">Knowledge Base</span>
          </div>
        </nav>

        {user && (
          <div className="px-3 py-2 text-xs text-muted-foreground hidden md:block w-full truncate">
            Logged in as <span className="font-semibold text-foreground">{user.full_name}</span>
          </div>
        )}

        <button 
          onClick={handleSignOut}
          className="w-full flex items-center justify-center md:justify-start gap-3 p-3 rounded-lg text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-colors mt-auto"
        >
          <LogOut className="w-6 h-6" />
          <span className="hidden md:inline font-medium">Sign Out</span>
        </button>
      </aside>
      
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}
