import os

base_dir = "C:/Portfolio/frontend/src/pages"

# --- HOME.JSX ---
home_content = """import { motion } from 'framer-motion';
import { Download, Mail, Edit3, X } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import { useEffect, useState } from 'react';
import api from '../api/axiosConfig';

export default function Home() {
    const [profile, setProfile] = useState({});
    const [showEdit, setShowEdit] = useState(false);
    const isAdmin = !!localStorage.getItem('token');
    
    // Form state
    const [formProfile, setFormProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '', email: '' });
    const [photo, setPhoto] = useState(null);
    const [resume, setResume] = useState(null);

    const loadProfile = () => {
        api.get('/profile').then(res => {
            setProfile(res.data);
            if(res.data) setFormProfile(res.data);
        }).catch(console.error);
    };

    useEffect(() => { loadProfile(); }, []);

    const handleSaveProfile = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('profile', new Blob([JSON.stringify(formProfile)], {type: 'application/json'}));
        if(photo) formData.append('photo', photo);
        if(resume) formData.append('resume', resume);
        await api.post('/profile', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        setShowEdit(false);
        loadProfile();
    };

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.2, delayChildren: 0.1 } } };
    const itemVariants = { hidden: { y: 40, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 100, damping: 15 } } };

    return (
        <div className="flex flex-col items-center justify-center text-center pb-20 overflow-hidden relative">
            
            {isAdmin && (
                <button onClick={() => setShowEdit(!showEdit)} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    {showEdit ? <X size={24}/> : <Edit3 size={24}/>}
                </button>
            )}

            {showEdit && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 flex items-center justify-center p-4 overflow-y-auto">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-2xl w-full mt-20">
                        <h3 className="text-2xl font-bold mb-6 text-stone-900 dark:text-white border-b pb-2">Edit Profile</h3>
                        <form onSubmit={handleSaveProfile} className="space-y-4 text-left">
                            <input placeholder="Full Name" value={formProfile.fullName || ''} onChange={e=>setFormProfile({...formProfile, fullName: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            <input placeholder="Title" value={formProfile.title || ''} onChange={e=>setFormProfile({...formProfile, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            <textarea placeholder="Bio" value={formProfile.bio || ''} onChange={e=>setFormProfile({...formProfile, bio: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="5" />
                            <div className="grid grid-cols-2 gap-4">
                                <input placeholder="GitHub URL" value={formProfile.githubLink || ''} onChange={e=>setFormProfile({...formProfile, githubLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                <input placeholder="LinkedIn URL" value={formProfile.linkedinLink || ''} onChange={e=>setFormProfile({...formProfile, linkedinLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            </div>
                            <input type="email" placeholder="Email" value={formProfile.email || ''} onChange={e=>setFormProfile({...formProfile, email: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            <div className="p-4 border border-dashed border-stone-300 dark:border-stone-700 rounded-sm">
                                <label className="block text-sm font-bold mb-2">Profile Photo</label>
                                <input type="file" accept="image/*" onChange={e => setPhoto(e.target.files[0])} className="w-full mb-4" />
                                <label className="block text-sm font-bold mb-2">Resume (PDF)</label>
                                <input type="file" accept=".pdf" onChange={e => setResume(e.target.files[0])} className="w-full" />
                            </div>
                            <div className="flex justify-end gap-4 mt-6">
                                <button type="button" onClick={()=>setShowEdit(false)} className="px-6 py-2 font-bold text-stone-500 hover:text-stone-700">Cancel</button>
                                <button type="submit" className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* HERO SECTION */}
            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="min-h-[80vh] flex flex-col items-center justify-center w-full mb-16 pt-10">
                <motion.div variants={itemVariants} className="relative group w-full flex justify-center">
                    {profile.profilePhotoPath ? (
                        <div className="relative w-64 md:w-80 h-[350px] md:h-[400px] mb-8 overflow-hidden" style={{ WebkitMaskImage: 'linear-gradient(to bottom, black 50%, transparent 100%)', maskImage: 'linear-gradient(to bottom, black 50%, transparent 100%)' }}>
                            <img src={`http://localhost:8080${profile.profilePhotoPath}`} alt="Profile" className="w-full h-full object-cover object-top filter grayscale-[10%] contrast-[1.1]" />
                        </div>
                    ) : (
                        <div className="relative w-48 h-48 md:w-56 md:h-56 rounded-full bg-slate-200 dark:bg-slate-800 shadow-2xl mb-8 flex items-center justify-center text-slate-400">No Photo</div>
                    )}
                </motion.div>
                
                <motion.h1 variants={itemVariants} className="text-5xl md:text-7xl font-bold mb-4 tracking-tight text-slate-800 dark:text-white ">
                    {profile.fullName || "Your Name"}
                </motion.h1>
                
                <motion.div variants={itemVariants} className="text-xl md:text-2xl text-stone-600 dark:text-stone-400 italic mb-10 font-bold tracking-wide">
                    {profile.title || "Electronics and Communication Engineer"}
                </motion.div>
                
                <motion.div variants={itemVariants} className="flex flex-wrap justify-center gap-4">
                    {profile.resumePath && (
                        <a href={`http://localhost:8080${profile.resumePath}`} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-8 py-3 uppercase tracking-widest text-xs border border-transparent bg-stone-900 hover:bg-stone-800 text-white dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-stone-300 rounded-sm transition-all hover:-translate-y-1">
                            <Download size={20} /> Download Resume
                        </a>
                    )}
                    {profile.githubLink && (
                        <a href={profile.githubLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-8 py-3 uppercase tracking-widest text-xs border border-transparent bg-slate-900 hover:bg-slate-800 dark:bg-slate-800 dark:hover:bg-slate-700 text-white rounded-sm shadow-sm transition-all hover:-translate-y-1">
                            <FaGithub size={20} /> GitHub
                        </a>
                    )}
                    {profile.linkedinLink && (
                        <a href={profile.linkedinLink} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-8 py-3 uppercase tracking-widest text-xs border border-transparent bg-[#0A66C2] hover:bg-[#004182] text-white rounded-sm shadow-sm transition-all hover:-translate-y-1">
                            <FaLinkedin size={20} /> LinkedIn
                        </a>
                    )}
                    <button onClick={() => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})} className="flex items-center gap-2 px-8 py-3 uppercase tracking-widest text-xs border border-transparent bg-stone-900 hover:bg-stone-800 text-white dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-stone-300 rounded-sm transition-all hover:-translate-y-1">
                        <Mail size={20} /> Contact Me
                    </button>
                </motion.div>
            </motion.div>

            {/* ABOUT SECTION */}
            <motion.div variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }} className="max-w-4xl w-full mx-auto text-left px-4">
                <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold tracking-tight mb-12 text-center text-slate-800 dark:text-white">About <span className="italic text-stone-500 dark:text-stone-400 font-normal">Me</span></motion.h2>
                
                <motion.div variants={itemVariants} className="glass-card p-8 md:p-10 mb-10 border-t-4 border-t-stone-700 shadow-xl">
                    <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Click the edit button in the bottom right to add your bio."}</p>
                </motion.div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-sm bg-stone-100 dark:bg-stone-900 flex items-center justify-center text-stone-800 dark:text-stone-300 text-xl shadow-inner">🎓</span>
                            Education
                        </h3>
                        <ul className="space-y-6">
                            <li className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2.5 before:h-2.5 before:bg-stone-700 before:rounded-full after:absolute after:left-[4px] after:top-4 after:w-0.5 after:h-full after:bg-gradient-to-b after:from-stone-700 after:to-transparent">
                                <h4 className="font-bold text-slate-800 dark:text-white text-lg">B.Tech in Electronics & Communication</h4>
                                <p className="text-sm font-bold text-stone-800 dark:text-stone-300 mt-1 uppercase tracking-wider">2020 - 2024</p>
                            </li>
                        </ul>
                    </motion.div>
                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-sm bg-stone-100 dark:bg-stone-900 flex items-center justify-center text-stone-800 dark:text-stone-300 text-xl shadow-inner">⚡</span>
                            Technical Domains
                        </h3>
                        <div className="flex flex-wrap gap-3">
                            {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map((domain) => (
                                <span key={domain} className="px-4 py-2 bg-white dark:bg-slate-800/80 rounded-sm text-sm font-bold text-slate-700 dark:text-slate-200 shadow-sm border border-slate-100 dark:border-slate-700/50">{domain}</span>
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

# --- SOFTWARE PROJECTS ---
sw_content = """import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Edit2, Trash2, X, Image as ImageIcon } from 'lucide-react';
import api from '../api/axiosConfig';

export default function SoftwareProjects() {
    const [projects, setProjects] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const isAdmin = !!localStorage.getItem('token');
    
    const [form, setForm] = useState({ id: null, title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' });
    const [imageFile, setImageFile] = useState(null);

    const fetchProjects = () => api.get('/projects/category/Software').then(res => setProjects(res.data));
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
        setForm({ id: null, title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' });
        setImageFile(null);
    };

    const editProject = (p) => {
        setForm({ id: p.id, title: p.title, description: p.description, category: 'Software', githubLink: p.githubLink || '', demoLink: p.demoLink || '', techStack: p.techStack || '' });
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
                <button onClick={() => {setForm({ id: null, title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' }); setImageFile(null); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{form.id ? 'Edit Project' : 'Add Software Project'}</h3>
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

            <motion.h2 variants={itemVariants} className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-center text-slate-800 dark:text-white">Software <span className="italic text-stone-500 dark:text-stone-400 font-normal">Engineering</span></motion.h2>
            <motion.p variants={itemVariants} className="text-center text-slate-500 dark:text-slate-400 mb-12 text-lg">Full-stack applications, scripts, and algorithms.</motion.p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map((p) => (
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
            {projects.length === 0 && <motion.p variants={itemVariants} className="text-center text-slate-500 mt-10 text-xl font-medium">No software projects uploaded yet.</motion.p>}
        </motion.div>
    );
}
"""
with open(os.path.join(base_dir, "SoftwareProjects.jsx"), "w", encoding="utf-8") as f:
    f.write(sw_content)

# We can duplicate the logic for HardwareProjects, Skills, and Certifications...
