import './DataEntryForm.css'

function DataEntryForm({ formData, locations, onFormChange, onCalculate, loading }) {
  return (
    <div className="data-entry-form">
      <h2>Data Entry</h2>
      <div className="form-group">
        <label htmlFor="district">District</label>
        <select
          id="district"
          value={formData.district}
          onChange={(e) => onFormChange('district', parseInt(e.target.value))}
        >
          <option value={1}>District 1</option>
          <option value={2}>District 2</option>
          <option value={3}>District 3</option>
          <option value={4}>District 4</option>
          <option value={5}>District 5</option>
          <option value={6}>District 6</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="startLocation">Start Location</label>
        <select
          id="startLocation"
          value={formData.startLocation}
          onChange={(e) => onFormChange('startLocation', e.target.value)}
          required
        >
          <option value="">Select start location</option>
          {locations.map(loc => (
            <option key={loc} value={loc}>{loc}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="destination">Destination</label>
        <input
          type="text"
          id="destination"
          value={formData.destination}
          onChange={(e) => onFormChange('destination', e.target.value)}
          readOnly={formData.startLocation === 'BSU'}
          placeholder="Auto-set to BSU"
        />
      </div>

      <div className="form-group checkbox-group">
        <label>
          <input
            type="checkbox"
            checked={formData.includeTrike}
            onChange={(e) => onFormChange('includeTrike', e.target.checked)}
          />
          Include Trike Option
        </label>
      </div>

      <button
        type="button"
        onClick={onCalculate}
        disabled={loading || !formData.startLocation}
        className="calculate-btn"
      >
        {loading ? 'Calculating...' : 'Calculate Fare'}
      </button>
    </div>
  )
}

export default DataEntryForm

