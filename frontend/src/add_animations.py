import os

base_dir = "C:/Portfolio/frontend/src/pages"

# HOME PAGE
home_content = """import { motion } from 'framer-motion';
import { Download, Mail } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Home() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        api.get('/profile').then(res => setProfile(res.data)).catch(console.error);
    }, []);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.2, delayChildren: 0.1 } }
    };
    
    const itemVariants = {
        hidden: { y: 40, opacity: 0 },
        visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 100, damping: 15 } }
    };

    return (
        <div className="flex flex-col items-center justify-center text-center pb-20 overflow-hidden">
            
            {/* HERO SECTION */}
            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="min-h-[80vh] flex flex-col items-center justify-center w-full mb-16">
                <motion.div variants={itemVariants} className="relative group">
                    <div className="absolute -inset-1 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                    {profile.profilePhotoPath ? (
                        <img src={`http://localhost:8080${profile.profilePhotoPath}`} alt="Profile" className="relative w-48 h-48 md:w-56 md:h-56 rounded-full object-cover border-4 border-slate-800 shadow-2xl mb-8 ring-4 ring-emerald-500/30" />
                    ) : (
                        <div className="relative w-48 h-48 md:w-56 md:h-56 rounded-full bg-slate-200 dark:bg-slate-800 border-4 border-emerald-500/30 shadow-2xl mb-8 flex items-center justify-center text-slate-400 dark:text-slate-500 ring-4 ring-white dark:ring-slate-900">No Photo</div>
                    )}
                </motion.div>
                
                <motion.h1 variants={itemVariants} className="text-5xl md:text-7xl font-black mb-4 tracking-tight text-slate-800 dark:text-white bg-clip-text">
                    {profile.fullName || "Your Name"}
                </motion.h1>
                
                <motion.div variants={itemVariants} className="text-xl md:text-2xl text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500 dark:from-emerald-400 dark:to-teal-300 mb-10 font-bold tracking-wide">
                    {profile.title || "Electronics and Communication Engineer"}
                </motion.div>
                
                <motion.div variants={itemVariants} className="flex flex-wrap justify-center gap-4">
                    {profile.resumePath && (
                        <a href={`http://localhost:8080${profile.resumePath}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-[0_0_20px_rgba(16,185,129,0.3)] transition-all hover:-translate-y-1 hover:shadow-[0_0_25px_rgba(16,185,129,0.5)]">
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
                    <a href="/contact" className="flex items-center gap-2 px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white rounded-xl shadow-[0_0_20px_rgba(20,184,166,0.3)] transition-all hover:-translate-y-1">
                        <Mail size={20} /> Contact Me
                    </a>
                </motion.div>
            </motion.div>

            {/* ABOUT SECTION */}
            <motion.div variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }} className="max-w-4xl w-full mx-auto text-left px-4">
                <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-black tracking-tight mb-12 text-center text-slate-800 dark:text-white">About <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">Me</span></motion.h2>
                
                <motion.div variants={itemVariants} className="glass-card p-8 md:p-10 mb-10 border-t-4 border-t-emerald-500 shadow-xl hover:shadow-emerald-500/10 transition-shadow duration-500">
                    <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Write something about yourself here in the Admin Dashboard."}</p>
                </motion.div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-lg hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-100 to-emerald-200 dark:from-emerald-900/50 dark:to-emerald-800/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 text-xl shadow-inner">🎓</span>
                            Education
                        </h3>
                        <ul className="space-y-6">
                            <li className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2.5 before:h-2.5 before:bg-emerald-500 before:rounded-full before:shadow-[0_0_10px_rgba(16,185,129,0.8)] after:absolute after:left-[4px] after:top-4 after:w-0.5 after:h-full after:bg-gradient-to-b after:from-emerald-500 after:to-transparent">
                                <h4 className="font-bold text-slate-800 dark:text-white text-lg">B.Tech in Electronics & Communication</h4>
                                <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-1 uppercase tracking-wider">2020 - 2024</p>
                            </li>
                        </ul>
                    </motion.div>
                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-lg hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-100 to-teal-200 dark:from-teal-900/50 dark:to-teal-800/50 flex items-center justify-center text-teal-600 dark:text-teal-400 text-xl shadow-inner">⚡</span>
                            Technical Domains
                        </h3>
                        <div className="flex flex-wrap gap-3">
                            {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map((domain, i) => (
                                <motion.span whileHover={{ scale: 1.05 }} key={domain} className="px-4 py-2 bg-white dark:bg-slate-800/80 rounded-lg text-sm font-bold text-slate-700 dark:text-slate-200 shadow-md border border-slate-100 dark:border-slate-700/50 cursor-default">{domain}</motion.span>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </motion.div>
        </div>
    );
}
"""

with open(os.path.join(base_dir, "Home.jsx"), "w", encoding="utf-8") as f:
    f.write(home_content)


# SOFTWARE PROJECTS PAGE
software_content = """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function SoftwareProjects() {
    const [projects, setProjects] = useState([]);
    
    useEffect(() => {
        api.get('/projects/category/Software').then(res => setProjects(res.data));
    }, []);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.15 } }
    };
    
    const itemVariants = {
        hidden: { y: 50, opacity: 0, scale: 0.95 },
        visible: { y: 0, opacity: 1, scale: 1, transition: { type: 'spring', stiffness: 100 } }
    };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4">
            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-black tracking-tight mb-4 text-center text-slate-800 dark:text-white">Software <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">Engineering</span></motion.h2>
            <motion.p variants={itemVariants} className="text-center text-slate-500 dark:text-slate-400 mb-12 text-lg">Full-stack applications, scripts, and algorithms.</motion.p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map((p, index) => (
                    <motion.div key={p.id} variants={itemVariants} whileHover={{ y: -10 }} className="glass-card rounded-2xl overflow-hidden border border-slate-200/50 dark:border-white/5 shadow-xl hover:shadow-emerald-500/20 transition-all duration-300 group flex flex-col h-full">
                        <div className="h-48 overflow-hidden bg-slate-200 dark:bg-slate-800 relative">
                            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
                                <span className="text-white font-bold tracking-wider uppercase text-sm">View Project</span>
                            </div>
                            {p.images && p.images.length > 0 ? (
                                <img src={`http://localhost:8080${p.images[0].filePath}`} alt={p.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-in-out" />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-slate-400 font-medium">No Image</div>
                            )}
                        </div>
                        <div className="p-6 flex-1 flex flex-col">
                            <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white group-hover:text-emerald-500 transition-colors">{p.title}</h3>
                            <p className="text-slate-600 dark:text-slate-300 text-sm line-clamp-3 mb-4 flex-1">{p.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {p.techStack && p.techStack.split(',').slice(0,3).map(tech => (
                                    <span key={tech} className="text-xs font-bold px-2.5 py-1 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-md border border-emerald-200 dark:border-emerald-500/20">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${p.id}`} className="block text-center w-full py-3 rounded-xl bg-slate-900 dark:bg-slate-800 hover:bg-emerald-600 dark:hover:bg-emerald-600 text-white font-bold transition-colors shadow-md">Details</Link>
                        </div>
                    </motion.div>
                ))}
            </div>
            {projects.length === 0 && <motion.p variants={itemVariants} className="text-center text-slate-500 mt-10 text-xl font-medium">No software projects uploaded yet.</motion.p>}
        </motion.div>
    );
}
"""
with open(os.path.join(base_dir, "SoftwareProjects.jsx"), "w", encoding="utf-8") as f:
    f.write(software_content)


# HARDWARE PROJECTS PAGE
hardware_content = """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function HardwareProjects() {
    const [projects, setProjects] = useState([]);
    useEffect(() => { api.get('/projects/category/Hardware').then(res => setProjects(res.data)); }, []);

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 50, opacity: 0, scale: 0.95 }, visible: { y: 0, opacity: 1, scale: 1, transition: { type: 'spring', stiffness: 100 } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4">
            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-black tracking-tight mb-4 text-center text-slate-800 dark:text-white">Hardware <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-500">Engineering</span></motion.h2>
            <motion.p variants={itemVariants} className="text-center text-slate-500 dark:text-slate-400 mb-12 text-lg">Circuit design, FPGA implementations, and embedded systems.</motion.p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map(p => (
                    <motion.div key={p.id} variants={itemVariants} whileHover={{ y: -10 }} className="glass-card rounded-2xl overflow-hidden border border-slate-200/50 dark:border-white/5 shadow-xl hover:shadow-orange-500/20 transition-all duration-300 group flex flex-col h-full">
                        <div className="h-48 overflow-hidden bg-slate-200 dark:bg-slate-800 relative">
                            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 to-transparent z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end p-4">
                                <span className="text-white font-bold tracking-wider uppercase text-sm">View Project</span>
                            </div>
                            {p.images && p.images.length > 0 ? (
                                <img src={`http://localhost:8080${p.images[0].filePath}`} alt={p.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-in-out" />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-slate-400 font-medium">No Image</div>
                            )}
                        </div>
                        <div className="p-6 flex-1 flex flex-col">
                            <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white group-hover:text-orange-500 transition-colors">{p.title}</h3>
                            <p className="text-slate-600 dark:text-slate-300 text-sm line-clamp-3 mb-4 flex-1">{p.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {p.techStack && p.techStack.split(',').slice(0,3).map(tech => (
                                    <span key={tech} className="text-xs font-bold px-2.5 py-1 bg-orange-50 dark:bg-orange-500/10 text-orange-600 dark:text-orange-400 rounded-md border border-orange-200 dark:border-orange-500/20">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${p.id}`} className="block text-center w-full py-3 rounded-xl bg-slate-900 dark:bg-slate-800 hover:bg-orange-500 dark:hover:bg-orange-600 text-white font-bold transition-colors shadow-md">Details</Link>
                        </div>
                    </motion.div>
                ))}
            </div>
            {projects.length === 0 && <motion.p variants={itemVariants} className="text-center text-slate-500 mt-10 text-xl font-medium">No hardware projects uploaded yet.</motion.p>}
        </motion.div>
    );
}
"""
with open(os.path.join(base_dir, "HardwareProjects.jsx"), "w", encoding="utf-8") as f:
    f.write(hardware_content)


# SKILLS PAGE
skills_content = """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Skills() {
    const [skills, setSkills] = useState([]);
    useEffect(() => { api.get('/skills').then(res => setSkills(res.data)); }, []);

    const groupedSkills = skills.reduce((acc, skill) => {
        if (!acc[skill.category]) acc[skill.category] = [];
        acc[skill.category].push(skill);
        return acc;
    }, {});

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring' } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-5xl mx-auto px-4 pb-20">
            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-black tracking-tight mb-16 text-center text-slate-800 dark:text-white">Technical <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">Proficiency</span></motion.h2>
            
            <div className="space-y-12">
                {Object.keys(groupedSkills).map((category, idx) => (
                    <motion.div key={category} variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-50px" }} className="glass-card p-8 shadow-xl border border-slate-200/50 dark:border-white/5 rounded-2xl relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-2 h-full bg-gradient-to-b from-emerald-500 to-teal-500"></div>
                        <motion.h3 variants={itemVariants} className="text-2xl font-bold mb-8 text-slate-800 dark:text-white pl-4 border-b border-slate-200 dark:border-slate-800 pb-4">{category}</motion.h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pl-4">
                            {groupedSkills[category].map(s => (
                                <motion.div key={s.id} variants={itemVariants}>
                                    <div className="flex justify-between mb-2">
                                        <span className="font-bold text-slate-700 dark:text-slate-200 tracking-wide">{s.name}</span>
                                        <span className="text-sm font-bold text-emerald-600 dark:text-emerald-400">{s.percentage}%</span>
                                    </div>
                                    <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-3 shadow-inner overflow-hidden">
                                        <motion.div 
                                            initial={{ width: 0 }} 
                                            whileInView={{ width: `${s.percentage}%` }} 
                                            viewport={{ once: true }}
                                            transition={{ duration: 1.5, type: 'spring', bounce: 0.2 }}
                                            className="bg-gradient-to-r from-emerald-500 to-teal-500 h-3 rounded-full relative"
                                        >
                                            <div className="absolute top-0 left-0 w-full h-full bg-white/20"></div>
                                        </motion.div>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                ))}
            </div>
            {skills.length === 0 && <motion.p variants={itemVariants} className="text-center text-slate-500 mt-10 text-xl font-medium">No skills added yet.</motion.p>}
        </motion.div>
    );
}
"""
with open(os.path.join(base_dir, "Skills.jsx"), "w", encoding="utf-8") as f:
    f.write(skills_content)

# CERTIFICATIONS PAGE
cert_content = """import { motion } from 'framer-motion';
import { ExternalLink } from 'lucide-react';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Certifications() {
    const [certs, setCerts] = useState([]);
    useEffect(() => { api.get('/certifications').then(res => setCerts(res.data)); }, []);

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 40, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring', damping: 12 } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4 pb-20">
            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-black tracking-tight mb-16 text-center text-slate-800 dark:text-white">Credentials & <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">Certifications</span></motion.h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {certs.map((c, i) => (
                    <motion.div key={c.id} variants={itemVariants} whileHover={{ y: -8, scale: 1.02 }} className="glass-card p-6 rounded-2xl border border-slate-200/50 dark:border-white/5 shadow-xl hover:shadow-emerald-500/20 transition-all duration-300 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <span className="text-6xl">🎓</span>
                        </div>
                        {c.imagePath && (
                            <div className="h-40 mb-6 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-700 shadow-inner">
                                <img src={`http://localhost:8080${c.imagePath}`} alt={c.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                            </div>
                        )}
                        <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white relative z-10 group-hover:text-emerald-500 transition-colors">{c.title}</h3>
                        <p className="text-emerald-600 dark:text-emerald-400 font-bold text-sm uppercase tracking-wider mb-1 relative z-10">{c.provider}</p>
                        <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-6 relative z-10">{c.date}</p>
                        {c.verificationLink && (
                            <a href={c.verificationLink} target="_blank" rel="noreferrer" className="inline-flex items-center text-sm font-bold text-white bg-slate-900 dark:bg-slate-800 hover:bg-emerald-600 dark:hover:bg-emerald-600 px-4 py-2 rounded-lg transition-colors shadow-md relative z-10 w-full justify-center">
                                Verify Credential <ExternalLink size={16} className="ml-2" />
                            </a>
                        )}
                    </motion.div>
                ))}
            </div>
            {certs.length === 0 && <motion.p variants={itemVariants} className="text-center text-slate-500 mt-10 text-xl font-medium">No certifications uploaded yet.</motion.p>}
        </motion.div>
    );
}
"""
with open(os.path.join(base_dir, "Certifications.jsx"), "w", encoding="utf-8") as f:
    f.write(cert_content)

print("Animations updated across pages.")
