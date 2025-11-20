import { useState, useEffect } from 'react'
import { useNavigate, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Login.css'

function Login() {
  const [srcode, setSrcode] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    // Check for success message from signup
    if (location.state?.message) {
      setSuccess(location.state.message)
    }
  }, [location])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    const result = await login(srcode, password)
    setLoading(false)

    if (result.success) {
      navigate('/home')
    } else {
      setError(result.message)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Fair Fares</h1>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="srcode">SRCODE</label>
            <input
              type="text"
              id="srcode"
              value={srcode}
              onChange={(e) => setSrcode(e.target.value)}
              required
              placeholder="Enter your SRCODE"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>
          {success && <div className="success-message">{success}</div>}
          {error && <div className="error-message">{error}</div>}
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Logging in...' : 'Login'}
          </button>
          <div className="signup-link">
            Don't have an account? <Link to="/signup">Sign Up</Link>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login

