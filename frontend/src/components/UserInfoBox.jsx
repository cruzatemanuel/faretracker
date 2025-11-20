import './UserInfoBox.css'

function UserInfoBox({ userInfo }) {
  if (!userInfo) {
    return (
      <div className="user-info-box">
        <h2>User Info</h2>
        <p>No user information available</p>
      </div>
    )
  }

  return (
    <div className="user-info-box">
      <h2>User Info</h2>
      <div className="user-details">
        <div className="user-detail-item">
          <span className="label">SRCODE:</span>
          <span className="value">{userInfo.srcode}</span>
        </div>
        <div className="user-detail-item">
          <span className="label">NAME:</span>
          <span className="value">{userInfo.name}</span>
        </div>
        <div className="user-detail-item">
          <span className="label">COLLEGE:</span>
          <span className="value">{userInfo.college}</span>
        </div>
      </div>
    </div>
  )
}

export default UserInfoBox

