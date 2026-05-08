import os

base_dir = "C:/Portfolio/frontend/src"

pages_content = {
    "pages/Home.jsx": """import { motion } from 'framer-motion';
import { Download, Mail } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Home() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        api.get('/profile').then(res => setProfile(res.data)).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center justify-center min-h-[70vh] text-center">
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 260, damping: 20 }}>
                {profile.profilePhotoPath ? (
                    <img src={`http://localhost:8080${profile.profilePhotoPath}`} alt="Profile" className="w-48 h-48 md:w-56 md:h-56 rounded-full object-cover border-4 border-violet-500/30 dark:border-violet-500/50 shadow-2xl mb-8 ring-4 ring-white dark:ring-slate-900" />
                ) : (
                    <div className="w-48 h-48 md:w-56 md:h-56 rounded-full bg-slate-200 dark:bg-slate-800 border-4 border-violet-500/30 dark:border-violet-500/50 shadow-2xl mb-8 flex items-center justify-center text-slate-400 dark:text-slate-500 ring-4 ring-white dark:ring-slate-900">No Photo</div>
                )}
            </motion.div>
            
            <motion.h1 initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-5xl md:text-7xl font-extrabold mb-4 tracking-tight text-slate-800 dark:text-white">
                {profile.fullName || "Your Name"}
            </motion.h1>
            
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }} className="text-xl md:text-2xl text-violet-600 dark:text-violet-400 mb-10 font-medium">
                <span className="typing-text">{profile.title || "Electronics and Communication Engineer"}</span>
            </motion.div>
            
            <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }} className="flex flex-wrap justify-center gap-4">
                {profile.resumePath && (
                    <a href={`http://localhost:8080${profile.resumePath}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-violet-600 hover:bg-violet-700 text-white rounded-xl shadow-lg shadow-violet-500/30 transition-all hover:-translate-y-1">
                        <Download size={20} /> Download Resume
                    </a>
                )}
                {profile.githubLink && (
                    <a href={profile.githubLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-slate-900 hover:bg-slate-800 dark:bg-slate-800 dark:hover:bg-slate-700 text-white rounded-xl shadow-lg transition-all hover:-translate-y-1">
                        <FaGithub size={20} /> GitHub
                    </a>
                )}
                {profile.linkedinLink && (
                    <a href={profile.linkedinLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-[#0A66C2] hover:bg-[#004182] text-white rounded-xl shadow-lg transition-all hover:-translate-y-1">
                        <FaLinkedin size={20} /> LinkedIn
                    </a>
                )}
                <a href="/contact" className="flex items-center gap-2 px-6 py-3 bg-fuchsia-600 hover:bg-fuchsia-700 text-white rounded-xl shadow-lg shadow-fuchsia-500/30 transition-all hover:-translate-y-1">
                    <Mail size={20} /> Contact Me
                </a>
            </motion.div>
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
            <div className="text-center mb-12">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-800 dark:text-white mb-4">Software <span className="text-violet-600 dark:text-violet-400">Projects</span></h2>
                <p className="text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">Explore my latest full-stack and software engineering endeavors.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map((project, i) => (
                    <motion.div key={project.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="glass-card overflow-hidden group">
                        {project.images && project.images.length > 0 ? (
                            <div className="h-48 overflow-hidden relative">
                                <img src={`http://localhost:8080${project.images[0].filePath}`} alt={project.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            </div>
                        ) : (
                            <div className="h-48 bg-slate-200 dark:bg-slate-800"></div>
                        )}
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors">{project.title}</h3>
                            <p className="text-slate-600 dark:text-slate-400 mb-6 line-clamp-2 text-sm">{project.description}</p>
                            <div className="flex flex-wrap gap-2 mb-6">
                                {project.techStack?.split(',').map(tech => (
                                    <span key={tech} className="px-2.5 py-1 bg-violet-100 text-violet-700 dark:bg-violet-500/10 dark:text-violet-300 text-xs font-semibold rounded-lg">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${project.id}`} className="inline-flex items-center justify-center w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-white rounded-lg transition-colors text-sm font-semibold">View Details</Link>
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
            <div className="text-center mb-12">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-800 dark:text-white mb-4">Hardware <span className="text-orange-600 dark:text-orange-400">Projects</span></h2>
                <p className="text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">Discover my embedded systems, FPGA designs, and robotic engineering work.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map((project, i) => (
                    <motion.div key={project.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="glass-card overflow-hidden group">
                        {project.images && project.images.length > 0 ? (
                            <div className="h-48 overflow-hidden relative">
                                <img src={`http://localhost:8080${project.images[0].filePath}`} alt={project.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            </div>
                        ) : (
                            <div className="h-48 bg-slate-200 dark:bg-slate-800"></div>
                        )}
                        <div className="p-6">
                            <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white group-hover:text-orange-600 dark:group-hover:text-orange-400 transition-colors">{project.title}</h3>
                            <p className="text-slate-600 dark:text-slate-400 mb-6 line-clamp-2 text-sm">{project.description}</p>
                            <div className="flex flex-wrap gap-2 mb-6">
                                {project.techStack?.split(',').map(tech => (
                                    <span key={tech} className="px-2.5 py-1 bg-orange-100 text-orange-700 dark:bg-orange-500/10 dark:text-orange-300 text-xs font-semibold rounded-lg">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${project.id}`} className="inline-flex items-center justify-center w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-white rounded-lg transition-colors text-sm font-semibold">View Details</Link>
                        </div>
                    </motion.div>
                ))}
            </div>
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
            <h2 className="text-4xl md:text-5xl font-black tracking-tight mb-12 text-center text-slate-800 dark:text-white">About <span className="text-fuchsia-600 dark:text-fuchsia-400">Me</span></h2>
            <div className="glass-card p-8 md:p-10 mb-10 border-t-4 border-t-violet-500">
                <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Write something about yourself here."}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="glass-card p-8">
                    <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-2">
                        <span className="w-8 h-8 rounded bg-violet-100 dark:bg-violet-900/50 flex items-center justify-center text-violet-600 dark:text-violet-400 text-lg">🎓</span>
                        Education
                    </h3>
                    <ul className="space-y-6">
                        <li className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2 before:h-2 before:bg-violet-500 before:rounded-full after:absolute after:left-[3px] after:top-4 after:w-0.5 after:h-full after:bg-slate-200 dark:after:bg-slate-800">
                            <h4 className="font-bold text-slate-800 dark:text-white text-lg">B.Tech in Electronics & Communication</h4>
                            <p className="text-sm font-medium text-violet-600 dark:text-violet-400 mt-1">2020 - 2024</p>
                        </li>
                    </ul>
                </div>
                <div className="glass-card p-8">
                    <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-2">
                        <span className="w-8 h-8 rounded bg-fuchsia-100 dark:bg-fuchsia-900/50 flex items-center justify-center text-fuchsia-600 dark:text-fuchsia-400 text-lg">⚡</span>
                        Technical Domains
                    </h3>
                    <div className="flex flex-wrap gap-2.5">
                        {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map(domain => (
                            <span key={domain} className="px-4 py-2 bg-slate-100 dark:bg-slate-800 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300 shadow-sm border border-slate-200 dark:border-slate-700">{domain}</span>
                        ))}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}"""
}

for path, content in pages_content.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Pages UI updated successfully.")
