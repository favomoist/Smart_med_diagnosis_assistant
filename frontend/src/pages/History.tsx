import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import { Calendar, ChevronRight, Activity, AlertTriangle, CheckCircle2, ShieldAlert, Loader2 } from "lucide-react"
import { Card, CardContent, Badge } from "../components/ui"
import { api, TriageHistoryItem } from "../lib/api"
import { useTriage } from "../context/TriageContext"

export function History() {
  const navigate = useNavigate()
  const { setActiveSession } = useTriage()
  const [historyData, setHistoryData] = useState<TriageHistoryItem[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [filter, setFilter] = useState("All")

  useEffect(() => {
    setIsLoading(true)
    api.getHistory()
      .then((data) => {
        setHistoryData(data || [])
      })
      .catch((err) => {
        setError(err?.message || "Failed to load past checks.")
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [])

  const handleCardClick = (item: TriageHistoryItem) => {
    setActiveSession(item)
    navigate("/patient/summary")
  }

  // Generate dynamic profile filters
  const uniqueProfiles = Array.from(
    new Set(historyData.map((item) => item.profile_name || "Self"))
  )
  const filterList = ["All", ...uniqueProfiles]

  const filteredItems = historyData.filter((item) => {
    if (filter === "All") return true
    const person = item.profile_name || "Self"
    return person === filter
  })

  const formatDate = (isoString: string) => {
    try {
      const date = new Date(isoString)
      return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      })
    } catch {
      return isoString
    }
  }

  const getUrgencyBadge = (urgency: string) => {
    if (urgency === "emergency") {
      return { label: "Emergency", color: "red", icon: ShieldAlert }
    }
    if (urgency === "urgent_care") {
      return { label: "Urgent Care", color: "amber", icon: AlertTriangle }
    }
    return { label: "Self-Care", color: "green", icon: CheckCircle2 }
  }

  return (
    <div className="flex flex-col min-h-full bg-background pb-20">
      <div className="bg-white px-6 py-4 pt-12 border-b sticky top-0 z-10">
        <h1 className="text-xl font-display font-semibold mb-4">Symptom Log</h1>
        
        <div className="flex gap-2 overflow-x-auto pb-2 -mx-2 px-2 snap-x">
          {filterList.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`snap-center px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                filter === f
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 space-y-3 relative before:absolute before:inset-0 before:ml-8 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-border before:to-transparent">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 gap-3">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
            <p className="text-sm text-muted-foreground">Loading past checks...</p>
          </div>
        ) : error ? (
          <div className="text-center py-12 p-4 bg-red-50 text-red-700 rounded-xl text-sm">
            {error}
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="text-center py-16 px-4 space-y-2">
            <Activity className="w-10 h-10 text-muted-foreground mx-auto" />
            <h3 className="font-semibold text-foreground">No checks recorded</h3>
            <p className="text-sm text-muted-foreground max-w-xs mx-auto">
              You haven't completed any symptom checks yet. Check your symptoms on the Home screen to build your timeline.
            </p>
          </div>
        ) : (
          filteredItems.map((item) => {
            const urgencyInfo = getUrgencyBadge(item.urgency)
            const UrgencyIcon = urgencyInfo.icon
            const personName = item.profile_name || "Self"

            return (
              <div key={item.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                
                <div className="flex items-center justify-center w-8 h-8 rounded-full border-4 border-background bg-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 ml-4 md:ml-0">
                  {urgencyInfo.color === 'red' ? (
                    <UrgencyIcon className="w-3.5 h-3.5 text-red-500" />
                  ) : urgencyInfo.color === 'amber' ? (
                    <UrgencyIcon className="w-3.5 h-3.5 text-amber-500" />
                  ) : (
                    <UrgencyIcon className="w-3.5 h-3.5 text-green-500" />
                  )}
                </div>
                
                <Card 
                  className="w-[calc(100%-3rem)] md:w-[calc(50%-2.5rem)] bg-white cursor-pointer hover:shadow-md transition-shadow ml-4 md:ml-0"
                  onClick={() => handleCardClick(item)}
                >
                  <CardContent className="p-4 flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                          {formatDate(item.created_at)}
                        </span>
                        <Badge variant="outline" className="text-[10px] py-0 px-1.5 h-4">{personName}</Badge>
                      </div>
                      <p className="text-sm font-medium text-foreground truncate max-w-[200px]">
                        {item.reported_symptoms.join(", ")}
                      </p>
                      <p className={`text-xs mt-1 font-medium ${
                        urgencyInfo.color === 'red' ? 'text-red-600' : 
                        urgencyInfo.color === 'amber' ? 'text-amber-600' : 'text-green-600'
                      }`}>
                        {urgencyInfo.label}
                      </p>
                    </div>
                    <ChevronRight className="w-4 h-4 text-muted-foreground opacity-50" />
                  </CardContent>
                </Card>

              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
