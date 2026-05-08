import os

base_dir = "C:/Portfolio/frontend/src/pages"

content = """import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function AdminDashboard() {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('projects');

    useEffect(() => {
        if(!localStorage.getItem('token')) navigate('/admin/login');
    }, [navigate]);

    return (
        <div className="flex flex-col md:flex-row gap-6 min-h-[70vh]">
            <div className="w-full md:w-64 glass-card p-4 flex flex-col gap-2 border border-slate-200 dark:border-white/10 shadow-sm">
                <button onClick={() => setActiveTab('projects')} className={`p-3 rounded-lg text-left font-medium transition-colors ${activeTab === 'projects' ? 'bg-emerald-600 text-white shadow-md shadow-emerald-500/20' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'}`}>Projects</button>
                <button onClick={() => setActiveTab('certifications')} className={`p-3 rounded-lg text-left font-medium transition-colors ${activeTab === 'certifications' ? 'bg-emerald-600 text-white shadow-md shadow-emerald-500/20' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'}`}>Certifications</button>
                <button onClick={() => setActiveTab('skills')} className={`p-3 rounded-lg text-left font-medium transition-colors ${activeTab === 'skills' ? 'bg-teal-600 text-white shadow-md shadow-teal-500/20' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'}`}>Skills</button>
                <button onClick={() => setActiveTab('profile')} className={`p-3 rounded-lg text-left font-medium transition-colors ${activeTab === 'profile' ? 'bg-teal-600 text-white shadow-md shadow-teal-500/20' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'}`}>Profile & Resume</button>
                <button onClick={() => setActiveTab('messages')} className={`p-3 rounded-lg text-left font-medium transition-colors ${activeTab === 'messages' ? 'bg-rose-600 text-white shadow-md shadow-rose-500/20' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'}`}>Messages</button>
                <button onClick={() => { localStorage.removeItem('token'); navigate('/admin/login'); }} className="p-3 rounded-lg text-left text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 mt-auto font-bold transition-colors">Logout</button>
            </div>
            <div className="flex-1 glass-card p-6 md:p-8 overflow-y-auto border border-slate-200 dark:border-white/10 shadow-sm">
                {activeTab === 'projects' && <ProjectManager />}
                {activeTab === 'certifications' && <CertificationManager />}
                {activeTab === 'skills' && <SkillManager />}
                {activeTab === 'profile' && <ProfileManager />}
                {activeTab === 'messages' && <MessageManager />}
            </div>
        </div>
    );
}

function ProjectManager() {
    const [projects, setProjects] = useState([]);
    const [form, setForm] = useState({ title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' });
    const [selectedProject, setSelectedProject] = useState(null);
    const [imageFile, setImageFile] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [imageCategory, setImageCategory] = useState('projects');
    const [previewUrl, setPreviewUrl] = useState(null);

    const fetchProjects = () => api.get('/projects').then(res => setProjects(res.data));
    useEffect(() => { fetchProjects(); }, []);

    const createProject = async (e) => {
        e.preventDefault();
        await api.post('/projects', form);
        fetchProjects();
        setPreviewUrl(form.category === 'Hardware' ? '/hardware' : '/software');
        setForm({ title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' });
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if(file) {
            setImageFile(file);
            setImagePreview(URL.createObjectURL(file));
        }
    };

    const uploadImage = async () => {
        if(!imageFile || !selectedProject) return;
        const formData = new FormData();
        formData.append('file', imageFile);
        formData.append('category', imageCategory);
        await api.post(`/projects/${selectedProject}/images`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        setImageFile(null);
        setImagePreview(null);
        fetchProjects();
        setPreviewUrl(`/project/${selectedProject}`);
        alert('Image uploaded successfully!');
    };

    const handleEdit = (p) => {
        setForm({ id: p.id, title: p.title, description: p.description, category: p.category, githubLink: p.githubLink || '', demoLink: p.demoLink || '', techStack: p.techStack || '' });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">{form.id ? 'Edit Project' : 'Add Project'}</h3>
            <form onSubmit={createProject} className="space-y-4 mb-10 p-6 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800">
                <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" required/>
                <textarea placeholder="Description" value={form.description} onChange={e=>setForm({...form, description: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" rows="3" required/>
                <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white">
                    <option>Software</option>
                    <option>Hardware</option>
                </select>
                <input placeholder="Tech Stack (comma separated)" value={form.techStack} onChange={e=>setForm({...form, techStack: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                <input placeholder="GitHub Link" value={form.githubLink} onChange={e=>setForm({...form, githubLink: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                <input placeholder="Live Demo Link" value={form.demoLink} onChange={e=>setForm({...form, demoLink: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                <div className="flex gap-4 items-center">
                    <button type="submit" className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md shadow-emerald-500/20">
                        {form.id ? 'Update Project' : 'Save Project'}
                    </button>
                    {form.id && <button type="button" onClick={() => setForm({ title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '' })} className="text-slate-500 hover:text-slate-700 font-semibold px-4 py-3">Cancel Edit</button>}
                    {previewUrl && <button type="button" onClick={() => window.open(previewUrl, '_blank')} className="bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 dark:hover:bg-slate-600 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">Preview</button>}
                </div>
            </form>

            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">Upload Project Images</h3>
            <div className="mb-10 p-6 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800 space-y-4">
                <select value={selectedProject || ''} onChange={e=>setSelectedProject(e.target.value)} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white">
                    <option value="">Select a Project...</option>
                    {projects.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
                <select value={imageCategory} onChange={e=>setImageCategory(e.target.value)} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white">
                    <option value="projects">General Project Image</option>
                    <option value="simulations">Simulation Screenshot</option>
                    <option value="architecture">Architecture Diagram</option>
                </select>
                <input type="file" accept="image/*" onChange={handleFileChange} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                {imagePreview && (
                    <div className="mt-4 p-4 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
                        <p className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">Preview:</p>
                        <img src={imagePreview} alt="Preview" className="w-full max-w-sm h-auto rounded shadow-sm mb-3" />
                        <button onClick={() => {setImageFile(null); setImagePreview(null);}} className="text-rose-500 hover:text-rose-600 text-sm font-semibold transition-colors">Cancel Selection</button>
                    </div>
                )}
                <div className="flex gap-4">
                    <button onClick={uploadImage} disabled={!imageFile || !selectedProject} className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-6 py-3 rounded-lg disabled:opacity-50 transition-colors shadow-md shadow-emerald-500/20">Upload Image</button>
                    {previewUrl && <button type="button" onClick={() => window.open(previewUrl, '_blank')} className="bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">Preview</button>}
                </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">Manage Projects</h3>
            <div className="space-y-3">
                {projects.map(p => (
                    <div key={p.id} className="p-4 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 flex justify-between items-center shadow-sm">
                        <span className="font-medium text-slate-700 dark:text-slate-200">{p.title} <span className="text-slate-400 font-normal ml-2">({p.images?.length || 0} images)</span></span>
                        <div>
                            <button onClick={() => handleEdit(p)} className="text-teal-600 hover:text-teal-700 font-semibold px-3 py-1 bg-teal-50 dark:bg-teal-500/10 rounded transition-colors mr-2">Edit</button>
                            <button onClick={() => { if(window.confirm('Delete project?')) api.delete(`/projects/${p.id}`).then(fetchProjects); }} className="text-rose-500 hover:text-rose-600 font-semibold px-3 py-1 bg-rose-50 dark:bg-rose-500/10 rounded transition-colors">Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

function CertificationManager() {
    const [certs, setCerts] = useState([]);
    const [form, setForm] = useState({ title: '', provider: '', date: '', verificationLink: '' });
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);

    const fetchCerts = () => api.get('/certifications').then(res => setCerts(res.data));
    useEffect(() => { fetchCerts(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('certification', new Blob([JSON.stringify(form)], {type: 'application/json'}));
        if(file) formData.append('file', file);
        await api.post('/certifications', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        fetchCerts();
        setPreviewUrl('/certifications');
        setForm({ title: '', provider: '', date: '', verificationLink: '' });
        setFile(null); setPreview(null);
    };

    const handleEdit = (c) => {
        setForm({ id: c.id, title: c.title, provider: c.provider, date: c.date, verificationLink: c.verificationLink || '', imagePath: c.imagePath });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">{form.id ? 'Edit Certification' : 'Add Certification'}</h3>
            <form onSubmit={handleSubmit} className="space-y-4 mb-10 p-6 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800">
                <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" required/>
                <input placeholder="Provider" value={form.provider} onChange={e=>setForm({...form, provider: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" required/>
                <input placeholder="Date (e.g. May 2026)" value={form.date} onChange={e=>setForm({...form, date: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" required/>
                <input placeholder="Verification Link" value={form.verificationLink} onChange={e=>setForm({...form, verificationLink: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                <input type="file" accept="image/*" onChange={e => {
                    const f = e.target.files[0];
                    if(f) {
                        setFile(f);
                        setPreview(URL.createObjectURL(f));
                    }
                }} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                {preview && <img src={preview} className="w-48 h-auto rounded shadow mt-2" />}
                <div className="flex gap-4 items-center">
                    <button type="submit" className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md shadow-emerald-500/20">
                        {form.id ? 'Update Certification' : 'Save Certification'}
                    </button>
                    {form.id && <button type="button" onClick={() => setForm({ title: '', provider: '', date: '', verificationLink: '' })} className="text-slate-500 hover:text-slate-700 font-semibold px-4 py-3">Cancel Edit</button>}
                    {previewUrl && <button type="button" onClick={() => window.open(previewUrl, '_blank')} className="bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">Preview</button>}
                </div>
            </form>
            
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">Manage Certifications</h3>
            <div className="space-y-3">
                {certs.map(c => (
                    <div key={c.id} className="p-4 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 flex justify-between items-center shadow-sm">
                        <span className="font-medium text-slate-700 dark:text-slate-200">{c.title} <span className="text-slate-400 font-normal">({c.provider})</span></span>
                        <div>
                            <button onClick={() => handleEdit(c)} className="text-teal-600 hover:text-teal-700 font-semibold px-3 py-1 bg-teal-50 dark:bg-teal-500/10 rounded transition-colors mr-2">Edit</button>
                            <button onClick={() => api.delete(`/certifications/${c.id}`).then(fetchCerts)} className="text-rose-500 hover:text-rose-600 font-semibold px-3 py-1 bg-rose-50 dark:bg-rose-500/10 rounded transition-colors">Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

function SkillManager() {
    const [skills, setSkills] = useState([]);
    const [form, setForm] = useState({ name: '', category: 'Programming Languages', percentage: 50 });
    const [previewUrl, setPreviewUrl] = useState(null);
    
    const fetchSkills = () => api.get('/skills').then(res => setSkills(res.data));
    useEffect(() => { fetchSkills(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        await api.post('/skills', form);
        fetchSkills();
        setPreviewUrl('/skills');
        setForm({ name: '', category: 'Programming Languages', percentage: 50 });
    };

    const handleEdit = (s) => {
        setForm({ id: s.id, name: s.name, category: s.category, percentage: s.percentage });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">{form.id ? 'Edit Skill' : 'Manage Skills'}</h3>
            <form onSubmit={handleSubmit} className="space-y-4 mb-10 p-6 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-800">
                <input placeholder="Skill Name" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" required/>
                <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full p-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white">
                    <option>Programming Languages</option>
                    <option>Web Development</option>
                    <option>Embedded Systems</option>
                    <option>FPGA Development</option>
                    <option>Engineering Tools</option>
                </select>
                <div className="flex items-center gap-4">
                    <span className="text-slate-700 dark:text-slate-300 font-medium w-16 text-right">{form.percentage}%</span>
                    <input type="range" min="0" max="100" value={form.percentage} onChange={e=>setForm({...form, percentage: e.target.value})} className="w-full accent-teal-600" required/>
                </div>
                <div className="flex gap-4 items-center mt-4">
                    <button type="submit" className="bg-teal-600 hover:bg-teal-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md shadow-teal-500/20">
                        {form.id ? 'Update Skill' : 'Add Skill'}
                    </button>
                    {form.id && <button type="button" onClick={() => setForm({ name: '', category: 'Programming Languages', percentage: 50 })} className="text-slate-500 hover:text-slate-700 font-semibold px-4 py-3">Cancel Edit</button>}
                    {previewUrl && <button type="button" onClick={() => window.open(previewUrl, '_blank')} className="bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">Preview</button>}
                </div>
            </form>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {skills.map(s => (
                    <div key={s.id} className="p-4 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 flex justify-between items-center shadow-sm">
                        <div>
                            <p className="font-semibold text-slate-700 dark:text-slate-200">{s.name}</p>
                            <p className="text-xs text-slate-500 dark:text-slate-400">{s.category} • {s.percentage}%</p>
                        </div>
                        <div>
                            <button onClick={()=>handleEdit(s)} className="text-teal-600 hover:text-teal-700 font-semibold px-3 py-1 bg-teal-50 dark:bg-teal-500/10 rounded transition-colors mr-2">Edit</button>
                            <button onClick={()=>api.delete(`/skills/${s.id}`).then(fetchSkills)} className="text-rose-500 hover:text-rose-600 font-semibold px-3 py-1 bg-rose-50 dark:bg-rose-500/10 rounded transition-colors">Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

function ProfileManager() {
    const [profile, setProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '', email: '' });
    const [photo, setPhoto] = useState(null);
    const [resume, setResume] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);

    useEffect(() => { api.get('/profile').then(res => setProfile(res.data || profile)); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('profile', new Blob([JSON.stringify(profile)], {type: 'application/json'}));
        if(photo) formData.append('photo', photo);
        if(resume) formData.append('resume', resume);
        await api.post('/profile', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        setPreviewUrl('/');
        alert('Profile updated successfully!');
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl">
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">Update Profile & Resume</h3>
            
            <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Full Name</label>
                <input value={profile.fullName || ''} onChange={e=>setProfile({...profile, fullName: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
            </div>
            
            <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Title</label>
                <input value={profile.title || ''} onChange={e=>setProfile({...profile, title: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
            </div>
            
            <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Bio</label>
                <textarea value={profile.bio || ''} onChange={e=>setProfile({...profile, bio: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" rows="5" />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">GitHub URL</label>
                    <input value={profile.githubLink || ''} onChange={e=>setProfile({...profile, githubLink: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                </div>
                <div>
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">LinkedIn URL</label>
                    <input value={profile.linkedinLink || ''} onChange={e=>setProfile({...profile, linkedinLink: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                </div>
                <div className="md:col-span-2">
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Email Address</label>
                    <input type="email" value={profile.email || ''} onChange={e=>setProfile({...profile, email: e.target.value})} className="w-full p-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-800 dark:text-white" />
                </div>
            </div>
            
            <div className="mt-6 p-6 border border-dashed border-slate-300 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-900/30">
                <div className="mb-6">
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Profile Photo</label>
                    <input type="file" accept="image/*" onChange={e => setPhoto(e.target.files[0])} className="w-full" />
                </div>
                <div>
                    <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Resume (PDF)</label>
                    <input type="file" accept=".pdf" onChange={e => setResume(e.target.files[0])} className="w-full" />
                </div>
            </div>
            
            <div className="flex gap-4 mt-6">
                <button type="submit" className="flex-1 md:flex-none bg-teal-600 hover:bg-teal-700 text-white font-semibold px-8 py-3 rounded-lg shadow-md shadow-teal-500/20 transition-colors">Save Profile</button>
                {previewUrl && <button type="button" onClick={() => window.open(previewUrl, '_blank')} className="bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">Preview</button>}
            </div>
        </form>
    );
}

function MessageManager() {
    const [messages, setMessages] = useState([]);
    const fetchMsgs = () => api.get('/messages').then(res => setMessages(res.data));
    useEffect(() => { fetchMsgs(); }, []);
    return (
        <div>
            <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white border-b border-slate-200 dark:border-white/10 pb-2">Messages</h3>
            <div className="space-y-4">
                {messages.length === 0 && <p className="text-slate-500 dark:text-slate-400">No messages yet.</p>}
                {messages.map(m => (
                    <div key={m.id} className="p-6 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm">
                        <div className="flex flex-col md:flex-row justify-between md:items-center mb-4 gap-4">
                            <div>
                                <h4 className="font-bold text-lg text-slate-800 dark:text-white">{m.name}</h4>
                                <a href={`mailto:${m.email}`} className="text-emerald-600 dark:text-emerald-400 text-sm font-medium hover:underline">{m.email}</a>
                            </div>
                            <button onClick={() => api.delete(`/messages/${m.id}`).then(fetchMsgs)} className="self-start text-rose-500 hover:text-rose-600 font-semibold px-4 py-2 bg-rose-50 dark:bg-rose-500/10 rounded-lg transition-colors">Delete</button>
                        </div>
                        <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-lg border border-slate-100 dark:border-slate-700/50">
                            <p className="text-slate-700 dark:text-slate-300 whitespace-pre-wrap">{m.content}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
"""

with open(os.path.join(base_dir, "AdminDashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(content)

print("AdminDashboard UI updated for Preview Button and Edit Option successfully.")
