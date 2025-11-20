import './WeeklyAverageBox.css'

function WeeklyAverageBox({ weeklyAverage }) {
  if (!weeklyAverage) {
    return (
      <div className="weekly-average-box">
        <h2>Weekly Average</h2>
        <p>No data available</p>
      </div>
    )
  }

  return (
    <div className="weekly-average-box">
      <h2>Weekly Average</h2>
      <div className="average-display">
        <div className="average-amount">₱{weeklyAverage.weekly_average.toFixed(2)}</div>
        <div className="average-period">
          Last 7 days
        </div>
      </div>
    </div>
  )
}

export default WeeklyAverageBox

