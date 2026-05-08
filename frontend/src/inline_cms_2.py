import os

base_dir = "C:/Portfolio/frontend/src/pages"

# --- HARDWARE PROJECTS ---
hw_content = """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Edit2, Trash2, X, Image as ImageIcon } from 'lucide-react';
import api from '../api/axiosConfig';

export default function HardwareProjects() {
    const [projects, setProjects] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const isAdmin = !!localStorage.getItem('token');
    
    const [form, setForm] = useState({ id: null, title: '', description: '', category: 'Hardware', githubLink: '', demoLink: '', techStack: '' });
    const [imageFile, setImageFile] = useState(null);

    const fetchProjects = () => api.get('/projects/category/Hardware').then(res => setProjects(res.data));
    useEffect(() => { fetchProjects(); }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        const res = await api.post('/projects', form);
        if(imageFile && res.data.id) {
            const formData = new FormData();
            formData.append('file', imageFile);
            formData.append('category', 'projects');
            await api.post(`/projects/${res.data.id}/images`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        }
        fetchProjects();
        setShowModal(false);
        setForm({ id: null, title: '', description: '', category: 'Hardware', githubLink: '', demoLink: '', techStack: '' });
        setImageFile(null);
    };

    const editProject = (p) => {
        setForm({ id: p.id, title: p.title, description: p.description, category: 'Hardware', githubLink: p.githubLink || '', demoLink: p.demoLink || '', techStack: p.techStack || '' });
        setShowModal(true);
    };

    const deleteProject = async (id) => {
        if(window.confirm('Delete this project?')) {
            await api.delete(`/projects/${id}`);
            fetchProjects();
        }
    };

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 50, opacity: 0, scale: 0.95 }, visible: { y: 0, opacity: 1, scale: 1, transition: { type: 'spring', stiffness: 100 } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4 relative pb-20">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, title: '', description: '', category: 'Hardware', githubLink: '', demoLink: '', techStack: '' }); setImageFile(null); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{form.id ? 'Edit Project' : 'Add Hardware Project'}</h3>
                            <button onClick={() => setShowModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSave} className="space-y-4">
                            <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <textarea placeholder="Description" value={form.description} onChange={e=>setForm({...form, description: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="3" required/>
                            <input placeholder="Tech Stack (comma separated)" value={form.techStack} onChange={e=>setForm({...form, techStack: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            <div className="grid grid-cols-2 gap-4">
                                <input placeholder="GitHub URL" value={form.githubLink} onChange={e=>setForm({...form, githubLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                <input placeholder="Live Demo URL" value={form.demoLink} onChange={e=>setForm({...form, demoLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            </div>
                            <div className="p-4 border border-dashed border-stone-300 dark:border-stone-700 rounded-sm">
                                <label className="flex items-center gap-2 text-sm font-bold mb-2"><ImageIcon size={16}/> Cover Image</label>
                                <input type="file" accept="image/*" onChange={e => setImageFile(e.target.files[0])} className="w-full" />
                            </div>
                            <div className="flex justify-end gap-4 mt-6">
                                <button type="submit" className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 w-full tracking-widest uppercase text-xs">Save Project</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-center text-slate-800 dark:text-white">Hardware <span className="italic text-stone-500 dark:text-stone-400 font-normal">Engineering</span></motion.h2>
            <motion.p variants={itemVariants} className="text-center text-slate-500 dark:text-slate-400 mb-12 text-lg">Circuit design, FPGA implementations, and embedded systems.</motion.p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map(p => (
                    <motion.div key={p.id} variants={itemVariants} whileHover={{ y: -5 }} className="glass-card rounded-sm overflow-hidden border border-slate-200/50 dark:border-white/5 shadow-sm hover:shadow-md transition-all duration-300 group flex flex-col h-full relative">
                        {isAdmin && (
                            <div className="absolute top-2 right-2 z-20 flex gap-2">
                                <button onClick={() => editProject(p)} className="p-2 bg-white/90 dark:bg-black/90 text-stone-800 dark:text-stone-200 rounded-sm shadow hover:bg-stone-200"><Edit2 size={16}/></button>
                                <button onClick={() => deleteProject(p.id)} className="p-2 bg-white/90 dark:bg-black/90 text-red-600 rounded-sm shadow hover:bg-red-50"><Trash2 size={16}/></button>
                            </div>
                        )}
                        <div className="h-48 overflow-hidden bg-slate-200 dark:bg-slate-800 relative">
                            {p.images && p.images.length > 0 ? (
                                <img src={`http://localhost:8080${p.images[0].filePath}`} alt={p.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-in-out" />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-slate-400 font-medium">No Image</div>
                            )}
                        </div>
                        <div className="p-6 flex-1 flex flex-col">
                            <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white group-hover:text-stone-500 transition-colors">{p.title}</h3>
                            <p className="text-slate-600 dark:text-slate-300 text-sm line-clamp-3 mb-4 flex-1">{p.description}</p>
                            <div className="flex flex-wrap gap-2 mb-4">
                                {p.techStack && p.techStack.split(',').slice(0,3).map(tech => (
                                    <span key={tech} className="text-xs font-bold px-2.5 py-1 bg-stone-100 dark:bg-stone-800 text-stone-800 dark:text-stone-300 rounded-sm border border-stone-200 dark:border-stone-700">{tech.trim()}</span>
                                ))}
                            </div>
                            <Link to={`/project/${p.id}`} className="block text-center w-full py-3 rounded-sm bg-stone-900 dark:bg-stone-800 hover:bg-stone-800 dark:hover:bg-stone-600 text-white font-bold transition-colors shadow-sm tracking-widest uppercase text-xs">Details</Link>
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
    f.write(hw_content)


# --- CERTIFICATIONS ---
cert_content = """import { motion } from 'framer-motion';
import { ExternalLink, Plus, Edit2, Trash2, X, Image as ImageIcon } from 'lucide-react';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Certifications() {
    const [certs, setCerts] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const isAdmin = !!localStorage.getItem('token');

    const [form, setForm] = useState({ id: null, title: '', provider: '', date: '', verificationLink: '' });
    const [file, setFile] = useState(null);

    const fetchCerts = () => api.get('/certifications').then(res => setCerts(res.data));
    useEffect(() => { fetchCerts(); }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('certification', new Blob([JSON.stringify(form)], {type: 'application/json'}));
        if(file) formData.append('file', file);
        await api.post('/certifications', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        fetchCerts();
        setShowModal(false);
        setForm({ id: null, title: '', provider: '', date: '', verificationLink: '' });
        setFile(null);
    };

    const editCert = (c) => {
        setForm({ id: c.id, title: c.title, provider: c.provider, date: c.date, verificationLink: c.verificationLink || '' });
        setShowModal(true);
    };

    const deleteCert = async (id) => {
        if(window.confirm('Delete this certification?')) {
            await api.delete(`/certifications/${id}`);
            fetchCerts();
        }
    };

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 40, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring', damping: 12 } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4 pb-20 relative">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, title: '', provider: '', date: '', verificationLink: '' }); setFile(null); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{form.id ? 'Edit Certification' : 'Add Certification'}</h3>
                            <button onClick={() => setShowModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSave} className="space-y-4">
                            <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <input placeholder="Provider" value={form.provider} onChange={e=>setForm({...form, provider: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <input placeholder="Date (e.g. May 2026)" value={form.date} onChange={e=>setForm({...form, date: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <input placeholder="Verification Link" value={form.verificationLink} onChange={e=>setForm({...form, verificationLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            <div className="p-4 border border-dashed border-stone-300 dark:border-stone-700 rounded-sm">
                                <label className="flex items-center gap-2 text-sm font-bold mb-2"><ImageIcon size={16}/> Certificate Image</label>
                                <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} className="w-full" />
                            </div>
                            <div className="flex justify-end gap-4 mt-6">
                                <button type="submit" className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 w-full tracking-widest uppercase text-xs">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold tracking-tight mb-16 text-center text-slate-800 dark:text-white">Credentials & <span className="italic text-stone-500 dark:text-stone-400 font-normal">Certifications</span></motion.h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {certs.map((c) => (
                    <motion.div key={c.id} variants={itemVariants} whileHover={{ y: -5, scale: 1.01 }} className="glass-card p-6 rounded-sm border border-slate-200/50 dark:border-white/5 shadow-sm hover:shadow-md transition-all duration-300 relative overflow-hidden group">
                        {isAdmin && (
                            <div className="absolute top-2 right-2 z-20 flex gap-2">
                                <button onClick={() => editCert(c)} className="p-2 bg-white/90 dark:bg-black/90 text-stone-800 dark:text-stone-200 rounded-sm shadow hover:bg-stone-200"><Edit2 size={16}/></button>
                                <button onClick={() => deleteCert(c.id)} className="p-2 bg-white/90 dark:bg-black/90 text-red-600 rounded-sm shadow hover:bg-red-50"><Trash2 size={16}/></button>
                            </div>
                        )}
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <span className="text-6xl">🎓</span>
                        </div>
                        {c.imagePath && (
                            <div className="h-40 mb-6 overflow-hidden rounded-sm border border-slate-200 dark:border-slate-700 shadow-inner">
                                <img src={`http://localhost:8080${c.imagePath}`} alt={c.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                            </div>
                        )}
                        <h3 className="text-xl font-bold mb-2 text-slate-800 dark:text-white relative z-10 group-hover:text-stone-500 transition-colors">{c.title}</h3>
                        <p className="text-stone-800 dark:text-stone-300 font-bold text-sm uppercase tracking-wider mb-1 relative z-10">{c.provider}</p>
                        <p className="text-slate-500 dark:text-slate-400 text-sm font-medium mb-6 relative z-10">{c.date}</p>
                        {c.verificationLink && (
                            <a href={c.verificationLink} target="_blank" rel="noreferrer" className="inline-flex items-center text-xs tracking-widest uppercase font-bold text-white bg-stone-900 dark:bg-stone-800 hover:bg-stone-800 dark:hover:bg-stone-600 px-4 py-3 rounded-sm transition-colors shadow-sm relative z-10 w-full justify-center">
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


# --- SKILLS ---
skills_content = """import { motion } from 'framer-motion';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Skills() {
    const [skills, setSkills] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const isAdmin = !!localStorage.getItem('token');

    const [form, setForm] = useState({ id: null, name: '', category: 'Programming Languages', percentage: 50 });

    const fetchSkills = () => api.get('/skills').then(res => setSkills(res.data));
    useEffect(() => { fetchSkills(); }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        await api.post('/skills', form);
        fetchSkills();
        setShowModal(false);
        setForm({ id: null, name: '', category: 'Programming Languages', percentage: 50 });
    };

    const editSkill = (s) => {
        setForm({ id: s.id, name: s.name, category: s.category, percentage: s.percentage });
        setShowModal(true);
    };

    const deleteSkill = async (id) => {
        if(window.confirm('Delete this skill?')) {
            await api.delete(`/skills/${id}`);
            fetchSkills();
        }
    };

    const groupedSkills = skills.reduce((acc, skill) => {
        if (!acc[skill.category]) acc[skill.category] = [];
        acc[skill.category].push(skill);
        return acc;
    }, {});

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring' } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-5xl mx-auto px-4 pb-20 relative">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, name: '', category: 'Programming Languages', percentage: 50 }); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-sm w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{form.id ? 'Edit Skill' : 'Add Skill'}</h3>
                            <button onClick={() => setShowModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSave} className="space-y-4">
                            <input placeholder="Skill Name" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm">
                                <option>Programming Languages</option>
                                <option>Web Development</option>
                                <option>Embedded Systems</option>
                                <option>FPGA Development</option>
                                <option>Engineering Tools</option>
                            </select>
                            <div className="flex items-center gap-4">
                                <span className="font-bold w-12 text-right">{form.percentage}%</span>
                                <input type="range" min="0" max="100" value={form.percentage} onChange={e=>setForm({...form, percentage: e.target.value})} className="w-full accent-stone-800" required/>
                            </div>
                            <div className="flex justify-end gap-4 mt-6">
                                <button type="submit" className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 w-full tracking-widest uppercase text-xs">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold tracking-tight mb-16 text-center text-slate-800 dark:text-white">Technical <span className="italic text-stone-500 dark:text-stone-400 font-normal">Proficiency</span></motion.h2>
            
            <div className="space-y-12">
                {Object.keys(groupedSkills).map((category) => (
                    <motion.div key={category} variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-50px" }} className="glass-card p-8 shadow-sm border border-slate-200/50 dark:border-white/5 rounded-sm relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-2 h-full bg-stone-700 dark:bg-stone-500"></div>
                        <motion.h3 variants={itemVariants} className="text-2xl font-bold mb-8 text-slate-800 dark:text-white pl-4 border-b border-slate-200 dark:border-slate-800 pb-4">{category}</motion.h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pl-4">
                            {groupedSkills[category].map(s => (
                                <motion.div key={s.id} variants={itemVariants} className="relative group">
                                    {isAdmin && (
                                        <div className="absolute -top-1 -right-1 z-20 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button onClick={() => editSkill(s)} className="p-1 bg-white/90 dark:bg-black/90 text-stone-800 rounded-sm shadow hover:bg-stone-200"><Edit2 size={12}/></button>
                                            <button onClick={() => deleteSkill(s.id)} className="p-1 bg-white/90 dark:bg-black/90 text-red-600 rounded-sm shadow hover:bg-red-50"><Trash2 size={12}/></button>
                                        </div>
                                    )}
                                    <div className="flex justify-between mb-2">
                                        <span className="font-bold text-slate-700 dark:text-slate-200 tracking-wide">{s.name}</span>
                                        <span className="text-sm font-bold text-stone-800 dark:text-stone-300">{s.percentage}%</span>
                                    </div>
                                    <div className="w-full bg-stone-200 dark:bg-stone-800 h-2 shadow-inner overflow-hidden rounded-sm">
                                        <motion.div 
                                            initial={{ width: 0 }} 
                                            whileInView={{ width: `${s.percentage}%` }} 
                                            viewport={{ once: true }}
                                            transition={{ duration: 1.5, type: 'spring', bounce: 0.2 }}
                                            className="bg-stone-700 dark:bg-stone-400 h-2 relative"
                                        />
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

print("Inline CMS fully implemented")
