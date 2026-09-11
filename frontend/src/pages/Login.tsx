import { useState } from "react"
import { useNavigate } from "react-router"
import { Activity, AlertCircle, Loader2 } from "lucide-react"
import { Button, Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui"
import { useAuth } from "../context/AuthContext"

export function Login() {
  const navigate = useNavigate()
  const { login, loginAsGuest, loginAsAdmin, isLoading } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email || !password) {
      setError("Please enter both email and password.")
      return
    }
    setError(null)
    try {
      const res = await login(email, password)
      if (res.role === "admin") {
        navigate("/admin")
      } else {
        navigate("/patient")
      }
    } catch (err: any) {
      setError(err?.message || "Invalid credentials. Please check your email and password.")
    }
  }

  const handleGuest = async () => {
    setError(null)
    try {
      await loginAsGuest()
      navigate("/patient")
    } catch (err: any) {
      setError("Unable to initialize guest session.")
    }
  }

  const handleAdmin = async () => {
    setError(null)
    try {
      await loginAsAdmin()
      navigate("/admin")
    } catch (err: any) {
      setError("Unable to log in as demo admin.")
    }
  }

  return (
    <div className="flex flex-col h-screen p-6 items-center justify-center bg-gradient-to-b from-teal-50/50 to-white">
      <div className="w-full max-w-sm space-y-8 flex flex-col items-center">
        
        <div className="flex flex-col items-center text-center space-y-3">
          <div className="bg-primary/10 p-4 rounded-2xl mb-2 text-primary">
            <Activity className="w-10 h-10" />
          </div>
          <h1 className="text-2xl font-display font-semibold tracking-tight">Smart Medical Assistant</h1>
          <p className="text-muted-foreground text-sm max-w-[280px]">
            Understand your symptoms, know when to seek care
          </p>
        </div>

        <Card className="w-full border-none shadow-xl shadow-teal-900/5">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-lg">Welcome back</CardTitle>
            <CardDescription>Sign in to continue</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {error && (
              <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <input 
                  className="flex h-12 w-full rounded-xl border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" 
                  placeholder="Email address"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                />
                <input 
                  className="flex h-12 w-full rounded-xl border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring" 
                  placeholder="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLoading}
                />
              </div>
              
              <Button className="w-full" size="lg" type="submit" disabled={isLoading}>
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Sign In"}
              </Button>
            </form>
            
            <div className="relative py-4">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Or continue as</span>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <Button variant="outline" onClick={handleGuest} disabled={isLoading}>
                Guest
              </Button>
              <Button variant="outline" onClick={handleAdmin} disabled={isLoading}>
                Admin
              </Button>
            </div>

          </CardContent>
        </Card>

        <p className="text-xs text-center text-muted-foreground max-w-[300px] leading-relaxed">
          Not a substitute for professional medical advice, diagnosis, or treatment. Always consult a healthcare provider for medical decisions.
        </p>

      </div>
    </div>
  )
}
