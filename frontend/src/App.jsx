import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Projects from './pages/Projects';
import SoftwareProjects from './pages/SoftwareProjects';
import HardwareProjects from './pages/HardwareProjects';
import Certifications from './pages/Certifications';
import Skills from './pages/Skills';
import WorkExperience from './pages/WorkExperience';
import Contact from './pages/Contact';
import AdminLogin from './pages/AdminLogin';
import Achievements from './pages/Achievements';
import ProjectDetails from './pages/ProjectDetails';
import Education from './pages/Education';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';
import { AnimatePresence } from 'framer-motion';

function App() {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') !== 'light';
    }
    return true;
  });

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <Router>
      <ScrollToTop />
      <div className="min-h-screen bg-mesh font-sans selection:bg-stone-700/30">
        <Navbar isDark={isDark} toggleTheme={toggleTheme} />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-28 min-h-[calc(100vh-160px)]">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/education" element={<Education />} />
              <Route path="/software" element={<SoftwareProjects />} />
              <Route path="/hardware" element={<HardwareProjects />} />
              <Route path="/certifications" element={<Certifications />} />
              <Route path="/skills" element={<Skills />} />
              <Route path="/experience" element={<WorkExperience />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/admin/login" element={<AdminLogin />} />
              <Route path="/achievements" element={<Achievements />} />
              <Route path="/project/:id" element={<ProjectDetails />} />
            </Routes>
          </AnimatePresence>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
export default App;
