import './FareDisplay.css'

function FareDisplay({ fareResult, onSave, saveMessage }) {
  if (!fareResult) {
    return (
      <div className="fare-display">
        <h2>Fare Result</h2>
        <p className="no-result">Calculate fare to see results</p>
      </div>
    )
  }

  const segments = fareResult.segments || []

  return (
    <div className="fare-display">
      <h2>Fare Result</h2>

      <div className="fare-route-box">
        <div className="route-box-header">
          <span>Route</span>
          <span>Vehicle</span>
          <span>Fare</span>
        </div>

        <div className="route-box-body">
          {segments.length === 0 ? (
            <p className="no-segments">No segments available</p>
          ) : (
            segments.map((segment, index) => (
              <div key={index} className="route-row">
                <span className="route-description">{segment.description}</span>
                <span className="route-vehicle">{segment.vehicle}</span>
                <span className="route-amount">₱{segment.fare.toFixed(2)}</span>
              </div>
            ))
          )}
        </div>
      </div>

      {fareResult.trike_fare > 0 && (
        <div className="trike-fare">
          <span>Trike Fare:</span>
          <span>₱{fareResult.trike_fare.toFixed(2)}</span>
        </div>
      )}

      <div className="total-fare">
        <span>Total Fare:</span>
        <span>₱{fareResult.total_fare.toFixed(2)}</span>
      </div>

      <button onClick={onSave} className="save-btn">
        Save Record
      </button>

      {saveMessage && (
        <div className="save-message">{saveMessage}</div>
      )}
    </div>
  )
}

export default FareDisplay

