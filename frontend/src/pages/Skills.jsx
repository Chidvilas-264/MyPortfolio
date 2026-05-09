import { motion } from 'framer-motion';
import { Plus, Edit2, Trash2, X, ExternalLink } from 'lucide-react';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Skills() {
    const [skills, setSkills] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);

    const [form, setForm] = useState({ id: null, name: '', category: '', evidenceLink: '' });

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchSkills = async () => {
        const { data } = await supabase.from('skills').select('*').order('name');
        if (data) {
            setSkills(data.map(s => ({
                ...s,
                evidenceLink: s.evidence_link
            })));
        }
    };

    useEffect(() => { 
        checkAdmin();
        fetchSkills(); 
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            const skillData = { 
                name: form.name, 
                category: form.category, 
                evidence_link: form.evidenceLink 
            };
            if (form.id) {
                await supabase.from('skills').update(skillData).eq('id', form.id);
            } else {
                await supabase.from('skills').insert([skillData]);
            }
            fetchSkills();
            setShowModal(false);
            setForm({ id: null, name: '', category: '', evidenceLink: '' });
        } catch (err) {
            console.error(err);
        }
    };

    const deleteSkill = async (id) => {
        if(window.confirm('Delete this skill?')) {
            await supabase.from('skills').delete().eq('id', id);
            fetchSkills();
        }
    };

    const editSkill = (s) => {
        setForm({ id: s.id, name: s.name, category: s.category, evidenceLink: s.evidenceLink || '' });
        setShowModal(true);
    };

    const groupedSkills = skills.reduce((acc, skill) => {
        const cat = skill.category || 'Other';
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(skill);
        return acc;
    }, {});

    const categories = [...new Set(skills.map(s => s.category))];

    const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.15 } } };
    const itemVariants = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1, transition: { type: 'spring' } } };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto px-4 py-32 relative">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, name: '', category: '', evidenceLink: '' }); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-sm w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white uppercase tracking-tight">{form.id ? 'Edit Entry' : 'Add Skill to Category'}</h3>
                            <button onClick={() => setShowModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSave} className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Category Name</label>
                                <input 
                                    list="categories-list"
                                    placeholder="e.g. Hardware, Software, Tools" 
                                    value={form.category} 
                                    onChange={e=>setForm({...form, category: e.target.value})} 
                                    className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm font-medium" 
                                    required
                                />
                                <datalist id="categories-list">
                                    {categories.map(c => <option key={c} value={c} />)}
                                </datalist>
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Skill / Tool Name</label>
                                <input 
                                    placeholder="e.g. React.js, Verilog, AutoCAD" 
                                    value={form.name} 
                                    onChange={e=>setForm({...form, name: e.target.value})} 
                                    className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm font-medium" 
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Work/Cert Link (Optional)</label>
                                <input 
                                    placeholder="https://..." 
                                    value={form.evidenceLink} 
                                    onChange={e=>setForm({...form, evidenceLink: e.target.value})} 
                                    className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm font-medium text-xs" 
                                />
                            </div>
                            <div className="flex justify-end gap-4 pt-4">
                                <button type="submit" className="bg-stone-900 dark:bg-white text-white dark:text-stone-900 px-8 py-3 font-bold rounded-sm hover:opacity-90 w-full tracking-[0.2em] uppercase text-[10px] transition-all">Save Entry</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <motion.div variants={itemVariants} className="text-center mb-24">
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-4 text-stone-900 dark:text-white">
                    Technical <span className="text-stone-400">Expertise</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Engineering proficiency & toolsets</p>
            </motion.div>
            
            <div className="space-y-24">
                {Object.keys(groupedSkills).map((category) => (
                    <motion.div key={category} variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.05 }} className="relative">
                        <div className="flex flex-col md:flex-row gap-12">
                            <div className="md:w-1/4">
                                <motion.h3 variants={itemVariants} className="text-3xl font-bold uppercase tracking-tighter text-stone-900 dark:text-white sticky top-32">{category}</motion.h3>
                            </div>
                            <div className="md:w-3/4 grid grid-cols-1 sm:grid-cols-2 gap-x-12 gap-y-8">
                                {groupedSkills[category].map(s => (
                                    <motion.div key={s.id} variants={itemVariants} className="relative group border-b border-stone-200 dark:border-white/10 pb-2">
                                        <div className="flex justify-between items-center group">
                                            <div className="flex items-center gap-3">
                                                <span className="text-sm font-bold text-stone-800 dark:text-stone-200 uppercase tracking-widest leading-none">{s.name}</span>
                                                {s.evidenceLink && (
                                                    <a href={s.evidenceLink} target="_blank" rel="noreferrer" className="text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                                                        <ExternalLink size={14}/>
                                                    </a>
                                                )}
                                            </div>
                                            
                                            {isAdmin && (
                                                <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                    <button onClick={() => editSkill(s)} className="p-2 text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors">
                                                        <Edit2 size={16}/>
                                                    </button>
                                                    <button onClick={() => deleteSkill(s.id)} className="p-2 text-stone-400 hover:text-red-600 transition-colors">
                                                        <Trash2 size={16}/>
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
            {skills.length === 0 && <motion.p variants={itemVariants} className="text-center text-stone-500 mt-10 text-xl font-medium">No skills added yet.</motion.p>}
        </motion.div>
    );
}
