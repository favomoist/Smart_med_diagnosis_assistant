const host = typeof window !== "undefined" && window.location.hostname ? window.location.hostname : "localhost"
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
  ? import.meta.env.VITE_API_BASE_URL.replace("localhost", host).replace("127.0.0.1", host)
  : `http://${host}:8000`

export interface TokenResponse {
  access_token: string
  token_type: string
  role: string
  user_id: number
  full_name: string
}

export interface MatchedCondition {
  condition_code: string
  condition_name: string
  confidence_score: number
  confidence_level: "High" | "Medium" | "Low" | string
  category: string
  description?: string
  care_recommendations?: string
}

export interface SymptomCheckRequest {
  symptoms: string[]
  age?: number
  sex?: "male" | "female" | "other" | string
  duration_days?: number
  severity_scale?: number
  profile_id?: number
}

export interface SymptomCheckResponse {
  session_id?: number
  urgency: "emergency" | "urgent_care" | "self_care" | string
  red_flags_triggered: string[]
  possible_conditions: MatchedCondition[]
  care_advice: string
  disclaimer: string
}

export interface TriageHistoryItem {
  id: number
  profile_id?: number
  profile_name?: string
  urgency: string
  patient_age?: number
  patient_sex?: string
  duration_days?: number
  severity_scale?: number
  reported_symptoms: string[]
  possible_conditions: MatchedCondition[]
  red_flags_triggered: string[]
  care_advice: string
  created_at: string
}

export interface SharedSummaryResponse {
  token: string
  share_url: string
  expires_at: string
  is_expired: boolean
  is_revoked: boolean
  clinician_notes?: string
  session_details: TriageHistoryItem
}

export interface ConditionItem {
  id: number
  code: string
  name: string
  category: string
  typical_urgency: string
  description?: string
  advice?: string
  care_recommendations?: string
}

export interface SymptomItem {
  id: number
  code: string
  name: string
  category: string
  description?: string
  is_red_flag: boolean
  guidance?: string
}

function getAuthHeader(): HeadersInit {
  const token = localStorage.getItem("smda_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const api = {
  async login(email: string, password: string): Promise<TokenResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Login failed")
    }
    return res.json()
  },

  async checkSymptoms(payload: SymptomCheckRequest): Promise<SymptomCheckResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/triage/check`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Symptom check failed")
    }
    return res.json()
  },

  async getHistory(): Promise<TriageHistoryItem[]> {
    const res = await fetch(`${API_BASE_URL}/api/v1/triage/history`, {
      headers: {
        ...getAuthHeader(),
      },
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to load history")
    }
    return res.json()
  },

  async getSession(sessionId: number): Promise<TriageHistoryItem> {
    const res = await fetch(`${API_BASE_URL}/api/v1/triage/sessions/${sessionId}`, {
      headers: {
        ...getAuthHeader(),
      },
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to load session details")
    }
    return res.json()
  },

  async createShare(sessionId: number, validHours = 72): Promise<SharedSummaryResponse> {
    const res = await fetch(`${API_BASE_URL}/api/v1/share/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify({ session_id: sessionId, valid_hours: validHours }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to create share link")
    }
    return res.json()
  },

  async getConditions(search?: string): Promise<ConditionItem[]> {
    const url = new URL(`${API_BASE_URL}/api/v1/knowledge/conditions`)
    if (search) url.searchParams.append("search", search)
    const res = await fetch(url.toString(), {
      headers: {
        ...getAuthHeader(),
      },
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to load conditions")
    }
    return res.json()
  },

  async getSymptoms(search?: string): Promise<SymptomItem[]> {
    const url = new URL(`${API_BASE_URL}/api/v1/knowledge/symptoms`)
    if (search) url.searchParams.append("search", search)
    const res = await fetch(url.toString(), {
      headers: {
        ...getAuthHeader(),
      },
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to load symptoms")
    }
    return res.json()
  },

  async createCondition(payload: Omit<ConditionItem, "id">): Promise<ConditionItem> {
    const res = await fetch(`${API_BASE_URL}/api/v1/knowledge/conditions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || "Failed to create condition")
    }
    return res.json()
  },

  async getHealth(): Promise<{ status: string; service: string; version: string }> {
    const res = await fetch(`${API_BASE_URL}/health`)
    if (!res.ok) throw new Error("Health check failed")
    return res.json()
  },
}
