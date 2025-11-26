import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './NavBar.css'

function NavBar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/home" className="nav-link">Home</Link>
        <Link to="/track" className="nav-link">Track</Link>
        <Link to="/dashboard" className="nav-link">My Dashboard</Link>
        <button onClick={handleLogout} className="nav-link nav-logout">Logout</button>
      </div>
    </nav>
  )
}

export default NavBar

