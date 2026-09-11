import React, { createContext, useContext, useState } from "react"
import { api, SymptomCheckResponse, TriageHistoryItem } from "../lib/api"

export interface EnteredSymptom {
  name: string
  severity: number
}

interface TriageContextType {
  currentResult: SymptomCheckResponse | null
  submittedSymptoms: EnteredSymptom[]
  activeSession: TriageHistoryItem | null
  isLoading: boolean
  error: string | null
  performCheck: (symptoms: EnteredSymptom[], durationDays?: number) => Promise<SymptomCheckResponse>
  setActiveSession: (session: TriageHistoryItem | null) => void
  resetTriage: () => void
}

const TriageContext = createContext<TriageContextType | undefined>(undefined)

export function TriageProvider({ children }: { children: React.ReactNode }) {
  const [currentResult, setCurrentResult] = useState<SymptomCheckResponse | null>(null)
  const [submittedSymptoms, setSubmittedSymptoms] = useState<EnteredSymptom[]>([])
  const [activeSession, setActiveSession] = useState<TriageHistoryItem | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  const performCheck = async (symptoms: EnteredSymptom[], durationDays = 2) => {
    setIsLoading(true)
    setError(null)
    try {
      const symptomNames = symptoms.map((s) => s.name)
      const maxSeverity = symptoms.length > 0 ? Math.max(...symptoms.map((s) => s.severity)) : 5

      const response = await api.checkSymptoms({
        symptoms: symptomNames,
        severity_scale: maxSeverity,
        duration_days: durationDays,
      })

      setCurrentResult(response)
      setSubmittedSymptoms(symptoms)

      // Create local TriageHistoryItem representation for immediate ClinicianSummary view
      const sessionItem: TriageHistoryItem = {
        id: response.session_id || Date.now(),
        urgency: response.urgency,
        reported_symptoms: symptomNames,
        possible_conditions: response.possible_conditions,
        red_flags_triggered: response.red_flags_triggered,
        care_advice: response.care_advice,
        severity_scale: maxSeverity,
        duration_days: durationDays,
        created_at: new Date().toISOString(),
      }
      setActiveSession(sessionItem)

      return response
    } catch (err: any) {
      const msg = err?.message || "Failed to analyze symptoms"
      setError(msg)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const resetTriage = () => {
    setCurrentResult(null)
    setSubmittedSymptoms([])
    setActiveSession(null)
    setError(null)
  }

  return (
    <TriageContext.Provider
      value={{
        currentResult,
        submittedSymptoms,
        activeSession,
        isLoading,
        error,
        performCheck,
        setActiveSession,
        resetTriage,
      }}
    >
      {children}
    </TriageContext.Provider>
  )
}

export function useTriage() {
  const context = useContext(TriageContext)
  if (!context) {
    throw new Error("useTriage must be used within a TriageProvider")
  }
  return context
}
