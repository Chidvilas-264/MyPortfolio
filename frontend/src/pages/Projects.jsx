import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { Link } from 'react-router-dom';
import { Plus, Edit2, Trash2, X, Image as ImageIcon, ExternalLink } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

export default function Projects() {
    const [projects, setProjects] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isAdmin, setIsAdmin] = useState(false);
    
    const [form, setForm] = useState({ id: null, title: '', description: '', githubLink: '', demoLink: '', techStack: '', image_url: '' });
    const [imageFile, setImageFile] = useState(null);

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchProjects = async () => {
        setLoading(true);
        const { data } = await supabase.from('projects').select('*').order('id', { ascending: false });
        if (data) {
            setProjects(data.map(p => ({
                ...p,
                githubLink: p.github_link,
                demoLink: p.demo_link,
                techStack: p.tech_stack
            })));
        }
        setLoading(false);
    };

    useEffect(() => { 
        checkAdmin();
        fetchProjects(); 
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        setLoading(true);
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
            setForm({ id: null, title: '', description: '', githubLink: '', demoLink: '', techStack: '', image_url: '' });
            setImageFile(null);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
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

    const containerVariants = { 
        hidden: { opacity: 0 }, 
        visible: { opacity: 1, transition: { staggerChildren: 0.1 } } 
    };
    const itemVariants = { 
        hidden: { y: 40, opacity: 0 }, 
        visible: { y: 0, opacity: 1, transition: { type: 'spring', damping: 20, stiffness: 100 } } 
    };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto relative">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, title: '', description: '', githubLink: '', demoLink: '', techStack: '' }); setImageFile(null); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{form.id ? 'Edit Project' : 'Add Project'}</h3>
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

            <motion.div variants={itemVariants} className="text-center mb-24">
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-4 text-stone-900 dark:text-white">
                    Portfolio <span className="text-stone-400">Works</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Selected hardware & software implementations</p>
            </motion.div>
            
            {loading ? (
                <div className="flex justify-center py-20">
                    <div className="w-12 h-12 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin"></div>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
                    {projects.map((p) => (
                        <ProjectCard key={p.id} p={p} isAdmin={isAdmin} editProject={editProject} deleteProject={deleteProject} itemVariants={itemVariants} />
                    ))}
                </div>
            )}
            {!loading && projects.length === 0 && <motion.p variants={itemVariants} className="text-center text-stone-500 mt-10 text-xl font-medium">No projects found.</motion.p>}
        </motion.div>
    );
}

function ProjectCard({ p, isAdmin, editProject, deleteProject, itemVariants }) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <motion.div variants={itemVariants} initial="hidden" animate="visible" className="group relative border-b border-stone-200 dark:border-white/10 pb-12">
            {isAdmin && (
                <div className="absolute top-2 right-2 z-20 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => editProject(p)} className="p-2 bg-white/90 dark:bg-black/90 text-stone-800 dark:text-stone-200 rounded-sm shadow hover:scale-110 transition-transform"><Edit2 size={16}/></button>
                    <button onClick={() => deleteProject(p.id)} className="p-2 bg-white/90 dark:bg-black/90 text-red-600 rounded-sm shadow hover:scale-110 transition-transform"><Trash2 size={16}/></button>
                </div>
            )}
            
            <div className="aspect-video overflow-hidden bg-stone-100 dark:bg-stone-900 mb-8 border border-stone-100 dark:border-white/5 relative rounded-sm">
                {p.image_url ? (
                    <img 
                        src={p.image_url} 
                        alt={p.title} 
                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" 
                    />
                ) : (
                    <div className="w-full h-full flex items-center justify-center text-stone-300">No Preview Available</div>
                )}
                <div className="absolute inset-0 bg-stone-900/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
                    {p.githubLink && <a href={p.githubLink} target="_blank" rel="noreferrer" className="p-4 bg-white text-stone-900 rounded-full hover:scale-110 transition-transform"><FaGithub size={20}/></a>}
                    <Link to={`/project/${p.id}`} className="p-4 bg-white text-stone-900 rounded-full hover:scale-110 transition-transform"><ExternalLink size={20}/></Link>
                </div>
            </div>

            <div className="space-y-6">
                <div className="space-y-2">
                    <div className="flex justify-end items-center">
                        <div className="flex gap-3">
                            {(p.techStack?.split(',') || []).slice(0, 3).map(tech => (
                                <span key={tech} className="text-[9px] font-bold uppercase tracking-widest text-stone-500 opacity-60">{tech.trim()}</span>
                            ))}
                        </div>
                    </div>
                    <h3 className="text-4xl font-bold uppercase tracking-tighter text-stone-900 dark:text-white leading-none group-hover:text-stone-500 transition-colors">{p.title}</h3>
                </div>

                <AnimatePresence>
                    {isExpanded && (
                        <motion.div 
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="overflow-hidden"
                        >
                            <p className="text-stone-600 dark:text-stone-400 text-lg leading-relaxed font-light italic mb-6">
                                "{p.description}"
                            </p>
                            <div className="flex flex-wrap gap-4 mb-4">
                                {(p.techStack?.split(',') || []).map(tech => (
                                    <span key={tech} className="px-3 py-1 bg-stone-100 dark:bg-stone-800/50 text-[9px] font-bold uppercase tracking-widest text-stone-500 rounded-full">{tech.trim()}</span>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
                
                <div className="flex justify-between items-center pt-2">
                    <button 
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="group/read flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.4em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-6 transition-all"
                    >
                        {isExpanded ? 'Hide Concept' : 'Project Vision'} 
                        <ExternalLink size={12} className={isExpanded ? 'rotate-180 transition-transform' : ''} />
                    </button>
                    <Link to={`/project/${p.id}`} className="text-[10px] font-bold uppercase tracking-[0.4em] text-stone-400 hover:text-stone-900 dark:hover:text-white transition-all flex items-center gap-2">
                        Details <ExternalLink size={12} />
                    </Link>
                </div>
            </div>
        </motion.div>
    );
}
