import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import { Search, Plus, X, ArrowRight, Loader2, AlertCircle } from "lucide-react"
import { Button, Card, CardContent, Badge } from "../components/ui"
import { useTriage, EnteredSymptom } from "../context/TriageContext"
import { api, SymptomItem } from "../lib/api"

const DEFAULT_POPULAR_SYMPTOMS = ["Headache", "Fever", "Cough", "Fatigue", "Nausea", "Sore throat"]

export function SymptomIntake() {
  const navigate = useNavigate()
  const { performCheck, isLoading, error: triageError } = useTriage()
  const [symptoms, setSymptoms] = useState<EnteredSymptom[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [popularSymptoms, setPopularSymptoms] = useState<string[]>(DEFAULT_POPULAR_SYMPTOMS)
  const [suggestions, setSuggestions] = useState<SymptomItem[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [localError, setLocalError] = useState<string | null>(null)

  // Fetch real symptoms from the knowledge base to populate suggestions
  useEffect(() => {
    api.getSymptoms()
      .then((data) => {
        if (data && data.length > 0) {
          const names = data.slice(0, 6).map((s) => s.name)
          setPopularSymptoms(names)
        }
      })
      .catch(() => {
        // Fallback to defaults if backend unavailable
      })
  }, [])

  // Dynamic autocomplete on search input
  useEffect(() => {
    if (!searchTerm.trim() || searchTerm.length < 2) {
      setSuggestions([])
      return
    }

    const timer = setTimeout(() => {
      setIsSearching(true)
      api.getSymptoms(searchTerm.trim())
        .then((items) => {
          setSuggestions(items.slice(0, 5))
        })
        .catch(() => {
          setSuggestions([])
        })
        .finally(() => {
          setIsSearching(false)
        })
    }, 250)

    return () => clearTimeout(timer)
  }, [searchTerm])

  const addSymptom = (name: string) => {
    if (!symptoms.find((s) => s.name.toLowerCase() === name.toLowerCase())) {
      setSymptoms([...symptoms, { name, severity: 5 }])
    }
    setSearchTerm("")
    setSuggestions([])
  }

  const removeSymptom = (name: string) => {
    setSymptoms(symptoms.filter((s) => s.name !== name))
  }

  const handleSubmit = async () => {
    if (symptoms.length === 0) return
    setLocalError(null)
    try {
      await performCheck(symptoms, 2)
      navigate("/patient/triage")
    } catch (err: any) {
      setLocalError(err?.message || "Error analyzing symptoms. Please try again.")
    }
  }

  return (
    <div className="flex flex-col min-h-full bg-background">
      <div className="bg-white px-6 py-4 pt-12 border-b sticky top-0 z-10">
        <h1 className="text-xl font-display font-semibold mb-1">Check Symptoms</h1>
        <p className="text-sm text-muted-foreground">What's bothering you today?</p>
        
        <div className="w-full bg-secondary h-1.5 rounded-full mt-4 overflow-hidden">
          <div className="bg-primary w-1/3 h-full rounded-full" />
        </div>
      </div>

      <div className="p-6 space-y-6 flex-1">
        {(localError || triageError) && (
          <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{localError || triageError}</span>
          </div>
        )}

        <div className="relative">
          <Search className="absolute left-3 top-3.5 h-5 w-5 text-muted-foreground" />
          <input
            className="flex h-12 w-full rounded-xl border border-input bg-white pl-10 pr-4 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Search symptoms (e.g. headache, fever)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && searchTerm.trim()) {
                addSymptom(searchTerm.trim())
              }
            }}
          />

          {/* Autocomplete dropdown */}
          {suggestions.length > 0 && (
            <div className="absolute top-14 left-0 right-0 bg-white border border-border rounded-xl shadow-lg z-20 overflow-hidden divide-y divide-border">
              {suggestions.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => addSymptom(item.name)}
                  className="w-full text-left px-4 py-2.5 text-sm hover:bg-teal-50 transition-colors flex items-center justify-between"
                >
                  <span className="font-medium text-foreground">{item.name}</span>
                  <span className="text-xs text-muted-foreground">{item.category}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {symptoms.length === 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-muted-foreground">Common symptoms</h3>
            <div className="flex flex-wrap gap-2">
              {popularSymptoms.map((s) => (
                <button
                  key={s}
                  onClick={() => addSymptom(s)}
                  className="inline-flex items-center gap-1 rounded-full border border-border bg-white px-3 py-1.5 text-sm transition-colors hover:bg-secondary hover:text-secondary-foreground hover:border-secondary"
                >
                  <Plus className="w-3.5 h-3.5" /> {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {symptoms.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-foreground">Added symptoms ({symptoms.length})</h3>
            {symptoms.map((s) => (
              <Card key={s.name} className="overflow-visible">
                <CardContent className="p-4 relative">
                  <button 
                    onClick={() => removeSymptom(s.name)}
                    className="absolute -top-2 -right-2 bg-destructive text-white rounded-full p-1 shadow-md hover:scale-105 transition-transform"
                    aria-label="Remove symptom"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-medium text-base">{s.name}</span>
                    <Badge variant="outline" className="text-muted-foreground">Today</Badge>
                  </div>
                  
                  <div className="space-y-2 mt-4">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Mild (1)</span>
                      <span>Moderate (5)</span>
                      <span>Severe (10)</span>
                    </div>
                    <input 
                      type="range" 
                      min="1" 
                      max="10" 
                      className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                      value={s.severity}
                      onChange={(e) => setSymptoms(symptoms.map((sym) => sym.name === s.name ? {...sym, severity: parseInt(e.target.value)} : sym))}
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
            
            <button 
              onClick={() => {
                if (searchTerm.trim()) addSymptom(searchTerm.trim())
              }}
              className="text-primary text-sm font-medium inline-flex items-center gap-1.5 pt-2 hover:underline"
            >
              <Plus className="w-4 h-4" /> Add another symptom
            </button>
          </div>
        )}
      </div>

      <div className="p-6 bg-white border-t mt-auto sticky bottom-0 z-10 pb-24">
        <Button 
          className="w-full flex justify-between group" 
          size="lg"
          disabled={symptoms.length === 0 || isLoading}
          onClick={handleSubmit}
        >
          <span>{isLoading ? "Evaluating Symptoms..." : "Continue"}</span>
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          )}
        </Button>
      </div>
    </div>
  )
}
