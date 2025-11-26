import { useState, useEffect } from 'react'
import NavBar from '../components/NavBar'
import Footer from '../components/Footer'
import DataEntryForm from '../components/DataEntryForm'
import FareDisplay from '../components/FareDisplay'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import './Track.css'

function Track() {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    district: 1,
    startLocation: '',
    destination: '',
    includeTrike: false,
    startLocationError: '',
    destinationError: ''
  })
  const [fareResult, setFareResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')

  const handleFormChange = (field, value) => {
    setFormData(prev => {
      const newData = { ...prev, [field]: value }
      // Clear errors when user types
      if (field === 'startLocation') {
        newData.startLocationError = ''
      } else if (field === 'destination') {
        newData.destinationError = ''
      }
      // Auto-set destination to BSU if start location is BSU and destination is empty
      if (field === 'startLocation' && value.toUpperCase() === 'BSU' && !prev.destination) {
        newData.destination = 'BSU'
      }
      return newData
    })
    setFareResult(null)
    setSaveMessage('')
  }

  const handleCalculate = async () => {
    // Clear previous errors
    setFormData(prev => ({
      ...prev,
      startLocationError: '',
      destinationError: ''
    }))

    // Basic validation
    if (!formData.startLocation.trim()) {
      setFormData(prev => ({
        ...prev,
        startLocationError: 'Please enter a start location'
      }))
      return
    }

    const destination = formData.destination.trim() || 'BSU'

    setLoading(true)
    setSaveMessage('')
    try {
      const response = await api.post(`/fare/calculate?srcode=${user?.srcode}`, {
        district: formData.district,
        start_location: formData.startLocation.trim(),
        destination: destination,
        include_trike: formData.includeTrike
      })
      setFareResult(response.data)
      // Clear any errors on success
      setFormData(prev => ({
        ...prev,
        startLocationError: '',
        destinationError: ''
      }))
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error calculating fare'
      
      // Parse error message to determine which field has the issue
      if (errorMessage.includes('start location') || errorMessage.includes('Invalid start location')) {
        setFormData(prev => ({
          ...prev,
          startLocationError: errorMessage
        }))
      } else if (errorMessage.includes('destination') || errorMessage.includes('Invalid destination')) {
        setFormData(prev => ({
          ...prev,
          destinationError: errorMessage
        }))
      } else {
        // General error - show in alert for now, could be improved
        alert(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!fareResult) {
      alert('Please calculate fare first')
      return
    }

    try {
      await api.post(`/fare/save?srcode=${user?.srcode}`, {
        district: formData.district,
        start_location: formData.startLocation,
        destination: formData.destination || 'BSU',
        include_trike: formData.includeTrike,
        total_fare: fareResult.total_fare,
        trike_fare: fareResult.trike_fare,
        fare_details: JSON.stringify(fareResult.segments)
      })
      setSaveMessage('Data saved successfully!')
      setTimeout(() => setSaveMessage(''), 3000)
    } catch (error) {
      alert(error.response?.data?.detail || 'Error saving fare record')
    }
  }

  return (
    <div className="track-page">
      <NavBar />
      <div className="track-content">
        <div className="track-container">
          <h1 className="page-title">Track Fare</h1>
          
          <div className="track-grid">
            <div className="data-entry-box">
              <DataEntryForm
                formData={formData}
                onFormChange={handleFormChange}
                onCalculate={handleCalculate}
                loading={loading}
              />
            </div>
            
            <div className="fare-result-box">
              <FareDisplay
                fareResult={fareResult}
                onSave={handleSave}
                saveMessage={saveMessage}
              />
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Track

