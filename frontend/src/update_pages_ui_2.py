import os

base_dir = "C:/Portfolio/frontend/src"

pages_content_2 = {
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
            <div className="text-center mb-12">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-800 dark:text-white mb-4"><span className="text-emerald-600 dark:text-emerald-400">Certifications</span></h2>
                <p className="text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">My professional credentials and continuous learning achievements.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {certs.map((cert, i) => (
                    <motion.div key={cert.id} initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ delay: i * 0.1 }} className="glass-card p-6 flex flex-col items-center text-center group">
                        {cert.imagePath ? (
                            <img src={`http://localhost:8080${cert.imagePath}`} alt={cert.title} className="w-full h-48 object-cover rounded-xl mb-6 group-hover:shadow-lg transition-shadow" />
                        ) : (
                            <div className="w-full h-48 bg-slate-200 dark:bg-slate-800 rounded-xl mb-6 flex items-center justify-center"><span className="text-4xl">📜</span></div>
                        )}
                        <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-2">{cert.title}</h3>
                        <p className="text-emerald-600 dark:text-emerald-400 font-semibold mb-1">{cert.provider}</p>
                        <p className="text-slate-500 dark:text-slate-400 text-sm mb-6">{cert.date}</p>
                        {cert.verificationLink && (
                            <a href={cert.verificationLink} target="_blank" rel="noreferrer" className="mt-auto px-6 py-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 dark:bg-emerald-500/10 dark:text-emerald-300 dark:hover:bg-emerald-500/20 rounded-lg transition-colors font-semibold">Verify Credential</a>
                        )}
                    </motion.div>
                ))}
            </div>
        </motion.div>
    );
}""",
    "pages/Skills.jsx": """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Skills() {
    const [skills, setSkills] = useState([]);
    useEffect(() => {
        api.get('/skills').then(res => setSkills(res.data)).catch(console.error);
    }, []);
    const groupedSkills = skills.reduce((acc, skill) => {
        if(!acc[skill.category]) acc[skill.category] = [];
        acc[skill.category].push(skill);
        return acc;
    }, {});
    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
                <h2 className="text-4xl md:text-5xl font-black tracking-tight text-slate-800 dark:text-white mb-4">Technical <span className="text-blue-600 dark:text-blue-400">Skills</span></h2>
            </div>
            {Object.keys(groupedSkills).map((category, i) => (
                <motion.div key={category} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }} className="mb-10 glass-card p-8 border-l-4 border-l-blue-500">
                    <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white">{category}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                        {groupedSkills[category].map(skill => (
                            <div key={skill.id}>
                                <div className="flex justify-between mb-2">
                                    <span className="font-semibold text-slate-700 dark:text-slate-300">{skill.name}</span>
                                    <span className="text-blue-600 dark:text-blue-400 font-bold">{skill.percentage}%</span>
                                </div>
                                <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-3 overflow-hidden shadow-inner">
                                    <motion.div initial={{ width: 0 }} animate={{ width: `${skill.percentage}%` }} transition={{ duration: 1.5, delay: 0.2, type: 'spring' }} className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full"></motion.div>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            ))}
        </motion.div>
    );
}""",
    "pages/Contact.jsx": """import { motion } from 'framer-motion';
import { useState } from 'react';
import api from '../api/axiosConfig';

export default function Contact() {
    const [formData, setFormData] = useState({ name: '', email: '', content: '' });
    const [status, setStatus] = useState('');
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/messages', formData);
            setStatus('success');
            setFormData({ name: '', email: '', content: '' });
        } catch(err) {
            setStatus('error');
        }
    };
    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-xl mx-auto">
            <div className="text-center mb-10">
                <h2 className="text-4xl font-black text-slate-800 dark:text-white">Let's <span className="text-violet-600 dark:text-violet-400">Connect</span></h2>
                <p className="text-slate-500 dark:text-slate-400 mt-2">Have a project in mind or want to hire me? Send a message!</p>
            </div>
            <div className="glass-card p-8 md:p-10 shadow-2xl shadow-violet-500/10">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Name</label>
                        <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500 transition-shadow" placeholder="John Doe" />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Email</label>
                        <input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500 transition-shadow" placeholder="john@example.com" />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Message</label>
                        <textarea rows="5" value={formData.content} onChange={e => setFormData({...formData, content: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500 transition-shadow resize-none" placeholder="How can I help you?"></textarea>
                    </div>
                    <button type="submit" className="w-full bg-gradient-to-r from-violet-600 to-fuchsia-600 hover:from-violet-500 hover:to-fuchsia-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-violet-500/30 transition-all hover:-translate-y-1">Send Message</button>
                    {status === 'success' && <div className="p-4 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-600 dark:text-emerald-400 rounded-xl text-center font-medium">Message sent successfully! I'll get back to you soon.</div>}
                    {status === 'error' && <div className="p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-600 dark:text-red-400 rounded-xl text-center font-medium">Failed to send message. Please try again.</div>}
                </form>
            </div>
        </motion.div>
    );
}""",
    "pages/ProjectDetails.jsx": """import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ExternalLink, Github } from 'lucide-react';
import api from '../api/axiosConfig';

export default function ProjectDetails() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [selectedImg, setSelectedImg] = useState(null);

    useEffect(() => {
        api.get(`/projects/${id}`).then(res => setProject(res.data)).catch(console.error);
    }, [id]);

    if(!project) return <div className="text-center py-20 text-slate-500 dark:text-slate-400">Loading project details...</div>;

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-5xl mx-auto">
            <Link to={project.category === 'Hardware' ? '/hardware' : '/software'} className="inline-flex items-center text-slate-500 hover:text-violet-600 dark:text-slate-400 dark:hover:text-violet-400 mb-8 font-medium transition-colors">
                <ArrowLeft size={16} className="mr-2" /> Back to {project.category} Projects
            </Link>
            
            <div className="glass-card p-8 md:p-12 mb-12">
                <h1 className="text-4xl md:text-5xl font-black text-slate-800 dark:text-white mb-6">{project.title}</h1>
                <div className="flex flex-wrap gap-4 mb-8">
                    {project.githubLink && (
                        <a href={project.githubLink} className="inline-flex items-center px-4 py-2 bg-slate-900 text-white dark:bg-slate-800 rounded-lg hover:bg-slate-800 dark:hover:bg-slate-700 transition-colors" target="_blank" rel="noreferrer">
                            <Github size={18} className="mr-2" /> View Source
                        </a>
                    )}
                    {project.demoLink && (
                        <a href={project.demoLink} className="inline-flex items-center px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors shadow-lg shadow-violet-500/30" target="_blank" rel="noreferrer">
                            <ExternalLink size={18} className="mr-2" /> Live Demo
                        </a>
                    )}
                </div>
                
                <h3 className="text-sm font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-3">About the Project</h3>
                <p className="text-slate-700 dark:text-slate-300 text-lg leading-relaxed whitespace-pre-wrap mb-10">{project.description}</p>
                
                <h3 className="text-sm font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-4">Technologies Used</h3>
                <div className="flex flex-wrap gap-3">
                    {project.techStack?.split(',').map(t => (
                        <span key={t} className="px-4 py-2 bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 font-medium shadow-sm">{t.trim()}</span>
                    ))}
                </div>
            </div>

            {project.images && project.images.length > 0 && (
                <div className="mb-12">
                    <h3 className="text-2xl font-bold text-slate-800 dark:text-white mb-6">Image Gallery</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {project.images.map(img => (
                            <div key={img.id} className="group relative overflow-hidden rounded-2xl glass-card cursor-pointer aspect-video" onClick={() => setSelectedImg(`http://localhost:8080${img.filePath}`)}>
                                <img src={`http://localhost:8080${img.filePath}`} alt="Gallery" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {selectedImg && (
                <div className="fixed inset-0 bg-slate-900/95 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setSelectedImg(null)}>
                    <button className="absolute top-6 right-6 text-white bg-white/10 hover:bg-white/20 p-2 rounded-full backdrop-blur-md transition-colors"><X size={24} /></button>
                    <img src={selectedImg} alt="Fullscreen" className="max-w-full max-h-full object-contain rounded-lg shadow-2xl" />
                </div>
            )}
        </motion.div>
    );
}"""
}

for path, content in pages_content_2.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Pages UI part 2 updated successfully.")
