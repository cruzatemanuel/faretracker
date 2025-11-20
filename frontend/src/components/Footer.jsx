import { Link } from 'react-router-dom'
import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-links">
          <Link to="/home">Home</Link>
          <Link to="/track">Track</Link>
          <Link to="/dashboard">My Dashboard</Link>
        </div>
        <div className="footer-credits">
          <p>&copy; 2024 Fair Fares. All rights reserved.</p>
          <p>Fare Data Management and Analysis System</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

