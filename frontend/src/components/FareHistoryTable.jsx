import './FareHistoryTable.css'

function FareHistoryTable({ fareHistory, onDelete }) {
  if (!fareHistory || fareHistory.length === 0) {
    return (
      <div className="fare-history-table">
        <h2>Fare History</h2>
        <p className="no-records">No fare records found</p>
      </div>
    )
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="fare-history-table">
      <h2>Fare History</h2>
      <table>
        <thead>
          <tr>
            <th>Start</th>
            <th>Destination</th>
            <th>Total Fare</th>
            <th>Date/Time</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {fareHistory.map(record => (
            <tr key={record.id}>
              <td>{record.start_location}</td>
              <td>{record.destination}</td>
              <td>₱{record.total_fare.toFixed(2)}</td>
              <td>{formatDate(record.created_at)}</td>
              <td>
                <button
                  onClick={() => onDelete(record.id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default FareHistoryTable

