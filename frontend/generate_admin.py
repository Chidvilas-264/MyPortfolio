import os

base_dir = "C:/Portfolio/frontend/src"

admin = {
    "pages/AdminDashboard.jsx": """import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function AdminDashboard() {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('projects');

    useEffect(() => {
        if(!localStorage.getItem('token')) navigate('/admin/login');
    }, [navigate]);

    return (
        <div className="flex gap-6 h-[80vh]">
            <div className="w-64 glass-card p-4 flex flex-col gap-2">
                <button onClick={() => setActiveTab('projects')} className={`p-3 rounded text-left ${activeTab === 'projects' ? 'bg-blue-600' : 'hover:bg-white/10'}`}>Projects</button>
                <button onClick={() => setActiveTab('certifications')} className={`p-3 rounded text-left ${activeTab === 'certifications' ? 'bg-blue-600' : 'hover:bg-white/10'}`}>Certifications</button>
                <button onClick={() => setActiveTab('skills')} className={`p-3 rounded text-left ${activeTab === 'skills' ? 'bg-blue-600' : 'hover:bg-white/10'}`}>Skills</button>
                <button onClick={() => setActiveTab('profile')} className={`p-3 rounded text-left ${activeTab === 'profile' ? 'bg-blue-600' : 'hover:bg-white/10'}`}>Profile & Resume</button>
                <button onClick={() => setActiveTab('messages')} className={`p-3 rounded text-left ${activeTab === 'messages' ? 'bg-blue-600' : 'hover:bg-white/10'}`}>Messages</button>
                <button onClick={() => { localStorage.removeItem('token'); navigate('/admin/login'); }} className="p-3 rounded text-left text-red-400 hover:bg-red-900/30 mt-auto">Logout</button>
            </div>
            <div className="flex-1 glass-card p-6 overflow-y-auto">
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

    const fetchProjects = () => api.get('/projects').then(res => setProjects(res.data));
    useEffect(() => { fetchProjects(); }, []);

    const createProject = async (e) => {
        e.preventDefault();
        await api.post('/projects', form);
        fetchProjects();
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
        alert('Image uploaded successfully!');
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-4">Add Project</h3>
            <form onSubmit={createProject} className="space-y-4 mb-8 p-4 border border-gray-700 rounded">
                <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <textarea placeholder="Description" value={form.description} onChange={e=>setForm({...form, description: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full p-2 bg-gray-800 rounded">
                    <option>Software</option>
                    <option>Hardware</option>
                </select>
                <input placeholder="Tech Stack (comma separated)" value={form.techStack} onChange={e=>setForm({...form, techStack: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
                <input placeholder="GitHub Link" value={form.githubLink} onChange={e=>setForm({...form, githubLink: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
                <button type="submit" className="bg-blue-600 px-4 py-2 rounded">Add Project</button>
            </form>

            <h3 className="text-2xl font-bold mb-4">Upload Project Images</h3>
            <div className="mb-8 p-4 border border-gray-700 rounded space-y-4">
                <select value={selectedProject || ''} onChange={e=>setSelectedProject(e.target.value)} className="w-full p-2 bg-gray-800 rounded">
                    <option value="">Select a Project...</option>
                    {projects.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
                <select value={imageCategory} onChange={e=>setImageCategory(e.target.value)} className="w-full p-2 bg-gray-800 rounded">
                    <option value="projects">General Project Image</option>
                    <option value="simulations">Simulation Screenshot</option>
                    <option value="architecture">Architecture Diagram</option>
                </select>
                <input type="file" accept="image/*" onChange={handleFileChange} className="w-full p-2" />
                {imagePreview && (
                    <div className="mt-2">
                        <p>Preview:</p>
                        <img src={imagePreview} alt="Preview" className="w-48 h-auto rounded border" />
                        <button onClick={() => {setImageFile(null); setImagePreview(null);}} className="text-red-400 text-sm mt-1">Remove before upload</button>
                    </div>
                )}
                <button onClick={uploadImage} disabled={!imageFile || !selectedProject} className="bg-emerald-600 px-4 py-2 rounded disabled:opacity-50">Upload Image</button>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Manage Projects</h3>
            <ul className="space-y-2">
                {projects.map(p => (
                    <li key={p.id} className="p-4 bg-white/5 rounded flex justify-between items-center">
                        <span>{p.title} - {p.images?.length || 0} images</span>
                        <button onClick={() => { api.delete(`/projects/${p.id}`).then(fetchProjects); }} className="text-red-400">Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

function CertificationManager() {
    const [certs, setCerts] = useState([]);
    const [form, setForm] = useState({ title: '', provider: '', date: '', verificationLink: '' });
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);

    const fetchCerts = () => api.get('/certifications').then(res => setCerts(res.data));
    useEffect(() => { fetchCerts(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('certification', new Blob([JSON.stringify(form)], {type: 'application/json'}));
        if(file) formData.append('file', file);
        await api.post('/certifications', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        fetchCerts();
        setForm({ title: '', provider: '', date: '', verificationLink: '' });
        setFile(null); setPreview(null);
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-4">Add Certification</h3>
            <form onSubmit={handleSubmit} className="space-y-4 mb-8">
                <input placeholder="Title" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <input placeholder="Provider" value={form.provider} onChange={e=>setForm({...form, provider: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <input placeholder="Date" value={form.date} onChange={e=>setForm({...form, date: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <input type="file" accept="image/*" onChange={e => {
                    const f = e.target.files[0];
                    setFile(f);
                    setPreview(URL.createObjectURL(f));
                }} className="w-full p-2" />
                {preview && <img src={preview} className="w-48 h-auto rounded" />}
                <button type="submit" className="bg-emerald-600 px-4 py-2 rounded">Upload & Save</button>
            </form>
            <ul>
                {certs.map(c => <li key={c.id} className="p-2 border-b border-gray-700">{c.title} <button onClick={() => api.delete(`/certifications/${c.id}`).then(fetchCerts)} className="text-red-400 ml-4">Delete</button></li>)}
            </ul>
        </div>
    );
}

function SkillManager() {
    const [skills, setSkills] = useState([]);
    const [form, setForm] = useState({ name: '', category: 'Programming Languages', percentage: 50 });
    const fetchSkills = () => api.get('/skills').then(res => setSkills(res.data));
    useEffect(() => { fetchSkills(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        await api.post('/skills', form);
        fetchSkills();
    };

    return (
        <div>
            <h3 className="text-2xl font-bold mb-4">Manage Skills</h3>
            <form onSubmit={handleSubmit} className="space-y-4 mb-8">
                <input placeholder="Skill Name" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full p-2 bg-gray-800 rounded">
                    <option>Programming Languages</option>
                    <option>Web Development</option>
                    <option>Embedded Systems</option>
                    <option>FPGA Development</option>
                    <option>Engineering Tools</option>
                </select>
                <input type="number" min="0" max="100" value={form.percentage} onChange={e=>setForm({...form, percentage: e.target.value})} className="w-full p-2 bg-gray-800 rounded" required/>
                <button type="submit" className="bg-purple-600 px-4 py-2 rounded">Add Skill</button>
            </form>
            <ul>{skills.map(s => <li key={s.id} className="p-2 border-b border-gray-700">{s.name} ({s.percentage}%) <button onClick={()=>api.delete(`/skills/${s.id}`).then(fetchSkills)} className="text-red-400 ml-4">Delete</button></li>)}</ul>
        </div>
    );
}

function ProfileManager() {
    const [profile, setProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '' });
    const [photo, setPhoto] = useState(null);
    const [resume, setResume] = useState(null);

    useEffect(() => { api.get('/profile').then(res => setProfile(res.data || profile)); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('profile', new Blob([JSON.stringify(profile)], {type: 'application/json'}));
        if(photo) formData.append('photo', photo);
        if(resume) formData.append('resume', resume);
        await api.post('/profile', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        alert('Profile updated');
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <h3 className="text-2xl font-bold mb-4">Update Profile & Resume</h3>
            <input placeholder="Full Name" value={profile.fullName || ''} onChange={e=>setProfile({...profile, fullName: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
            <input placeholder="Title" value={profile.title || ''} onChange={e=>setProfile({...profile, title: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
            <textarea placeholder="Bio" value={profile.bio || ''} onChange={e=>setProfile({...profile, bio: e.target.value})} className="w-full p-2 bg-gray-800 rounded" rows="4" />
            <input placeholder="GitHub Link" value={profile.githubLink || ''} onChange={e=>setProfile({...profile, githubLink: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
            <input placeholder="LinkedIn Link" value={profile.linkedinLink || ''} onChange={e=>setProfile({...profile, linkedinLink: e.target.value})} className="w-full p-2 bg-gray-800 rounded" />
            <div>
                <label className="block mb-1">Profile Photo</label>
                <input type="file" accept="image/*" onChange={e => setPhoto(e.target.files[0])} className="w-full p-2" />
            </div>
            <div>
                <label className="block mb-1">Resume (PDF)</label>
                <input type="file" accept=".pdf" onChange={e => setResume(e.target.files[0])} className="w-full p-2" />
            </div>
            <button type="submit" className="bg-blue-600 px-4 py-2 rounded">Save Profile</button>
        </form>
    );
}

function MessageManager() {
    const [messages, setMessages] = useState([]);
    const fetchMsgs = () => api.get('/messages').then(res => setMessages(res.data));
    useEffect(() => { fetchMsgs(); }, []);
    return (
        <div>
            <h3 className="text-2xl font-bold mb-4">Messages</h3>
            <div className="space-y-4">
                {messages.map(m => (
                    <div key={m.id} className="p-4 bg-white/5 rounded border border-gray-700">
                        <div className="flex justify-between mb-2">
                            <span className="font-bold">{m.name} ({m.email})</span>
                            <button onClick={() => api.delete(`/messages/${m.id}`).then(fetchMsgs)} className="text-red-400">Delete</button>
                        </div>
                        <p className="text-gray-300">{m.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
"""
}

for path, content in admin.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Admin dashboard generated successfully.")
