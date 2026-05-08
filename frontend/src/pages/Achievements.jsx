import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { Trophy, Plus, Edit2, Trash2, X, Image as ImageIcon, ExternalLink, Calendar } from 'lucide-react';

export default function Achievements() {
    const [achievements, setAchievements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [selectedImage, setSelectedImage] = useState(null);
    const [isAdmin, setIsAdmin] = useState(false);

    const [form, setForm] = useState({
        id: null,
        title: '',
        description: '',
        link: '',
        date: '',
        image_url: ''
    });

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchAchievements = async () => {
        setLoading(true);
        const { data } = await supabase.from('achievements').select('*').order('date', { ascending: false });
        if (data) setAchievements(data);
        setLoading(false);
    };

    useEffect(() => {
        checkAdmin();
        fetchAchievements();
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
                const fileName = `ach_${Date.now()}`;
                const { data } = await supabase.storage.from('project-images').upload(fileName, selectedImage);
                if (data) imageUrl = supabase.storage.from('project-images').getPublicUrl(data.path).data.publicUrl;
            }

            const achData = {
                title: form.title,
                description: form.description,
                link: form.link,
                date: form.date,
                image_url: imageUrl
            };
            if (form.id) {
                await supabase.from('achievements').update(achData).eq('id', form.id);
            } else {
                await supabase.from('achievements').insert([achData]);
            }

            fetchAchievements();
            setShowModal(false);
            resetForm();
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setForm({ id: null, title: '', description: '', link: '', date: '', image_url: '' });
        setSelectedImage(null);
    };

    const editAchievement = (ach) => {
        setForm(ach);
        setShowModal(true);
    };

    const deleteAchievement = async (id) => {
        if (window.confirm('Delete this achievement?')) {
            await supabase.from('achievements').delete().eq('id', id);
            fetchAchievements();
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
                    Key <span className="text-stone-400">Achievements</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Honors, Awards & Recognition</p>
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
                                    {form.id ? 'Edit Achievement' : 'Add Achievement'}
                                </h3>
                                <button onClick={() => setShowModal(false)} className="text-stone-400 hover:text-stone-900 dark:hover:text-white">
                                    <X size={20}/>
                                </button>
                            </div>

                            <div className="p-6 overflow-y-auto custom-scrollbar">
                                <form onSubmit={handleSave} className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Achievement Title</label>
                                        <input value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="e.g. Best Innovation Award" required/>
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Date</label>
                                            <input value={form.date} onChange={e=>setForm({...form, date: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="e.g. 2026" required/>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Redirect Link</label>
                                            <input value={form.link} onChange={e=>setForm({...form, link: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="https://..."/>
                                        </div>
                                    </div>
                                    <div className="p-6 border-2 border-dashed border-stone-100 dark:border-stone-800 rounded-sm hover:border-stone-400 transition-colors">
                                        <label className="flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest mb-4"><ImageIcon size={18} className="text-stone-400"/> Achievement Photo / Icon</label>
                                        <input type="file" accept="image/*" onChange={e => setSelectedImage(e.target.files[0])} className="w-full text-xs text-stone-500 file:mr-4 file:py-2 file:px-4 file:rounded-sm file:border-0 file:text-[10px] file:font-bold file:bg-stone-100 dark:file:bg-stone-800 dark:file:text-white" />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Short Description</label>
                                        <textarea rows={4} value={form.description} onChange={e=>setForm({...form, description: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm text-sm" placeholder="Describe the achievement..." required></textarea>
                                    </div>
                                    <div className="pt-4 sticky bottom-0 bg-white dark:bg-stone-900 pb-2">
                                        <button type="submit" className="w-full bg-stone-900 dark:bg-white text-white dark:text-stone-900 py-4 font-bold uppercase tracking-[0.3em] text-[10px] hover:opacity-90 transition-all shadow-xl">
                                            Save Achievement
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
                {loading ? (
                    <div className="col-span-full flex justify-center py-20">
                        <div className="w-12 h-12 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin"></div>
                    </div>
                ) : achievements.length > 0 ? achievements.map((ach, idx) => (
                    <AchCard key={ach.id} ach={ach} isAdmin={isAdmin} editAchievement={editAchievement} deleteAchievement={deleteAchievement} itemVariants={itemVariants} />
                )) : (
                    <div className="col-span-full text-center py-20 text-stone-400 italic font-medium">No achievements added yet.</div>
                )}
            </motion.div>
        </div>
    );
}

function AchCard({ ach, isAdmin, editAchievement, deleteAchievement, itemVariants }) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <motion.div variants={itemVariants} whileInView="visible" viewport={{ once: false }} className="relative group transition-all duration-500 border-b border-stone-200 dark:border-white/10 pb-12">
            {isAdmin && (
                <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity z-20">
                    <button onClick={() => editAchievement(ach)} className="p-2 bg-white dark:bg-black rounded-sm shadow-xl text-stone-600 hover:text-stone-900 dark:text-stone-400 dark:hover:text-white transition-transform hover:scale-110"><Edit2 size={16}/></button>
                    <button onClick={() => deleteAchievement(ach.id)} className="p-2 bg-white dark:bg-black rounded-sm shadow-xl text-red-400 hover:text-red-600 transition-transform hover:scale-110"><Trash2 size={16}/></button>
                </div>
            )}

            <div className="flex flex-col items-center text-center">
                <div className="w-full max-w-[180px] mb-8 bg-stone-200 dark:bg-stone-800 rounded-sm overflow-hidden border border-stone-100 dark:border-white/5 shadow-lg group-hover:scale-105 transition-transform duration-500">
                    {ach.image_url ? (
                        <img 
                            src={ach.image_url} 
                            alt={ach.title} 
                            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" 
                        />
                    ) : (
                        <div className="w-full h-32 flex items-center justify-center">
                            <Trophy size={40} className="text-stone-400" />
                        </div>
                    )}
                </div>
                
                <div className="space-y-4 w-full">
                    <div className="flex flex-col items-center gap-2">
                        <span className="text-[10px] font-bold uppercase tracking-[0.4em] text-stone-400 flex items-center gap-2"><Calendar size={12}/> {ach.date}</span>
                        <h3 className="text-2xl font-bold uppercase tracking-tight text-stone-900 dark:text-white leading-tight">{ach.title}</h3>
                    </div>
                    
                    <AnimatePresence>
                        {isExpanded && (
                            <motion.div 
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                className="overflow-hidden"
                            >
                                <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed font-light italic mb-4">"{ach.description}"</p>
                                {ach.link && (
                                    <a href={ach.link} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all">
                                        View Details <ExternalLink size={12} />
                                    </a>
                                )}
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <div className="pt-2">
                        <button 
                            onClick={() => setIsExpanded(!isExpanded)}
                            className="text-[10px] font-bold uppercase tracking-[0.3em] text-stone-400 hover:text-stone-900 dark:hover:text-white transition-all border-b border-stone-100 dark:border-white/5 pb-1"
                        >
                            {isExpanded ? 'Show Less' : 'Honor Details'} 
                        </button>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
