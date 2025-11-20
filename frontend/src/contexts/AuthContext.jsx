import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is stored in localStorage
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser)
        setUser(userData)
        setIsAuthenticated(true)
      } catch (e) {
        localStorage.removeItem('user')
      }
    }
    setLoading(false)
  }, [])

  const login = async (srcode, password) => {
    try {
      const response = await api.post('/auth/login', { srcode, password })
      const { success, user: userData, message } = response.data
      
      if (success && userData) {
        // Store user in localStorage
        localStorage.setItem('user', JSON.stringify(userData))
        setUser(userData)
        setIsAuthenticated(true)
        return { success: true, user: userData }
      } else {
        return {
          success: false,
          message: message || 'Login failed. Please signup if you don\'t have an account.'
        }
      }
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || error.response?.data?.detail || 'Login failed. Please signup if you don\'t have an account.'
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

