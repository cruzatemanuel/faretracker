import { useState, useEffect } from 'react'
import NavBar from '../components/NavBar'
import Footer from '../components/Footer'
import UserInfoBox from '../components/UserInfoBox'
import WeeklyAverageBox from '../components/WeeklyAverageBox'
import FareHistoryTable from '../components/FareHistoryTable'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import './Dashboard.css'

function Dashboard() {
  const { user } = useAuth()
  const [userInfo, setUserInfo] = useState(null)
  const [weeklyAverage, setWeeklyAverage] = useState(null)
  const [fareHistory, setFareHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const loadDashboardData = async () => {
    if (!user?.srcode) {
      setLoading(false)
      return
    }

    try {
      const [userRes, historyRes, averageRes] = await Promise.all([
        api.get(`/auth/me?srcode=${user.srcode}`),
        api.get(`/fare/user-history?srcode=${user.srcode}`),
        api.get(`/fare/weekly-average?srcode=${user.srcode}`)
      ])
      
      setUserInfo(userRes.data)
      setFareHistory(historyRes.data)
      setWeeklyAverage(averageRes.data)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (recordId) => {
    if (!window.confirm('Are you sure you want to delete this record?')) {
      return
    }

    try {
      await api.delete(`/fare/delete/${recordId}?srcode=${user?.srcode}`)
      setFareHistory(prev => prev.filter(record => record.id !== recordId))
      // Reload weekly average after deletion
      const averageRes = await api.get(`/fare/weekly-average?srcode=${user?.srcode}`)
      setWeeklyAverage(averageRes.data)
    } catch (error) {
      alert(error.response?.data?.detail || 'Error deleting record')
    }
  }

  useEffect(() => {
    loadDashboardData()
  }, [user])

  if (loading) {
    return (
      <div className="dashboard-page">
        <NavBar />
        <div className="dashboard-content">
          <div className="loading">Loading...</div>
        </div>
        <Footer />
      </div>
    )
  }

  return (
    <div className="dashboard-page">
      <NavBar />
      <div className="dashboard-content">
        <div className="dashboard-container">
          <h1 className="page-title">My Dashboard</h1>
          
          <div className="dashboard-grid">
            <UserInfoBox userInfo={userInfo} />
            <WeeklyAverageBox weeklyAverage={weeklyAverage} />
          </div>

          <div className="fare-history-section">
            <FareHistoryTable 
              fareHistory={fareHistory} 
              onDelete={handleDelete}
            />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Dashboard

