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
              Fair Fares is a comprehensive web application designed for efficient fare data 
              management and analysis. This system allows users to track transportation fares 
              across different districts, calculate route costs, and maintain a personal history 
              of fare records.
            </p>
            <p>
              With Fair Fares, you can:
            </p>
            <ul>
              <li>Calculate fares for routes across multiple districts</li>
              <li>Track your transportation expenses over time</li>
              <li>View weekly averages and fare history</li>
              <li>Manage your fare records with ease</li>
            </ul>
            <p>
              The system supports fare calculations for various transportation modes including 
              jeepneys, vans, and taxis, with optional trike fare calculations for enhanced 
              route planning.
            </p>
          </section>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Home

