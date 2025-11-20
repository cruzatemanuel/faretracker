import { useRef } from 'react'
import { motion, useScroll, useTransform } from 'framer-motion'
import { Link } from 'react-router-dom'
import './HeroSection.css'

const milestonesData = [
  {
    id: 1,
    name: "Calculate",
    status: "complete",
    position: { top: "70%", left: "5%" },
  },
  {
    id: 2,
    name: "Track",
    status: "complete",
    position: { top: "15%", left: "20%" },
  },
  {
    id: 3,
    name: "Manage",
    status: "in-progress",
    position: { top: "45%", left: "55%" },
  },
  {
    id: 4,
    name: "Analyze",
    status: "pending",
    position: { top: "10%", right: "10%" },
  },
];

const MilestoneMarker = ({ milestone }) => {
  const statusClasses = {
    complete: "milestone-complete",
    "in-progress": "milestone-in-progress",
    pending: "milestone-pending",
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5 }}
      whileInView={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: milestone.id * 0.3, ease: "easeOut" }}
      viewport={{ once: true, amount: 0.8 }}
      className="milestone-marker"
      style={milestone.position}
    >
      <div className="milestone-dot-container">
        <div className={`milestone-dot ${statusClasses[milestone.status]}`} />
        <div className="milestone-dot-ring" />
      </div>
      <div className="milestone-label">
        {milestone.name}
      </div>
    </motion.div>
  );
};

const AnimatedRoadmap = ({ milestones, mapImageSrc }) => {
  const targetRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: targetRef,
    offset: ["start end", "end start"],
  });

  const pathLength = useTransform(scrollYProgress, [0.15, 0.7], [0, 1]);

  return (
    <div ref={targetRef} className="animated-roadmap">
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        viewport={{ once: true, amount: 0.2 }}
        className="roadmap-background"
      >
        {mapImageSrc && (
          <img
            src={mapImageSrc}
            alt="Fare tracking roadmap"
            className="roadmap-image"
          />
        )}
      </motion.div>

      <div className="roadmap-svg-container">
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 800 400"
          preserveAspectRatio="none"
          className="roadmap-svg"
        >
          <motion.path
            d="M 50 350 Q 200 50 400 200 T 750 100"
            fill="none"
            stroke="var(--primary-red)"
            strokeWidth="3"
            strokeDasharray="10 5"
            strokeLinecap="round"
            style={{ pathLength }}
          />
        </svg>

        {milestones.map((milestone) => (
          <MilestoneMarker key={milestone.id} milestone={milestone} />
        ))}
      </div>
    </div>
  );
};

function HeroSection() {
  return (
    <div className="hero-section">
      <div className="hero-container">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="hero-title"
        >
          Discover a smarter way to manage fare data—simple, accurate, and designed to support your daily commuting needs
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="hero-description"
        >
          Track, manage, and explore your fare data—all in one seamless platform designed for convenience and accuracy.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="hero-buttons"
        >
          <Link to="/track" className="hero-btn-primary">
            Track Now!
          </Link>
          <a
            href="https://github.com/yourusername/fairfares/blob/main/README.md"
            target="_blank"
            rel="noopener noreferrer"
            className="hero-btn-outline"
          >
            See how it works
          </a>
        </motion.div>
      </div>

      <AnimatedRoadmap
        milestones={milestonesData}
        mapImageSrc="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-SsfjxCJh43Hr1dqzkbFWUGH3ICZQbH.png&w=320&q=75"
      />
    </div>
  );
}

export default HeroSection;

