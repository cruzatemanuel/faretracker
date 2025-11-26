import NavBar from '../components/NavBar'
import Footer from '../components/Footer'
import HeroSection from '../components/HeroSection'
import './Home.css'

function Home() {
  return (
    <div className="home-page">
      <NavBar />
      <div className="home-content">
        <HeroSection />

        <div className="home-container">
          <section className="about-section">
            <h3>About the Program</h3>
            <p>
              The Fare Track System is a comprehensive web application designed exclusively for the students and faculty of Batangas State University. It provides a convenient and efficient way to record, track, and analyze daily fare expenses based on local routes and transportation options commonly used around the campus.
            </p>
            <p>
              With the Fare Track System, users can:
            </p>
            <ul>
              <li>Record daily fare expenses with ease</li>
              <li>Track transportation spending across different districts and routes</li>
              <li>Monitor weekly averages, spending trends, and fare history</li>
              <li>Generate simple budgeting summaries for better financial management</li>
              <li>Calculate fares for various transportation modes, including jeepneys, vans, taxis, and optional tricycle fares for more accurate route planning</li>
            </ul>
            <p>
            Developed by <b><i>Emanuel C. Cruzat</i></b> and <b><i>Crissele H. Deomampo</i></b>, the system aims to help the BatStateU community manage their transportation costs effectively through an organized and user-friendly platform.
            </p>
          </section>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Home

