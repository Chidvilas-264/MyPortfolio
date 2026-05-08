import os

base_dir = "C:/Portfolio/frontend/src"

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

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex flex-col items-center justify-center text-center pb-20">
            
            {/* HERO SECTION */}
            <div className="min-h-[70vh] flex flex-col items-center justify-center w-full mb-16">
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 260, damping: 20 }}>
                    {profile.profilePhotoPath ? (
                        <img src={`http://localhost:8080${profile.profilePhotoPath}`} alt="Profile" className="w-48 h-48 md:w-56 md:h-56 rounded-full object-cover border-4 border-emerald-500/30 dark:border-emerald-500/50 shadow-2xl mb-8 ring-4 ring-white dark:ring-slate-900" />
                    ) : (
                        <div className="w-48 h-48 md:w-56 md:h-56 rounded-full bg-slate-200 dark:bg-slate-800 border-4 border-emerald-500/30 dark:border-emerald-500/50 shadow-2xl mb-8 flex items-center justify-center text-slate-400 dark:text-slate-500 ring-4 ring-white dark:ring-slate-900">No Photo</div>
                    )}
                </motion.div>
                
                <motion.h1 initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-5xl md:text-7xl font-extrabold mb-4 tracking-tight text-slate-800 dark:text-white">
                    {profile.fullName || "Your Name"}
                </motion.h1>
                
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }} className="text-xl md:text-2xl text-emerald-600 dark:text-emerald-400 mb-10 font-medium">
                    <span className="typing-text">{profile.title || "Electronics and Communication Engineer"}</span>
                </motion.div>
                
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }} className="flex flex-wrap justify-center gap-4">
                    {profile.resumePath && (
                        <a href={`http://localhost:8080${profile.resumePath}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-lg shadow-emerald-500/30 transition-all hover:-translate-y-1">
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
                    <a href="/contact" className="flex items-center gap-2 px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white rounded-xl shadow-lg shadow-teal-500/30 transition-all hover:-translate-y-1">
                        <Mail size={20} /> Contact Me
                    </a>
                </motion.div>
            </div>

            {/* ABOUT SECTION */}
            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-4xl w-full mx-auto text-left px-4">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight mb-12 text-center text-slate-800 dark:text-white">About <span className="text-teal-600 dark:text-teal-400">Me</span></h2>
                <div className="glass-card p-8 md:p-10 mb-10 border-t-4 border-t-emerald-500 shadow-xl">
                    <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Write something about yourself here in the Admin Dashboard."}</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="glass-card p-8 shadow-lg hover:-translate-y-1 transition-transform">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 text-xl">🎓</span>
                            Education
                        </h3>
                        <ul className="space-y-6">
                            <li className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2.5 before:h-2.5 before:bg-emerald-500 before:rounded-full after:absolute after:left-[4px] after:top-4 after:w-0.5 after:h-full after:bg-slate-200 dark:after:bg-slate-800">
                                <h4 className="font-bold text-slate-800 dark:text-white text-lg">B.Tech in Electronics & Communication</h4>
                                <p className="text-sm font-medium text-emerald-600 dark:text-emerald-400 mt-1">2020 - 2024</p>
                            </li>
                        </ul>
                    </div>
                    <div className="glass-card p-8 shadow-lg hover:-translate-y-1 transition-transform">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-lg bg-teal-100 dark:bg-teal-900/50 flex items-center justify-center text-teal-600 dark:text-teal-400 text-xl">⚡</span>
                            Technical Domains
                        </h3>
                        <div className="flex flex-wrap gap-3">
                            {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map(domain => (
                                <span key={domain} className="px-4 py-2 bg-slate-50 dark:bg-slate-800/80 rounded-lg text-sm font-semibold text-slate-700 dark:text-slate-200 shadow-sm border border-slate-200 dark:border-slate-700/50">{domain}</span>
                            ))}
                        </div>
                    </div>
                </div>
            </motion.div>
        </motion.div>
    );
}
"""

with open(os.path.join(base_dir, "pages", "Home.jsx"), "w", encoding="utf-8") as f:
    f.write(home_content)

# Update App.jsx to remove About route
app_path = os.path.join(base_dir, "App.jsx")
with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()
    
app_content = app_content.replace("import About from './pages/About';\n", "")
app_content = app_content.replace("<Route path=\"/about\" element={<About />} />\n", "")
with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_content)

# Update Navbar.jsx to remove About link
navbar_path = os.path.join(base_dir, "components", "Navbar.jsx")
with open(navbar_path, "r", encoding="utf-8") as f:
    navbar_content = f.read()

# remove { name: 'About', path: '/about' },
navbar_content = navbar_content.replace("{ name: 'About', path: '/about' },\n", "")
with open(navbar_path, "w", encoding="utf-8") as f:
    f.write(navbar_content)

print("Home and About pages successfully merged.")
