import { motion, AnimatePresence } from 'framer-motion';
import { GraduationCap, Calendar, MapPin, Award, BookOpen, Plus, Edit2, Trash2, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Education() {
    const [education, setEducation] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);
    
    const [form, setForm] = useState({ id: null, degree: '', institution: '', year: '', grade: '' });

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchEdu = async () => {
        setLoading(true);
        const { data } = await supabase.from('education').select('*').order('year', { ascending: false });
        if (data) setEducation(data);
        setLoading(false);
    };

    useEffect(() => {
        checkAdmin();
        fetchEdu();
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            if (form.id) {
                await supabase.from('education').update(form).eq('id', form.id);
            } else {
                const { id, ...newEdu } = form;
                await supabase.from('education').insert([newEdu]);
            }
            fetchEdu();
            setShowModal(false);
            setForm({ id: null, degree: '', institution: '', year: '', grade: '' });
        } catch (error) {
            console.error(error);
        }
    };

    const deleteEdu = async (id) => {
        if (window.confirm('Delete this entry?')) {
            await supabase.from('education').delete().eq('id', id);
            fetchEdu();
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { staggerChildren: 0.2 } }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { y: 0, opacity: 1, transition: { type: 'spring', damping: 20, stiffness: 100 } }
    };

    const getEduDescription = (edu) => {
        const degree = edu.degree?.toLowerCase() || '';
        const inst = edu.institution?.toLowerCase() || '';
        
        if (degree.includes('btech') || degree.includes('b.tech') || degree.includes('bachelor')) {
            return "Focused on building a strong foundation in electronics and communication engineering, consistently striving for academic excellence and technical mastery.";
        }
        if (degree.includes('12th') || inst.includes('junior') || inst.includes('intermediate')) {
            return "Completed higher secondary education with a focus on Mathematics, Physics, and Chemistry, establishing a rigorous analytical foundation for technical studies.";
        }
        if (degree.includes('10th') || degree.includes('ssc') || inst.includes('school')) {
            return "Established a robust academic base through a comprehensive secondary curriculum, fostering early interests in science and technology.";
        }
        return "Dedicated to academic growth and the pursuit of knowledge, maintaining a high standard of performance throughout the curriculum.";
    };

    return (
        <div className="pb-20">
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto mb-24 text-center relative">
                {isAdmin && (
                    <motion.button 
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => { setForm({ id: null, degree: '', institution: '', year: '', grade: '' }); setShowModal(true); }}
                        className="absolute right-0 top-1/2 -translate-y-1/2 flex items-center gap-2 bg-stone-900 dark:bg-white text-white dark:text-stone-900 px-6 py-3 rounded-sm font-bold uppercase tracking-widest text-[10px] shadow-xl hover:bg-stone-800 dark:hover:bg-stone-100 transition-all"
                    >
                        <Plus size={16} /> Add Entry
                    </motion.button>
                )}
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-6 text-stone-900 dark:text-white">
                    Academic <span className="text-stone-400">Journey</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Foundation of Engineering Excellence</p>
            </motion.div>

            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="max-w-4xl mx-auto space-y-24">
                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="w-12 h-12 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin"></div>
                    </div>
                ) : education.length > 0 ? education.map((edu, idx) => (
                    <motion.div key={edu.id} variants={itemVariants} className="relative pl-12 md:pl-20 border-l border-stone-200 dark:border-white/10 group">
                        {/* Admin Controls */}
                        {isAdmin && (
                            <div className="absolute right-0 top-0 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <button onClick={() => { setForm(edu); setShowModal(true); }} className="p-2 text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                                    <Edit2 size={16} />
                                </button>
                                <button onClick={() => deleteEdu(edu.id)} className="p-2 text-stone-400 hover:text-red-500 transition-colors">
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        )}

                        {/* Timeline Dot */}
                        <div className="absolute -left-[9px] top-0 w-4 h-4 bg-white dark:bg-stone-950 border-2 border-stone-900 dark:border-white rounded-full group-hover:scale-150 transition-transform duration-500 z-10" />
                        
                        <div className="space-y-6">
                            <div className="space-y-2">
                                <div className="flex flex-wrap items-center gap-6 text-xs font-bold uppercase tracking-[0.4em] text-stone-400 mb-2">
                                    <span className="flex items-center gap-2"><Calendar size={16}/> {edu.year}</span>
                                    {edu.grade && <span className="flex items-center gap-2 text-stone-900 dark:text-white bg-stone-100 dark:bg-stone-800 px-3 py-1 rounded-sm"><Award size={16}/> {edu.grade}</span>}
                                </div>
                                <h2 className="text-3xl md:text-5xl font-bold uppercase tracking-tight text-stone-900 dark:text-white leading-none">{edu.institution}</h2>
                                {edu.degree && <p className="text-xl md:text-2xl text-stone-600 dark:text-stone-400 italic font-light">{edu.degree}</p>}
                            </div>

                            <div className="flex items-center gap-6 pt-4">
                                <div className="p-4 bg-stone-50 dark:bg-stone-900/50 rounded-sm border border-stone-100 dark:border-white/5">
                                    <GraduationCap size={32} className="text-stone-400 opacity-50" />
                                </div>
                                <div className="max-w-2xl">
                                    <p className="text-base text-stone-500 dark:text-stone-400 leading-relaxed font-light italic">
                                        {getEduDescription(edu)}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )) : (
                    <div className="text-center py-20 text-stone-400 italic font-medium">Academic history being updated...</div>
                )}
            </motion.div>

            {/* Modal */}
            <AnimatePresence>
                {showModal && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className="bg-white dark:bg-stone-900 w-full max-w-lg p-8 rounded-sm shadow-2xl overflow-y-auto max-h-[90vh]"
                        >
                            <div className="flex justify-between items-center mb-8 border-b border-stone-100 dark:border-white/5 pb-4">
                                <h3 className="text-2xl font-bold uppercase tracking-tighter">
                                    {form.id ? 'Edit Education' : 'Add Education'}
                                </h3>
                                <button onClick={() => setShowModal(false)} className="text-stone-400 hover:text-stone-900 dark:hover:text-white">
                                    <X size={24} />
                                </button>
                            </div>

                            <form onSubmit={handleSave} className="space-y-6">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Institution Name</label>
                                    <input
                                        required
                                        value={form.institution}
                                        onChange={e => setForm({ ...form, institution: e.target.value })}
                                        placeholder="e.g. University of Technology"
                                        className="w-full p-4 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm focus:border-stone-900 transition-colors"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Degree (Optional)</label>
                                    <input
                                        value={form.degree}
                                        onChange={e => setForm({ ...form, degree: e.target.value })}
                                        placeholder="e.g. B.Tech in Electronics"
                                        className="w-full p-4 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm focus:border-stone-900 transition-colors"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Year / Duration</label>
                                        <input
                                            required
                                            value={form.year}
                                            onChange={e => setForm({ ...form, year: e.target.value })}
                                            placeholder="e.g. 2022 - 2026"
                                            className="w-full p-4 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm focus:border-stone-900 transition-colors"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">CGPA / Percentage</label>
                                        <input
                                            required
                                            value={form.grade}
                                            onChange={e => setForm({ ...form, grade: e.target.value })}
                                            placeholder="e.g. 9.2 or 85%"
                                            className="w-full p-4 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm focus:border-stone-900 transition-colors"
                                        />
                                    </div>
                                </div>

                                <div className="pt-6 flex justify-end gap-4">
                                    <button
                                        type="button"
                                        onClick={() => setShowModal(false)}
                                        className="px-6 py-3 font-bold uppercase tracking-widest text-[10px] text-stone-500 hover:text-stone-900 transition-colors"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="bg-stone-900 dark:bg-white text-white dark:text-stone-900 px-10 py-3 rounded-sm font-bold uppercase tracking-widest text-[10px] shadow-xl hover:bg-stone-800 transition-all"
                                    >
                                        {form.id ? 'Update Entry' : 'Save Entry'}
                                    </button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
}
