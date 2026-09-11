import React, { createContext, useContext, useState, useEffect } from "react"
import { api, TokenResponse } from "../lib/api"

export interface UserInfo {
  user_id: number
  email?: string
  full_name: string
  role: string
}

interface AuthContextType {
  user: UserInfo | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<TokenResponse>
  loginAsGuest: () => Promise<void>
  loginAsAdmin: () => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("smda_token"))
  const [user, setUser] = useState<UserInfo | null>(() => {
    const saved = localStorage.getItem("smda_user")
    return saved ? JSON.parse(saved) : null
  })
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const saveAuth = (authData: TokenResponse, email?: string) => {
    localStorage.setItem("smda_token", authData.access_token)
    const userInfo: UserInfo = {
      user_id: authData.user_id,
      email: email || `${authData.role}@example.com`,
      full_name: authData.full_name,
      role: authData.role,
    }
    localStorage.setItem("smda_user", JSON.stringify(userInfo))
    setToken(authData.access_token)
    setUser(userInfo)
  }

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const res = await api.login(email, password)
      saveAuth(res, email)
      return res
    } finally {
      setIsLoading(false)
    }
  }

  const loginAsGuest = async () => {
    setIsLoading(true)
    try {
      // Authenticate as seeded demo patient
      const res = await api.login("patient@example.com", "patient123")
      saveAuth(res, "patient@example.com")
    } catch {
      // Fallback guest session in memory/local
      const guestInfo: UserInfo = {
        user_id: 9999,
        email: "guest@smda.local",
        full_name: "Guest Patient",
        role: "patient",
      }
      localStorage.setItem("smda_user", JSON.stringify(guestInfo))
      setUser(guestInfo)
    } finally {
      setIsLoading(false)
    }
  }

  const loginAsAdmin = async () => {
    setIsLoading(true)
    try {
      // Authenticate as seeded demo admin
      const res = await api.login("admin@example.com", "admin123")
      saveAuth(res, "admin@example.com")
    } catch {
      const adminInfo: UserInfo = {
        user_id: 1,
        email: "admin@example.com",
        full_name: "Admin User",
        role: "admin",
      }
      localStorage.setItem("smda_user", JSON.stringify(adminInfo))
      setUser(adminInfo)
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem("smda_token")
    localStorage.removeItem("smda_user")
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token || !!user,
        isLoading,
        login,
        loginAsGuest,
        loginAsAdmin,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
