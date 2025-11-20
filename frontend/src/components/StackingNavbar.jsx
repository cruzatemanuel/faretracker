import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../contexts/AuthContext'
import './StackingNavbar.css'

const StackingNavbarItem = ({
  to,
  children,
  expanded,
  index,
  isLogout = false,
  onClick
}) => {
  const className = isLogout 
    ? 'stacking-nav-item stacking-nav-item-logout'
    : 'stacking-nav-item'

  if (isLogout) {
    return (
      <motion.div
        initial={{ x: -100 * (index + 1) }}
        animate={{ x: expanded ? 0 : -100 * (index + 1) }}
        transition={{
          duration: 0.6,
          ease: "circInOut",
          delay: 0.1 * (index + 1),
          type: "spring",
        }}
        style={{ zIndex: 100 - (index + 1) }}
      >
        <button
          className={className}
          onClick={onClick}
        >
          {children}
        </button>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ x: -100 * index }}
      animate={{ x: expanded ? 0 : -100 * index }}
      transition={{
        duration: 0.6,
        ease: "circInOut",
        delay: 0.1 * index,
        type: "spring",
      }}
      style={{ zIndex: 100 - index }}
    >
      <Link
        className={className}
        to={to}
      >
        {children}
      </Link>
    </motion.div>
  )
}

const StackingNavbar = () => {
  const [expanded, setExpanded] = useState(false)
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const items = [
    { to: "/home", label: "Home" },
    { to: "/track", label: "Track" },
    { to: "/dashboard", label: "My Dashboard" },
  ]

  return (
    <div
      className="stacking-navbar"
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
    >
      {items.map((item, index) => (
        <StackingNavbarItem
          to={item.to}
          expanded={expanded}
          key={index}
          index={index}
        >
          {item.label}
        </StackingNavbarItem>
      ))}
      <StackingNavbarItem
        expanded={expanded}
        index={items.length}
        isLogout={true}
        onClick={handleLogout}
      >
        Logout
      </StackingNavbarItem>
    </div>
  )
}

export default StackingNavbar

