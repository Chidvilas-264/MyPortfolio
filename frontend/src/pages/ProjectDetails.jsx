import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ExternalLink, X } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';
import { supabase } from '../supabaseClient';

export default function ProjectDetails() {
    const { id } = useParams();
    const [project, setProject] = useState(null);
    const [selectedImg, setSelectedImg] = useState(null);

    useEffect(() => {
        supabase.from('projects').select('*').eq('id', id).maybeSingle().then(({ data }) => {
            if (data) {
                setProject({
                    ...data,
                    githubLink: data.github_link,
                    demoLink: data.demo_link,
                    techStack: data.tech_stack
                });
            }
        }).catch(console.error);
    }, [id]);

    if(!project) return <div className="text-center py-20 text-slate-500 dark:text-slate-400">Loading project details...</div>;

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-5xl mx-auto">
            <Link to={project.category === 'Hardware' ? '/hardware' : '/software'} className="inline-flex items-center text-slate-500 hover:text-stone-800 dark:text-slate-400 dark:hover:text-stone-300 mb-8 font-medium transition-colors">
                <ArrowLeft size={16} className="mr-2" /> Back to {project.category} Projects
            </Link>
            
            <div className="glass-card p-8 md:p-12 mb-12">
                <h1 className="text-4xl md:text-5xl font-bold text-slate-800 dark:text-white mb-6">{project.title}</h1>
                <div className="flex flex-wrap gap-4 mb-8">
                    {project.githubLink && (
                        <a href={project.githubLink} className="inline-flex items-center px-4 py-2 bg-slate-900 text-white dark:bg-slate-800 rounded-sm hover:bg-slate-800 dark:hover:bg-slate-700 transition-colors" target="_blank" rel="noreferrer">
                            <FaGithub size={18} className="mr-2" /> View Source
                        </a>
                    )}
                    {project.demoLink && (
                        <a href={project.demoLink} className="inline-flex items-center px-4 py-2 bg-stone-800 text-white rounded-sm hover:bg-stone-900 transition-colors shadow-lg shadow-stone-700/30" target="_blank" rel="noreferrer">
                            <ExternalLink size={18} className="mr-2" /> Live Demo
                        </a>
                    )}
                </div>
                
                <h3 className="text-sm font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-3">About the Project</h3>
                <p className="text-slate-700 dark:text-slate-300 text-lg leading-relaxed whitespace-pre-wrap mb-10">{project.description}</p>
                
                <h3 className="text-sm font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-4">Technologies Used</h3>
                <div className="flex flex-wrap gap-3">
                    {project.techStack?.split(',').map(t => (
                        <span key={t} className="px-4 py-2 bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-sm text-slate-700 dark:text-slate-300 font-medium shadow-sm">{t.trim()}</span>
                    ))}
                </div>
            </div>

            {project.image_url && (
                <div className="mb-12">
                    <h3 className="text-2xl font-bold text-slate-800 dark:text-white mb-6">Project Preview</h3>
                    <div className="rounded-sm overflow-hidden glass-card aspect-video max-w-3xl mx-auto cursor-pointer" onClick={() => setSelectedImg(project.image_url)}>
                        <img src={project.image_url} alt={project.title} className="w-full h-full object-cover hover:scale-105 transition-transform duration-500" />
                    </div>
                </div>
            )}

            {selectedImg && (
                <div className="fixed inset-0 bg-slate-900/95 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setSelectedImg(null)}>
                    <button className="absolute top-6 right-6 text-white bg-white/10 hover:bg-white/20 p-2 rounded-full backdrop-blur-md transition-colors"><X size={24} /></button>
                    <img src={selectedImg} alt="Fullscreen" className="max-w-full max-h-full object-contain rounded-sm shadow-2xl" />
                </div>
            )}
        </motion.div>
    );
}