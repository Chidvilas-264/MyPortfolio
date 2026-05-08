import os

base_dir = "C:/Portfolio/frontend/src"

pages = {
    "pages/Home.jsx": """import { motion } from 'framer-motion';
import { Download, Github, Linkedin, Mail } from 'lucide-react';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Home() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        api.get('/profile').then(res => setProfile(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center justify-center min-h-[80vh] text-center">
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 260, damping: 20 }}>
                {profile.profilePhotoPath ? (
                    <img src={`http://localhost:8080${profile.profilePhotoPath}`} alt="Profile" className="w-48 h-48 rounded-full object-cover border-4 border-blue-500 shadow-2xl mb-8" />
                ) : (
                    <div className="w-48 h-48 rounded-full bg-gray-800 border-4 border-blue-500 shadow-2xl mb-8 flex items-center justify-center text-gray-500">No Photo</div>
                )}
            </motion.div>
            
            <motion.h1 initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-5xl md:text-7xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
                {profile.fullName || "Your Name"}
            </motion.h1>
            
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }} className="text-xl md:text-2xl text-gray-400 mb-8 h-12">
                <span className="typing-text">{profile.title || "Electronics and Communication Engineer"}</span>
            </motion.div>
            
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }} className="flex flex-wrap justify-center gap-4">
                {profile.resumePath && (
                    <a href={`http://localhost:8080${profile.resumePath}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                        <Download size={20} /> Download Resume
                    </a>
                )}
                {profile.githubLink && (
                    <a href={profile.githubLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors">
                        <Github size={20} /> GitHub
                    </a>
                )}
                {profile.linkedinLink && (
                    <a href={profile.linkedinLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-blue-800 hover:bg-blue-700 text-white rounded-lg transition-colors">
                        <Linkedin size={20} /> LinkedIn
                    </a>
                )}
                <a href="/contact" className="flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors">
                    <Mail size={20} /> Contact Me
                </a>
            </motion.div>
        </motion.div>
    );
}""",
    "pages/About.jsx": """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function About() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        api.get('/profile').then(res => setProfile(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">About Me</h2>
            <div className="glass-card p-8 mb-8">
                <p className="text-lg text-gray-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Write something about yourself here."}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-card p-6">
                    <h3 className="text-xl font-semibold mb-4 text-blue-400">Education</h3>
                    <ul className="space-y-4">
                        <li className="border-l-2 border-blue-500 pl-4">
                            <h4 className="font-medium text-white">B.Tech in Electronics & Communication</h4>
                            <p className="text-sm text-gray-400">2020 - 2024</p>
                        </li>
                    </ul>
                </div>
                <div className="glass-card p-6">
                    <h3 className="text-xl font-semibold mb-4 text-purple-400">Technical Domains</h3>
                    <div className="flex flex-wrap gap-2">
                        {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map(domain => (
                            <span key={domain} className="px-3 py-1 bg-white/10 rounded-full text-sm text-gray-300">{domain}</span>
                        ))}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}""",
    "pages/SoftwareProjects.jsx": """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function SoftwareProjects() {
    const [projects, setProjects] = useState([]);
    
    useEffect(() => {
        api.get('/projects/category/Software').then(res => setProjects(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <h2 className="text-4xl font-bold mb-8 text-center text-blue-400">Software Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project, i) => (
                    <motion.div key={project.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="glass-card overflow-hidden">
                        {project.images && project.images.length > 0 && (
                            <img src={`http://localhost:8080${project.images[0].filePath}`} alt={project.title} className="w-full h-48 object-cover" />
                        )}
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-2 text-white">{project.title}</h3>
                            <p className="text-gray-400 mb-4 line-clamp-2">{project.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {project.techStack?.split(',').map(tech => (
                                    <span key={tech} className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${project.id}`} className="text-blue-400 hover:text-blue-300 font-medium">View Details →</Link>
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}""",
    "pages/HardwareProjects.jsx": """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function HardwareProjects() {
    const [projects, setProjects] = useState([]);
    
    useEffect(() => {
        api.get('/projects/category/Hardware').then(res => setProjects(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <h2 className="text-4xl font-bold mb-8 text-center text-orange-400">Hardware Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project, i) => (
                    <motion.div key={project.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="glass-card overflow-hidden">
                        {project.images && project.images.length > 0 && (
                            <img src={`http://localhost:8080${project.images[0].filePath}`} alt={project.title} className="w-full h-48 object-cover" />
                        )}
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-2 text-white">{project.title}</h3>
                            <p className="text-gray-400 mb-4 line-clamp-2">{project.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {project.techStack?.split(',').map(tech => (
                                    <span key={tech} className="px-2 py-1 bg-orange-500/20 text-orange-300 text-xs rounded">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${project.id}`} className="text-orange-400 hover:text-orange-300 font-medium">View Details →</Link>
                        </div>
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}""",
    "pages/Certifications.jsx": """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Certifications() {
    const [certs, setCerts] = useState([]);
    
    useEffect(() => {
        api.get('/certifications').then(res => setCerts(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <h2 className="text-4xl font-bold mb-8 text-center text-emerald-400">Certifications</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {certs.map((cert, i) => (
                    <motion.div key={cert.id} initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: i * 0.1 }} className="glass-card p-6 flex flex-col items-center text-center">
                        {cert.imagePath && <img src={`http://localhost:8080${cert.imagePath}`} alt={cert.title} className="w-full h-40 object-cover rounded mb-4" />}
                        <h3 className="text-xl font-bold text-white mb-2">{cert.title}</h3>
                        <p className="text-gray-400 mb-1">{cert.provider}</p>
                        <p className="text-gray-500 text-sm mb-4">{cert.date}</p>
                        {cert.verificationLink && (
                            <a href={cert.verificationLink} target="_blank" rel="noreferrer" className="mt-auto px-4 py-2 bg-white/10 hover:bg-white/20 rounded text-emerald-300 transition-colors">Verify</a>
                        )}
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}"""
}

for path, content in pages.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend pages part 1 generated successfully.")
