import { motion, AnimatePresence } from 'framer-motion';
import { Download, Mail, Edit3, X, Plus, Trash2, ExternalLink, Briefcase, Award, Code, Cpu, Settings, Phone, MapPin, Trophy, GraduationCap } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import experienceImg from '../assets/experience.png';
import certImg from '../assets/certification.png';
import achImg from '../assets/achievements.png';
import eduImg from '../assets/education.png';

export default function Home() {
    const [profile, setProfile] = useState({});
    const [education, setEducationList] = useState([]);
    const [workExp, setWorkExp] = useState([]);
    const [skills, setSkills] = useState([]);
    const [certs, setCerts] = useState([]);
    const [projects, setProjects] = useState([]);
    
    const [showEdit, setShowEdit] = useState(false);
    const [showEduModal, setShowEduModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const [eduForm, setEduForm] = useState({ id: null, degree: '', institution: '', year: '', grade: '' });
    const [isAdmin, setIsAdmin] = useState(false);

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setIsAdmin(!!session);
    };

    useEffect(() => { 
        checkAdmin();
        loadData(); 
    }, []);

    // Contact workflow state
    const [contactStep, setContactStep] = useState(() => localStorage.getItem('contactRevealed') === 'true' ? 'revealed' : 'button');
    const [contactForm, setContactForm] = useState({ name: '', email: '', phoneNumber: '', content: 'Contact Request' });

    // Form state for profile
    const [formProfile, setFormProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '', email: '', phoneNumber: '' });
    const [photo, setPhoto] = useState(null);
    const [resume, setResume] = useState(null);

    const loadData = async () => {
        setLoading(true);
        try {
            const { data: pData } = await supabase.from('profiles').select('*').maybeSingle();
            if (pData) {
                const mapped = {
                    ...pData,
                    fullName: pData.full_name,
                    githubLink: pData.github_link,
                    linkedinLink: pData.linkedin_link,
                    phoneNumber: pData.phone_number
                };
                setProfile(mapped);
                setFormProfile(mapped);
            }
// ... rest of loadData ...

            const { data: eData } = await supabase.from('education').select('*').order('year', { ascending: false });
            if (eData) setEducationList(eData);

            const { count: wCount } = await supabase.from('work_experience').select('*', { count: 'exact', head: true });
            const { count: sCount } = await supabase.from('skills').select('*', { count: 'exact', head: true });
            const { count: cCount } = await supabase.from('certifications').select('*', { count: 'exact', head: true });
            const { count: prCount } = await supabase.from('projects').select('*', { count: 'exact', head: true });

            setWorkExp(new Array(wCount || 0).fill({}));
            setSkills(new Array(sCount || 0).fill({}));
            setCerts(new Array(cCount || 0).fill({}));
            setProjects(new Array(prCount || 0).fill({}));
        } catch (error) {
            console.error("Migration error:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleContactSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await supabase.from('messages').insert([{ ...contactForm, created_at: new Date() }]);
            localStorage.setItem('contactRevealed', 'true');
            setContactStep('revealed');
            window.dispatchEvent(new Event('storage'));
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSaveProfile = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            let photoUrl = profile.profile_photo_url;
            let resumeUrl = profile.resume_url;

            if (photo) {
                const fileName = `photo_${Date.now()}`;
                const { data } = await supabase.storage.from('profile-assets').upload(fileName, photo);
                if (data) photoUrl = supabase.storage.from('profile-assets').getPublicUrl(data.path).data.publicUrl;
            }

            if (resume) {
                const fileName = `resume_${Date.now()}.pdf`;
                const { data } = await supabase.storage.from('resumes').upload(fileName, resume);
                if (data) resumeUrl = supabase.storage.from('resumes').getPublicUrl(data.path).data.publicUrl;
            }

            const { error } = await supabase.from('profiles').upsert({
                id: profile.id || 1,
                full_name: formProfile.fullName,
                title: formProfile.title,
                bio: formProfile.bio,
                github_link: formProfile.githubLink,
                linkedin_link: formProfile.linkedinLink,
                email: formProfile.email,
                phone_number: formProfile.phoneNumber,
                profile_photo_url: photoUrl,
                resume_url: resumeUrl
            });

            if (!error) {
                setShowEdit(false);
                loadData();
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleSaveEdu = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            if (eduForm.id) {
                await supabase.from('education').update(eduForm).eq('id', eduForm.id);
            } else {
                const { id, ...newEdu } = eduForm;
                await supabase.from('education').insert([newEdu]);
            }
            setShowEduModal(false);
            setEduForm({ id: null, degree: '', institution: '', year: '', grade: '' });
            loadData();
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const containerVariants = { 
        hidden: { opacity: 0 }, 
        visible: { opacity: 1, transition: { staggerChildren: 0.15 } } 
    };
    const itemVariants = { 
        hidden: { y: 30, opacity: 0 }, 
        visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 80, damping: 15 } } 
    };

    // Skill categorization with safety checks
    const skillCategories = [
        { name: 'Hardware', icon: <Cpu className="text-blue-500"/>, items: (Array.isArray(skills) ? skills : []).filter(s => s.category?.toLowerCase() === 'hardware') },
        { name: 'Software', icon: <Code className="text-emerald-500"/>, items: (Array.isArray(skills) ? skills : []).filter(s => s.category?.toLowerCase() === 'software' || s.category?.toLowerCase() === 'programming languages') },
        { name: 'Tools and Technologies', icon: <Settings className="text-stone-500"/>, items: (Array.isArray(skills) ? skills : []).filter(s => !['hardware', 'software', 'programming languages'].includes(s.category?.toLowerCase() || '')) }
    ];

    return (
        <div className="flex flex-col items-center w-full pb-20 overflow-hidden">
            
            {isAdmin && (
                <button onClick={() => setShowEdit(!showEdit)} className="fixed bottom-8 right-8 z-50 bg-stone-900 hover:bg-stone-800 text-white p-4 rounded-full shadow-2xl transition-transform hover:scale-110">
                    {showEdit ? <X size={24}/> : <Edit3 size={24}/>}
                </button>
            )}

            {/* Profile Edit Modal */}
            <AnimatePresence>
                {showEdit && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60] flex items-center justify-center p-4 overflow-y-auto">
                        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-2xl w-full">
                            <h3 className="text-2xl font-bold mb-6 text-stone-900 dark:text-white border-b pb-2">Edit Profile</h3>
                            <form onSubmit={handleSaveProfile} className="space-y-4 text-left">
                                <input placeholder="Full Name" value={formProfile.fullName || ''} onChange={e=>setFormProfile({...formProfile, fullName: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                <input placeholder="Title" value={formProfile.title || ''} onChange={e=>setFormProfile({...formProfile, title: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                <textarea placeholder="Bio" value={formProfile.bio || ''} onChange={e=>setFormProfile({...formProfile, bio: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="5" />
                                <div className="grid grid-cols-2 gap-4">
                                    <input placeholder="GitHub URL" value={formProfile.githubLink || ''} onChange={e=>setFormProfile({...formProfile, githubLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                    <input placeholder="LinkedIn URL" value={formProfile.linkedinLink || ''} onChange={e=>setFormProfile({...formProfile, linkedinLink: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <input type="email" placeholder="Email" value={formProfile.email || ''} onChange={e=>setFormProfile({...formProfile, email: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                    <input placeholder="Phone Number" value={formProfile.phoneNumber || ''} onChange={e=>setFormProfile({...formProfile, phoneNumber: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                </div>
                                <div className="p-4 border border-dashed border-stone-300 dark:border-stone-700 rounded-sm">
                                    <label className="block text-sm font-bold mb-2">Profile Photo</label>
                                    <input type="file" accept="image/*" onChange={e => setPhoto(e.target.files[0])} className="w-full mb-4" />
                                    <label className="block text-sm font-bold mb-2">Resume (PDF)</label>
                                    <input type="file" accept=".pdf" onChange={e => setResume(e.target.files[0])} className="w-full" />
                                </div>
                                <div className="flex justify-end gap-4 mt-6">
                                    <button type="button" onClick={()=>setShowEdit(false)} className="px-6 py-2 font-bold text-stone-500 hover:text-stone-700 transition-colors">Cancel</button>
                                    <button type="submit" disabled={loading} className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 disabled:opacity-50 transition-colors">
                                        {loading ? 'Saving...' : 'Save'}
                                    </button>
                                </div>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            <AnimatePresence>
                {showEduModal && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60] flex items-center justify-center p-4">
                        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto">
                            <h3 className="text-2xl font-bold mb-6 text-stone-900 dark:text-white border-b pb-2">Academic Journey Manager</h3>
                            
                            <div className="space-y-6 mb-10">
                                {education.map(edu => (
                                    <div key={edu.id} className="flex justify-between items-center p-4 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm">
                                        <div>
                                            <p className="font-bold text-stone-900 dark:text-white">{edu.institution}</p>
                                            <p className="text-xs text-stone-400 uppercase tracking-widest">{edu.year} · {edu.grade}</p>
                                        </div>
                                        <div className="flex gap-2">
                                            <button onClick={() => setEduForm(edu)} className="p-2 text-stone-400 hover:text-stone-900 dark:hover:text-white transition-colors"><Edit3 size={16}/></button>
                                            <button onClick={async () => { if(window.confirm('Delete entry?')) { await api.delete(`/education/${edu.id}`); loadData(); } }} className="p-2 text-stone-400 hover:text-red-500 transition-colors"><Trash2 size={16}/></button>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <form onSubmit={handleSaveEdu} className="space-y-4 border-t pt-6">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Institution Name</label>
                                    <input placeholder="University / School" value={eduForm.institution} onChange={e=>setEduForm({...eduForm, institution: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Degree (Optional)</label>
                                    <input placeholder="e.g. B.Tech in ECE" value={eduForm.degree} onChange={e=>setEduForm({...eduForm, degree: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">Year / Duration</label>
                                        <input placeholder="e.g. 2022-2026" value={eduForm.year} onChange={e=>setEduForm({...eduForm, year: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-bold uppercase tracking-widest text-stone-400">CGPA / Percentage</label>
                                        <input placeholder="e.g. 9.2 or 85%" value={eduForm.grade} onChange={e=>setEduForm({...eduForm, grade: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                                    </div>
                                </div>
                                <div className="flex justify-end gap-4 mt-8">
                                    <button type="button" onClick={() => { setShowEduModal(false); setEduForm({ id: null, degree: '', institution: '', year: '', grade: '' }); }} className="px-6 py-2 font-bold text-stone-500">Close</button>
                                    <button type="submit" disabled={loading} className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 disabled:opacity-50 transition-colors">
                                        {eduForm.id ? 'Update Entry' : 'Add Entry'}
                                    </button>
                                </div>
                            </form>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* HERO SECTION */}
            <motion.section 
                variants={containerVariants} 
                initial="hidden" 
                whileInView="visible" 
                viewport={{ once: false }}
                className="relative min-h-screen flex flex-col items-center justify-center w-full px-4 pt-20 overflow-hidden"
            >
                {/* Decorative Background Elements */}
                <motion.div 
                    initial={{ opacity: 0, y: -50 }}
                    whileInView={{ opacity: 0.05, y: 0 }}
                    viewport={{ once: false }}
                    className="absolute left-4 md:left-8 top-0 bottom-0 select-none pointer-events-none hidden sm:flex items-center justify-center w-12"
                >
                    <span className="text-2xl md:text-3xl font-black uppercase tracking-[0.6em] whitespace-nowrap text-stone-900 dark:text-white opacity-20" style={{ writingMode: 'vertical-rl' }}>
                        Engineering · Engineering · Engineering
                    </span>
                </motion.div>
                
                <motion.div 
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 0.05, y: 0 }}
                    viewport={{ once: false }}
                    className="absolute right-4 md:right-8 top-0 bottom-0 select-none pointer-events-none hidden sm:flex items-center justify-center w-12"
                >
                    <span className="text-2xl md:text-3xl font-black uppercase tracking-[0.6em] whitespace-nowrap text-stone-900 dark:text-white opacity-20" style={{ writingMode: 'vertical-rl' }}>
                        Collaboration · Collaboration · Collaboration
                    </span>
                </motion.div>

                {/* Floating Keywords */}
                <motion.div 
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 0.15 }}
                    viewport={{ once: false }}
                    className="absolute top-[15%] left-[10%] text-xs uppercase tracking-[1em] font-bold italic hidden md:block whitespace-nowrap"
                >
                    Building
                </motion.div>
                <motion.div 
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 0.15 }}
                    viewport={{ once: false }}
                    className="absolute top-[15%] right-[10%] text-xs uppercase tracking-[1em] font-bold italic hidden md:block whitespace-nowrap"
                >
                    Innovating
                </motion.div>

                <motion.div variants={itemVariants} className="relative z-10 w-64 md:w-80 h-[400px] md:h-[450px] mb-10 overflow-hidden" style={{ WebkitMaskImage: 'linear-gradient(to bottom, black 60%, transparent 100%)', maskImage: 'linear-gradient(to bottom, black 60%, transparent 100%)' }}>
                    {profile.profile_photo_url ? (
                        <img src={profile.profile_photo_url} alt="Profile" className="w-full h-full object-cover object-top filter grayscale-[15%] contrast-[1.05]" />
                    ) : (
                        <div className="w-full h-full bg-stone-200 dark:bg-stone-800 flex items-center justify-center text-stone-400">No Photo</div>
                    )}
                </motion.div>
                
                <motion.h1 variants={itemVariants} className="relative z-10 text-4xl md:text-6xl lg:text-7xl font-bold mb-4 tracking-tight text-stone-900 dark:text-white uppercase">
                    {profile.fullName || "Your Name"}
                </motion.h1>
                
                <motion.div variants={itemVariants} className="relative z-10 text-xl md:text-2xl text-stone-600 dark:text-stone-400 italic mb-12 font-medium tracking-widest uppercase text-center">
                    {profile.title || "Electronics and Communication Engineer"}
                </motion.div>

            </motion.section>

            {/* ABOUT SECTION */}
            <motion.section variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: false, margin: "-100px" }} className="max-w-5xl w-full mx-auto px-4 py-32 border-t border-stone-200 dark:border-white/5">
                <div className="grid md:grid-cols-3 gap-12 items-start">
                    <motion.h2 variants={itemVariants} className="text-4xl md:text-6xl font-bold uppercase tracking-tighter sticky top-24">About <span className="text-stone-400">Me</span></motion.h2>
                    <motion.div variants={itemVariants} className="md:col-span-2 space-y-8">
                        <p className="text-xl md:text-2xl text-stone-700 dark:text-stone-300 leading-relaxed font-light whitespace-pre-wrap italic text-justify">
                            {profile.bio || "Crafting elegance through electronics and code."}
                        </p>
                    </motion.div>
                </div>
            </motion.section>

            <motion.section variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: false }} className="max-w-6xl w-full mx-auto px-4 py-32 border-t border-stone-200 dark:border-white/5">
                <motion.h2 variants={itemVariants} className="text-4xl md:text-6xl font-bold uppercase tracking-tighter mb-20">Editorial <span className="text-stone-400">Overview</span></motion.h2>
                
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
                    {/* Academic Journey Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        {isAdmin && (
                            <button onClick={() => setShowEduModal(true)} className="absolute top-4 right-4 z-20 p-2 bg-white/90 dark:bg-black/90 text-stone-800 dark:text-stone-200 rounded-sm shadow-xl opacity-0 group-hover:opacity-100 transition-opacity"><Edit3 size={16}/></button>
                        )}
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src={eduImg} alt="Education" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <GraduationCap className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Academic Journey</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                Highlighting a strong educational foundation and academic milestones in engineering and technology.
                            </p>
                            <a href="/education" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>

                    {/* Skills Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80" alt="Skills" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <Code className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Skills</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                Crafting sophisticated digital solutions through a mastery of hardware architecture and software engineering.
                            </p>
                            <a href="/skills" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>

                    {/* Experience Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src={experienceImg} alt="Experience" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <Briefcase className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Experience</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                A professional journey marked by innovation in electronics and communication engineering.
                            </p>
                            <a href="/experience" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>

                    {/* Projects Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80" alt="Projects" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <Cpu className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Projects</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                From complex hardware systems to elegant software applications. Dive into my technical implementations.
                            </p>
                            <a href="/projects" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>

                    {/* Certifications Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src={certImg} alt="Certifications" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <Award className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Certifications</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                Validated expertise and continuous learning in cutting-edge technologies.
                            </p>
                            <a href="/certifications" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>

                    {/* Achievements Overview */}
                    <motion.div variants={itemVariants} className="group relative overflow-hidden border border-stone-100 dark:border-white/5 hover:bg-stone-50 dark:hover:bg-white/5 transition-all duration-500 rounded-sm flex flex-col">
                        <div className="aspect-[16/9] overflow-hidden mb-6">
                            <img src={achImg} alt="Achievements" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 grayscale group-hover:grayscale-0" />
                        </div>
                        <div className="p-8 pt-0 flex-1 flex flex-col">
                            <div className="flex items-center gap-4 mb-4">
                                <div className="p-3 bg-stone-100 dark:bg-stone-800 rounded-sm group-hover:scale-110 transition-transform">
                                    <Trophy className="text-stone-900 dark:text-white" size={20} />
                                </div>
                                <h3 className="text-xl font-bold uppercase tracking-tight">Achievements</h3>
                            </div>
                            <p className="text-sm text-stone-600 dark:text-stone-400 leading-relaxed mb-8 font-light italic flex-1">
                                Honors, awards, and recognition for academic and professional excellence.
                            </p>
                            <a href="/achievements" className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.3em] text-stone-900 dark:text-white border-b border-stone-900 dark:border-white pb-1 hover:gap-4 transition-all w-fit">
                                Read More <ExternalLink size={12} />
                            </a>
                        </div>
                    </motion.div>
                </div>
            </motion.section>

            {/* CONTACT SECTION */}
            <motion.section id="contact-section" variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: false }} className="max-w-4xl w-full mx-auto px-4 pt-40 pb-20 border-t border-stone-200 dark:border-white/5 text-center">
                <motion.h2 variants={itemVariants} className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-6 leading-none">Get in <span className="text-stone-400">Touch</span></motion.h2>
                <motion.p variants={itemVariants} className="text-stone-500 dark:text-stone-400 text-lg md:text-xl font-light italic mb-16 max-w-2xl mx-auto">
                    Have a project in mind or just want to say hi? I'm always open to discussing new opportunities and technical challenges.
                </motion.p>
                
                <motion.div variants={itemVariants} className="flex flex-col items-center gap-12 w-full">
                    <motion.div variants={itemVariants} className="flex flex-col items-center gap-8">
                        <div className="p-6 bg-stone-100 dark:bg-stone-800 rounded-full text-stone-900 dark:text-white">
                            <Mail size={40} />
                        </div>
                        <div className="space-y-6">
                            <motion.div variants={itemVariants} className="space-y-1">
                                <p className="text-xs text-stone-400 uppercase tracking-[0.4em] font-bold">Email</p>
                                <a href={`mailto:${profile.email}`} className="text-2xl md:text-4xl font-bold tracking-tight hover:text-stone-500 transition-colors">{profile.email}</a>
                            </motion.div>
                            <motion.div variants={itemVariants} className="space-y-1">
                                <p className="text-xs text-stone-400 uppercase tracking-[0.4em] font-bold">Phone</p>
                                <a href={`tel:${profile.phone_number}`} className="text-2xl md:text-4xl font-bold tracking-tight hover:text-stone-500 transition-colors">{profile.phone_number}</a>
                            </motion.div>
                            <motion.div variants={itemVariants} className="space-y-1">
                                <p className="text-xs text-stone-400 uppercase tracking-[0.4em] font-bold">Location</p>
                                <div className="flex items-center justify-center gap-2 text-2xl md:text-4xl font-bold tracking-tight text-stone-900 dark:text-white">
                                    <MapPin className="text-stone-400" size={32} />
                                    <span>Hyderabad, India</span>
                                </div>
                            </motion.div>
                        </div>
                    </motion.div>
                    
                    <motion.div variants={itemVariants} className="flex flex-col items-center gap-4 mt-12">
                        <motion.div variants={itemVariants} className="flex gap-4">
                            {profile.github_link && (
                                <a href={profile.github_link} target="_blank" rel="noreferrer" className="flex items-center justify-center gap-3 w-[160px] py-4 bg-[#171717] text-white rounded-sm hover:bg-black transition-all shadow-lg">
                                    <FaGithub size={18} />
                                    <span className="text-[10px] font-bold uppercase tracking-[0.2em]">Github</span>
                                </a>
                            )}
                            {profile.linkedin_link && (
                                <a href={profile.linkedin_link} target="_blank" rel="noreferrer" className="flex items-center justify-center gap-3 w-[160px] py-4 bg-[#0077b5] text-white rounded-sm hover:bg-[#006396] transition-all shadow-lg">
                                    <FaLinkedin size={18} />
                                    <span className="text-[10px] font-bold uppercase tracking-[0.2em]">LinkedIn</span>
                                </a>
                            )}
                        </motion.div>

                        {profile.resume_url && (
                            <motion.div variants={itemVariants} className="w-full max-w-[336px]">
                                <a href={profile.resume_url} download target="_blank" rel="noreferrer" className="flex items-center justify-center gap-3 w-full py-5 bg-stone-900 dark:bg-white text-white dark:text-stone-900 rounded-sm hover:scale-105 transition-all shadow-2xl border border-stone-200 dark:border-white/10 font-bold uppercase tracking-widest text-[10px]">
                                    <Download size={18} />
                                    Download Full Resume
                                </a>
                            </motion.div>
                        )}
                    </motion.div>
            </motion.div>
            </motion.section>
        </div>
    );
}