import os

base_dir = "C:/Portfolio/frontend/src"
dirs = ["pages", "components", "api"]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {
    "api/axiosConfig.js": """import axios from 'axios';
const api = axios.create({
    baseURL: 'http://localhost:8080/api'
});
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
export default api;
""",
    "App.jsx": """import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import SoftwareProjects from './pages/SoftwareProjects';
import HardwareProjects from './pages/HardwareProjects';
import Certifications from './pages/Certifications';
import Skills from './pages/Skills';
import Contact from './pages/Contact';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import ProjectDetails from './pages/ProjectDetails';
import { AnimatePresence } from 'framer-motion';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white font-sans selection:bg-blue-500 selection:text-white">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/software" element={<SoftwareProjects />} />
              <Route path="/hardware" element={<HardwareProjects />} />
              <Route path="/certifications" element={<Certifications />} />
              <Route path="/skills" element={<Skills />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/admin/login" element={<AdminLogin />} />
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
              <Route path="/project/:id" element={<ProjectDetails />} />
            </Routes>
          </AnimatePresence>
        </main>
      </div>
    </Router>
  );
}
export default App;
""",
    "main.jsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",
    "index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-900 text-white;
  }
}

.glass-card {
  @apply bg-white/10 backdrop-blur-md border border-white/20 rounded-xl shadow-xl hover:bg-white/15 transition-all duration-300;
}
""",
    "components/Navbar.jsx": """import { Link } from 'react-router-dom';
import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { motion } from 'framer-motion';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const links = [
        { name: 'Home', path: '/' },
        { name: 'About', path: '/about' },
        { name: 'Software', path: '/software' },
        { name: 'Hardware', path: '/hardware' },
        { name: 'Certifications', path: '/certifications' },
        { name: 'Skills', path: '/skills' },
        { name: 'Contact', path: '/contact' },
    ];
    return (
        <nav className="fixed w-full top-0 z-50 bg-gray-900/80 backdrop-blur-md border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        Portfolio
                    </Link>
                    <div className="hidden md:flex space-x-4">
                        {links.map(link => (
                            <Link key={link.name} to={link.path} className="text-gray-300 hover:text-white transition-colors">
                                {link.name}
                            </Link>
                        ))}
                    </div>
                    <div className="md:hidden">
                        <button onClick={() => setIsOpen(!isOpen)} className="text-gray-300 hover:text-white">
                            {isOpen ? <X /> : <Menu />}
                        </button>
                    </div>
                </div>
            </div>
            {isOpen && (
                <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="md:hidden bg-gray-800">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {links.map(link => (
                            <Link key={link.name} to={link.path} onClick={() => setIsOpen(false)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-700">
                                {link.name}
                            </Link>
                        ))}
                    </div>
                </motion.div>
            )}
        </nav>
    );
};
export default Navbar;
"""
}

for path, content in files.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend setup generated successfully.")
