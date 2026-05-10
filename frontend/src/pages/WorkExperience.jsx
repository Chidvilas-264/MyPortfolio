import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { Briefcase, Calendar, MapPin, Plus, Edit2, Trash2, X, ExternalLink, Image as ImageIcon } from 'lucide-react';

export default function WorkExperience() {
    const [workExp, setWorkExp] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [selectedImage, setSelectedImage] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);

    const [form, setForm] = useState({
        id: null,
        company: '',
        position: '',
        projectName: '',
        startDate: '',
        endDate: '',
        workMode: 'On-site',
        description: '',
        location: '',
        link: '',
        image_url: ''
    });

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchExp = async () => {
        setLoading(true);
        const { data } = await supabase.from('work_experience').select('*').order('start_date', { ascending: false });
        if (data) {
            setWorkExp(data.map(e => ({
                ...e,
                projectName: e.project_name,
                workMode: e.work_mode
            })));
        }
        setLoading(false);
    };

    useEffect(() => {
        checkAdmin();
        fetchExp();
    }, []);

    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape') setShowModal(false);
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            let imageUrl = form.image_url;

            if (selectedImage) {
                const fileName = `exp_${Date.now()}`;
                const { data } = await supabase.storage.from('project-images').upload(fileName, selectedImage);
                if (data) imageUrl = supabase.storage.from('project-images').getPublicUrl(data.path).data.publicUrl;
            }

            const expData = { 
                company: form.company,
                position: form.position,
                project_name: form.projectName,
                start_date: form.startDate,
                end_date: form.endDate,
                work_mode: form.workMode,
                description: form.description,
                location: form.location,
                link: form.link,
                image_url: imageUrl 
            };
            
            if (form.id) {
                await supabase.from('work_experience').update(expData).eq('id', form.id);
            } else {
                await supabase.from('work_experience').insert([expData]);
            }

            fetchExp();
            setShowModal(false);
            resetForm();
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setForm({
            id: null,
            company: '',
            position: '',
            projectName: '',
            startDate: '',
            endDate: '',
            workMode: 'On-site',
            description: '',
            location: '',
            link: '',
            image_url: ''
        });
        setSelectedImage(null);
    };

    const editExp = (exp) => {
        setForm(exp);
        setShowModal(true);
    };

    const deleteExp = async (id) => {
        if (window.confirm('Delete this experience entry?')) {
            await supabase.from('work_experience').delete().eq('id', id);
            fetchExp();
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { y: 0, opacity: 1 }
    };

    return (
        <div className="pb-20">
            {isAdmin && (
                <button 
                    onClick={() => { resetForm(); setShowModal(true); }}
                    className="fixed bottom-8 right-8 z-50 bg-stone-900 dark:bg-white text-white dark:text-stone-900 p-4 rounded-full shadow-2xl hover:scale-110 transition-transform"
                >
                    <Plus size={24} />
                </button>
            )}

            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto mb-20 text-center">
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-6 text-stone-900 dark:text-white">
                    Work <span className="text-stone-400">Experience</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">My Professional Journey</p>
            </motion.div>

            <AnimatePresence>
                {showModal && (
                    <div className="fixed inset-0 bg-black/60 backdrop-blur-md z-50 flex items-center justify-center p-4">
                        <motion.div 
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="bg-white dark:bg-stone-900 rounded-sm shadow-2xl max-w-lg w-full flex flex-col max-h-[90vh]"
                        >
                            <div className="flex justify-between items-center p-6 border-b border-stone-100 dark:border-stone-800 shrink-0">
                                <h3 className="text-xl font-bold uppercase tracking-tighter text-stone-900 dark:text-white">
                                    {form.id ? 'Edit Entry' : 'Add Experience'}
                                </h3>
                                <button onClick={() => setShowModal(false)} className="text-stone-400 hover:text-stone-900 dark:hover:text-white">
                                    <X size={20}/>
                                </button>
                            </div>

                            <div className="p-6 overflow-y-auto custom-scrollbar">
                                <form onSubmit={handleSave} className="space-y-6">
                                    <div className="grid grid-cols-1 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Job Title / Role</label>
                                            <input value={form.position} onChange={e=>setForm({...form, position: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="e.g. Software Intern" required/>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Company Name</label>
                                            <input value={form.company} onChange={e=>setForm({...form, company: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Company Name" required/>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Project Name</label>
                                            <input value={form.projectName} onChange={e=>setForm({...form, projectName: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Main Project Worked On"/>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="space-y-2">
                                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Start Date</label>
                                                <input value={form.startDate} onChange={e=>setForm({...form, startDate: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Month YYYY" required/>
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">End Date</label>
                                                <input value={form.endDate} onChange={e=>setForm({...form, endDate: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Present or Month YYYY" required/>
                                            </div>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="space-y-2">
                                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Work Mode</label>
                                                <select value={form.workMode} onChange={e=>setForm({...form, workMode: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm">
                                                    <option>On-site</option>
                                                    <option>Remote</option>
                                                    <option>Hybrid</option>
                                                </select>
                                            </div>
                                            <div className="space-y-2">
                                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Location</label>
                                                <input value={form.location} onChange={e=>setForm({...form, location: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="City, Country"/>
                                            </div>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">LinkedIn / Cert Link</label>
                                            <input value={form.link} onChange={e=>setForm({...form, link: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-xs" placeholder="https://linkedin.com/..."/>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Picture / Logo</label>
                                            <input type="file" onChange={e=>setSelectedImage(e.target.files[0])} className="w-full p-2 text-xs text-stone-500 file:mr-4 file:py-2 file:px-4 file:rounded-sm file:border-0 file:text-[10px] file:font-bold file:bg-stone-100 dark:file:bg-stone-800 dark:file:text-white hover:file:bg-stone-200" />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Description</label>
                                            <textarea rows={4} value={form.description} onChange={e=>setForm({...form, description: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Describe your key contributions..."></textarea>
                                        </div>
                                    </div>
                                    <div className="pt-4 sticky bottom-0 bg-white dark:bg-stone-900 pb-2">
                                        <button type="submit" className="w-full bg-stone-900 dark:bg-white text-white dark:text-stone-900 py-4 font-bold uppercase tracking-[0.3em] text-[10px] hover:opacity-90 transition-all shadow-xl">
                                            Save Experience
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-12">
                {loading ? (
                    <div className="col-span-full flex justify-center py-20">
                        <div className="w-12 h-12 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin"></div>
                    </div>
                ) : workExp.length > 0 ? workExp.map((exp, idx) => (
                    <ExperienceCard key={idx} exp={exp} isAdmin={isAdmin} editExp={editExp} deleteExp={deleteExp} itemVariants={itemVariants} />
                )) : (
                    <div className="col-span-full text-center py-20 text-stone-400 italic font-medium">No experience entries found.</div>
                )}
            </motion.div>
        </div>
    );
}

function ExperienceCard({ exp, isAdmin, editExp, deleteExp, itemVariants }) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <motion.div variants={itemVariants} initial="hidden" animate="visible" className="group transition-all duration-500 overflow-hidden flex flex-col h-fit relative border-b border-stone-200 dark:border-white/10 pb-16">
            {isAdmin && (
                <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity z-20">
                    <button onClick={() => editExp(exp)} className="p-2 bg-white dark:bg-black rounded-sm shadow-xl text-stone-600 hover:text-stone-900 dark:text-stone-400 dark:hover:text-white transition-transform hover:scale-110"><Edit2 size={16}/></button>
                    <button onClick={() => deleteExp(exp.id)} className="p-2 bg-white dark:bg-black rounded-sm shadow-xl text-red-400 hover:text-red-600 transition-transform hover:scale-110"><Trash2 size={16}/></button>
                </div>
            )}

            <div className="w-full mb-10 overflow-hidden rounded-sm">
                {exp.image_url ? (
                    <img 
                        src={exp.image_url} 
                        alt={exp.company} 
                        className="w-full h-full object-cover grayscale-[20%] group-hover:grayscale-0 transition-all duration-700 group-hover:scale-105" 
                    />
                ) : (
                    <div className="w-full h-24 flex items-center justify-start">
                        <Briefcase size={40} className="text-stone-400 opacity-20" />
                    </div>
                )}
            </div>

            <div className="space-y-8">
                <div className="space-y-4">
                    <div className="flex justify-between items-start">
                        <span className="text-[10px] font-bold uppercase tracking-[0.5em] text-stone-400">{exp.company}</span>
                        <span className="text-[9px] font-bold uppercase tracking-[0.2em] text-stone-500 italic opacity-60">{exp.workMode}</span>
                    </div>
                    <h2 className="text-4xl md:text-5xl font-bold uppercase tracking-tighter text-stone-900 dark:text-white leading-none group-hover:text-stone-600 dark:group-hover:text-stone-400 transition-colors">{exp.position}</h2>
                    <div className="flex flex-wrap gap-8 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-500">
                        <span className="flex items-center gap-2"><Calendar size={14} className="text-stone-400 opacity-50"/> {exp.startDate} — {exp.endDate}</span>
                        <span className="flex items-center gap-2"><MapPin size={14} className="text-stone-400 opacity-50"/> {exp.location}</span>
                    </div>
                </div>

                <AnimatePresence>
                    {isExpanded && (
                        <motion.div 
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="overflow-hidden space-y-8"
                        >
                            {exp.projectName && (
                                <div className="space-y-2 border-l border-stone-200 dark:border-white/10 pl-6">
                                    <span className="text-[10px] font-bold uppercase tracking-widest text-stone-400 block opacity-60">Primary Project</span>
                                    <p className="text-stone-900 dark:text-white font-bold text-xl tracking-tight">{exp.projectName}</p>
                                </div>
                            )}
                            <p className="text-xl text-stone-600 dark:text-stone-400 leading-relaxed font-light italic">
                                "{exp.description}"
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>

                <div className="flex justify-between items-center pt-4">
                    <button 
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="group/read flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.4em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-6 transition-all"
                    >
                        {isExpanded ? 'Collapse' : 'Expand Details'} 
                        <ExternalLink size={12} className={isExpanded ? 'rotate-180 transition-transform' : ''} />
                    </button>
                    {exp.link && (
                        <a href={exp.link} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.4em] text-stone-400 hover:text-stone-900 dark:hover:text-white transition-all">
                            Evidence <ExternalLink size={12}/>
                        </a>
                    )}
                </div>
            </div>
        </motion.div>
    );
}
