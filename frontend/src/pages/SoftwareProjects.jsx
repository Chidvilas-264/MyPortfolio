import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Edit2, Trash2, X, Image as ImageIcon } from 'lucide-react';
import { supabase } from '../supabaseClient';

export default function SoftwareProjects() {
    const [projects, setProjects] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);
    
    const [form, setForm] = useState({ id: null, title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '', image_url: '' });
    const [imageFile, setImageFile] = useState(null);

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchProjects = async () => {
        const { data } = await supabase.from('projects').select('*').eq('category', 'Software').order('id', { ascending: false });
        if (data) {
            setProjects(data.map(p => ({
                ...p,
                githubLink: p.github_link,
                demoLink: p.demo_link,
                techStack: p.tech_stack
            })));
        }
    };

    useEffect(() => { 
        checkAdmin();
        fetchProjects(); 
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            let imageUrl = form.image_url;

            if (imageFile) {
                const fileName = `proj_${Date.now()}`;
                const { data } = await supabase.storage.from('project-images').upload(fileName, imageFile);
                if (data) imageUrl = supabase.storage.from('project-images').getPublicUrl(data.path).data.publicUrl;
            }

            const projData = {
                title: form.title,
                description: form.description,
                category: 'Software',
                github_link: form.githubLink,
                demo_link: form.demoLink,
                tech_stack: form.techStack,
                image_url: imageUrl
            };

            if (form.id) {
                await supabase.from('projects').update(projData).eq('id', form.id);
            } else {
                await supabase.from('projects').insert([projData]);
            }
            
            fetchProjects();
            setShowModal(false);
            setForm({ id: null, title: '', description: '', category: 'Software', githubLink: '', demoLink: '', techStack: '', image_url: '' });
            setImageFile(null);
        } catch (err) {
            console.error(err);
        }
    };

    const editProject = (p) => {
        setForm(p);
        setShowModal(true);
    };

    const deleteProject = async (id) => {
        if(window.confirm('Delete this project?')) {
            await supabase.from('projects').delete().eq('id', id);
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
                            {p.image_url ? (
                                <img src={p.image_url} alt={p.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-in-out" />
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
