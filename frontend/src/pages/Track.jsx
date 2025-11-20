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
    destination: 'BSU',
    includeTrike: false
  })
  const [fareResult, setFareResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')
  const [locations, setLocations] = useState([])

  useEffect(() => {
    // Load available locations for the selected district based on the fare guide
    const districtLocations = {
      1: ['BSU', 'Balayan', 'Calaca', 'Calatagan', 'Lian', 'Nasugbu', 'Tuy', 'Taal', 'Lemery', 'Grand Terminal', 'Batangas City'],
      2: ['BSU', 'Bauan', 'Lobo', 'Mabini', 'San Luis', 'San Pascual', 'Tingloy', 'Batangas City', 'Batangas City Port', 'Lemery'],
      3: ['BSU', 'Sto. Tomas', 'Tanauan City', 'Agoncillo', 'Alitagtag', 'Balete', 'Cuenca', 'Laurel', 'Talisay', 'Malvar', 'Mataas na Kahoy', 'San Nicolas', 'Santa Teresita', 'Grand Terminal', 'Batangas City', 'Lipa City', 'Lemery'],
      4: ['BSU', 'Ibaan', 'Padre Garcia', 'Rosario', 'San Jose', 'San Juan', 'Taysan', 'Batangas'],
      5: ['BSU', 'Batangas City'],
      6: ['BSU', 'Lipa City', 'Batangas City']
    }
    setLocations(districtLocations[formData.district] || [])
  }, [formData.district])

  const handleFormChange = (field, value) => {
    setFormData(prev => {
      const newData = { ...prev, [field]: value }
      // Auto-set destination to BSU if start location is BSU
      if (field === 'startLocation' && value === 'BSU') {
        newData.destination = 'BSU'
      } else if (field === 'startLocation' && prev.startLocation === 'BSU') {
        newData.destination = 'BSU'
      }
      return newData
    })
    setFareResult(null)
    setSaveMessage('')
  }

  const handleCalculate = async () => {
    if (!formData.startLocation) {
      alert('Please select a start location')
      return
    }

    setLoading(true)
    setSaveMessage('')
    try {
      const response = await api.post(`/fare/calculate?srcode=${user?.srcode}`, {
        district: formData.district,
        start_location: formData.startLocation,
        destination: formData.destination || 'BSU',
        include_trike: formData.includeTrike
      })
      setFareResult(response.data)
    } catch (error) {
      alert(error.response?.data?.detail || 'Error calculating fare')
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
                locations={locations}
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

