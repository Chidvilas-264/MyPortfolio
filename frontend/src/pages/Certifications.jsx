import { motion, AnimatePresence } from 'framer-motion';
import { ExternalLink, Plus, Edit2, Trash2, X, Image as ImageIcon, Award } from 'lucide-react';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Certifications() {
    const [certs, setCerts] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);

    const [form, setForm] = useState({ id: null, title: '', provider: '', date: '', verificationLink: '', image_url: '' });
    const [file, setFile] = useState(null);

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    const fetchCerts = async () => {
        const { data } = await supabase.from('certifications').select('*').order('title', { ascending: true });
        if (data) {
            setCerts(data.map(c => ({
                ...c,
                verificationLink: c.verification_link
            })));
        }
    };

    useEffect(() => { 
        checkAdmin();
        fetchCerts(); 
    }, []);

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            let imageUrl = form.image_url;

            if (file) {
                const fileName = `cert_${Date.now()}`;
                const { data } = await supabase.storage.from('project-images').upload(fileName, file);
                if (data) imageUrl = supabase.storage.from('project-images').getPublicUrl(data.path).data.publicUrl;
            }

            const certData = {
                title: form.title,
                provider: form.provider,
                date: form.date,
                verification_link: form.verificationLink,
                image_url: imageUrl
            };

            if (form.id) {
                await supabase.from('certifications').update(certData).eq('id', form.id);
            } else {
                await supabase.from('certifications').insert([certData]);
            }

            fetchCerts();
            setShowModal(false);
            setForm({ id: null, title: '', provider: '', date: '', verificationLink: '', image_url: '' });
            setFile(null);
        } catch (err) {
            console.error(err);
        }
    };

    const editCert = (c) => {
        setForm(c);
        setShowModal(true);
    };

    const deleteCert = async (id) => {
        if(window.confirm('Delete this certification?')) {
            await supabase.from('certifications').delete().eq('id', id);
            fetchCerts();
        }
    };

    const containerVariants = { 
        hidden: { opacity: 0 }, 
        visible: { opacity: 1, transition: { staggerChildren: 0.15 } } 
    };
    const itemVariants = { 
        hidden: { y: 40, opacity: 0 }, 
        visible: { y: 0, opacity: 1, transition: { type: 'spring', damping: 20, stiffness: 100 } } 
    };

    return (
        <motion.div initial="hidden" animate="visible" variants={containerVariants} className="max-w-6xl mx-auto relative">
            {isAdmin && (
                <button onClick={() => {setForm({ id: null, title: '', provider: '', date: '', verificationLink: '' }); setFile(null); setShowModal(true);}} className="fixed bottom-8 right-8 z-50 bg-stone-900 dark:bg-white text-white dark:text-stone-900 p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    <Plus size={24}/>
                </button>
            )}

            {showModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold uppercase tracking-tighter text-stone-900 dark:text-white">{form.id ? 'Edit Certification' : 'Add Credential'}</h3>
                            <button onClick={() => setShowModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSave} className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Certification Title</label>
                                <input placeholder="e.g. AWS Certified Developer" value={form.title} onChange={e=>setForm({...form, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Issuing Organization</label>
                                <input placeholder="e.g. Amazon Web Services" value={form.provider} onChange={e=>setForm({...form, provider: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Date Earned</label>
                                    <input placeholder="May 2026" value={form.date} onChange={e=>setForm({...form, date: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Credential ID / Link</label>
                                    <input placeholder="Optional Link" value={form.verificationLink} onChange={e=>setForm({...form, verificationLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                </div>
                            </div>
                            <div className="p-6 border-2 border-dashed border-stone-100 dark:border-stone-800 rounded-sm hover:border-stone-400 transition-colors">
                                <label className="flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest mb-4"><ImageIcon size={18} className="text-stone-400"/> Certificate Image / Logo</label>
                                <input type="file" accept="image/*" onChange={e => setFile(e.target.files[0])} className="w-full text-xs text-stone-500 file:mr-4 file:py-2 file:px-4 file:rounded-sm file:border-0 file:text-[10px] file:font-bold file:bg-stone-100 dark:file:bg-stone-800 dark:file:text-white" />
                            </div>
                            <div className="pt-4">
                                <button type="submit" className="bg-stone-900 dark:bg-white text-white dark:text-stone-900 px-8 py-4 font-bold rounded-sm hover:opacity-90 w-full tracking-[0.3em] uppercase text-xs transition-all shadow-xl">Save Credential</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <motion.div variants={itemVariants} initial="hidden" animate="visible" className="text-center mb-24">
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-4 text-stone-900 dark:text-white">
                    Verified <span className="text-stone-400">Credentials</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Professional certifications & engineering training</p>
            </motion.div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
                {certs.map((c) => (
                    <CertCard key={c.id} c={c} isAdmin={isAdmin} editCert={editCert} deleteCert={deleteCert} itemVariants={itemVariants} />
                ))}
            </div>
            {certs.length === 0 && <motion.p variants={itemVariants} className="text-center text-stone-500 mt-10 text-xl font-medium">No certifications uploaded yet.</motion.p>}
        </motion.div>
    );
}

function CertCard({ c, isAdmin, editCert, deleteCert, itemVariants }) {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <motion.div variants={itemVariants} initial="hidden" animate="visible" className="relative group border-b border-stone-200 dark:border-white/10 pb-12">
            {isAdmin && (
                <div className="absolute top-4 right-4 z-20 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={() => editCert(c)} className="p-2 bg-white dark:bg-black text-stone-800 dark:text-stone-200 rounded-sm shadow-xl hover:scale-110 transition-transform"><Edit2 size={16}/></button>
                    <button onClick={() => deleteCert(c.id)} className="p-2 bg-white dark:bg-black text-red-600 rounded-sm shadow-xl hover:scale-110 transition-transform"><Trash2 size={16}/></button>
                </div>
            )}
            
            <div className="w-full mb-8 overflow-hidden bg-stone-100 dark:bg-stone-900 border border-stone-100 dark:border-white/5 relative group cursor-pointer shadow-sm hover:shadow-2xl transition-all duration-500 rounded-sm">
                {c.image_url ? (
                    <img 
                        src={c.image_url} 
                        alt={c.title} 
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" 
                    />
                ) : (
                    <div className="w-full h-48 flex items-center justify-center text-stone-300">
                        <Award size={64} className="opacity-20" />
                    </div>
                )}
            </div>

            <div className="space-y-4 pl-2">
                <span className="text-[10px] font-bold uppercase tracking-[0.4em] text-stone-400 block">{c.provider}</span>
                <h3 className="text-2xl font-bold uppercase tracking-tight text-stone-900 dark:text-white leading-tight group-hover:text-stone-600 dark:group-hover:text-stone-300 transition-colors">{c.title}</h3>
                
                <AnimatePresence>
                    {isExpanded && (
                        <motion.div 
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="overflow-hidden space-y-4 pt-2"
                        >
                            <div className="flex items-center gap-3">
                                <div className="w-8 h-[1px] bg-stone-200 dark:bg-white/10" />
                                <p className="text-[10px] text-stone-500 font-bold uppercase tracking-widest italic">Issued: {c.date}</p>
                            </div>
                            {c.verificationLink && (
                                <a href={c.verificationLink} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white bg-stone-100 dark:bg-stone-800 px-4 py-2 rounded-sm hover:opacity-80 transition-all">
                                    Verify Credential <ExternalLink size={12} />
                                </a>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>

                <div className="pt-2">
                    <button 
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="group/read flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-500 hover:text-stone-900 dark:hover:text-white border-b border-stone-200 dark:border-white/10 pb-1 transition-all"
                    >
                        {isExpanded ? 'Show Less' : 'Credential Info'} 
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
