import os

base_dir = "C:/Portfolio/frontend/src"

pages2 = {
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
            <h2 className="text-4xl font-bold mb-8 text-center text-purple-400">Skills</h2>
            {Object.keys(groupedSkills).map((category, i) => (
                <motion.div key={category} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }} className="mb-8">
                    <h3 className="text-2xl font-semibold mb-4 text-white">{category}</h3>
                    <div className="space-y-4">
                        {groupedSkills[category].map(skill => (
                            <div key={skill.id}>
                                <div className="flex justify-between mb-1">
                                    <span className="text-gray-300">{skill.name}</span>
                                    <span className="text-gray-400">{skill.percentage}%</span>
                                </div>
                                <div className="w-full bg-gray-700 rounded-full h-2.5">
                                    <motion.div initial={{ width: 0 }} animate={{ width: `${skill.percentage}%` }} transition={{ duration: 1, delay: 0.5 }} className="bg-gradient-to-r from-purple-500 to-pink-500 h-2.5 rounded-full"></motion.div>
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
            setStatus('Message sent successfully!');
            setFormData({ name: '', email: '', content: '' });
        } catch(err) {
            setStatus('Failed to send message.');
        }
    };

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-md mx-auto glass-card p-8">
            <h2 className="text-3xl font-bold mb-6 text-center text-white">Contact Me</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block text-gray-300 mb-1">Name</label>
                    <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white focus:outline-none focus:border-blue-500" />
                </div>
                <div>
                    <label className="block text-gray-300 mb-1">Email</label>
                    <input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white focus:outline-none focus:border-blue-500" />
                </div>
                <div>
                    <label className="block text-gray-300 mb-1">Message</label>
                    <textarea rows="4" value={formData.content} onChange={e => setFormData({...formData, content: e.target.value})} required className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white focus:outline-none focus:border-blue-500"></textarea>
                </div>
                <button type="submit" className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-3 rounded hover:opacity-90 transition-opacity">Send Message</button>
                {status && <p className="text-center text-gray-300 mt-4">{status}</p>}
            </form>
        </motion.div>
    );
}""",
    "pages/AdminLogin.jsx": """import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axiosConfig';

export default function AdminLogin() {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/admin/login', credentials);
            if(res.data.status === 'success') {
                localStorage.setItem('token', res.data.token);
                navigate('/admin/dashboard');
            } else {
                setError('Invalid credentials');
            }
        } catch(err) {
            setError('Login failed');
        }
    };

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-center items-center h-[60vh]">
            <div className="glass-card p-8 w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6 text-center text-white">Admin Login</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <input type="text" placeholder="Username" value={credentials.username} onChange={e => setCredentials({...credentials, username: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white" />
                    </div>
                    <div>
                        <input type="password" placeholder="Password" value={credentials.password} onChange={e => setCredentials({...credentials, password: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white" />
                    </div>
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded">Login</button>
                </form>
            </div>
        </motion.div>
    );
}""",
    "pages/ProjectDetails.jsx": """import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../api/axiosConfig';

export default function ProjectDetails() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [selectedImg, setSelectedImg] = useState(null);

    useEffect(() => {
        api.get(`/projects/${id}`).then(res => setProject(res.data)).catch(console.error);
    }, [id]);

    if(!project) return <div className="text-center">Loading...</div>;

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <h1 className="text-4xl font-bold mb-4">{project.title}</h1>
            <div className="flex gap-4 mb-6">
                {project.githubLink && <a href={project.githubLink} className="text-blue-400 hover:underline" target="_blank" rel="noreferrer">GitHub Repo</a>}
                {project.demoLink && <a href={project.demoLink} className="text-emerald-400 hover:underline" target="_blank" rel="noreferrer">Live Demo</a>}
            </div>
            <p className="text-gray-300 text-lg whitespace-pre-wrap mb-8">{project.description}</p>
            <div className="mb-8">
                <h3 className="text-2xl font-semibold mb-4 border-b border-gray-700 pb-2">Tech Stack</h3>
                <div className="flex flex-wrap gap-2">
                    {project.techStack?.split(',').map(t => (
                        <span key={t} className="px-3 py-1 bg-white/10 rounded-full">{t.trim()}</span>
                    ))}
                </div>
            </div>
            <div>
                <h3 className="text-2xl font-semibold mb-4 border-b border-gray-700 pb-2">Image Gallery</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {project.images?.map(img => (
                        <img key={img.id} src={`http://localhost:8080${img.filePath}`} alt="Gallery" className="w-full h-40 object-cover rounded cursor-pointer hover:opacity-80 transition" onClick={() => setSelectedImg(`http://localhost:8080${img.filePath}`)} />
                    ))}
                </div>
            </div>
            {selectedImg && (
                <div className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4" onClick={() => setSelectedImg(null)}>
                    <img src={selectedImg} alt="Fullscreen" className="max-w-full max-h-full object-contain" />
                </div>
            )}
        </motion.div>
    );
}"""
}

for path, content in pages2.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

print("Frontend pages part 2 generated successfully.")
