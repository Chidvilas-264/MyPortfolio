import os

base_dir = "C:/Portfolio/frontend/src/pages"

# --- UPDATE HOME.JSX FOR REUSABLE EDUCATION ---
home_path = os.path.join(base_dir, "Home.jsx")
with open(home_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Education state and handlers
new_imports = "import { Download, Mail, Edit3, X, Plus, Trash2 } from 'lucide-react';"
content = content.replace("import { Download, Mail, Edit3, X } from 'lucide-react';", new_imports)

state_additions = """    const [education, setEducationList] = useState([]);
    const [showEduModal, setShowEduModal] = useState(false);
    const [eduForm, setEduForm] = useState({ id: null, degree: '', institution: '', year: '', grade: '' });

    const loadEducation = () => {
        api.get('/education').then(res => setEducationList(res.data)).catch(console.error);
    };"""

content = content.replace("const [resume, setResume] = useState(null);", "const [resume, setResume] = useState(null);\n" + state_additions)
content = content.replace("useEffect(() => { loadProfile(); }, []);", "useEffect(() => { loadProfile(); loadEducation(); }, []);")

edu_handlers = """    const handleSaveEdu = async (e) => {
        e.preventDefault();
        await api.post('/education', eduForm);
        setShowEduModal(false);
        setEduForm({ id: null, degree: '', institution: '', year: '', grade: '' });
        loadEducation();
    };

    const deleteEdu = async (id) => {
        if(window.confirm('Delete this education entry?')) {
            await api.delete(`/education/${id}`);
            loadEducation();
        }
    };"""

content = content.replace("loadProfile();\n    };", "loadProfile();\n    };\n" + edu_handlers)

# 2. Add Education Modal
edu_modal = """            {showEduModal && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white dark:bg-stone-900 p-8 rounded-sm shadow-2xl max-w-sm w-full">
                        <div className="flex justify-between items-center mb-6 border-b pb-2">
                            <h3 className="text-2xl font-bold text-stone-900 dark:text-white">{eduForm.id ? 'Edit' : 'Add'} Education</h3>
                            <button onClick={() => setShowEduModal(false)} className="text-stone-500 hover:text-stone-800"><X/></button>
                        </div>
                        <form onSubmit={handleSaveEdu} className="space-y-4 text-left">
                            <input placeholder="Degree (e.g. 10th Standard)" value={eduForm.degree} onChange={e=>setEduForm({...eduForm, degree: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <input placeholder="Institution" value={eduForm.institution} onChange={e=>setEduForm({...eduForm, institution: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                            <div className="grid grid-cols-2 gap-4">
                                <input placeholder="Year" value={eduForm.year} onChange={e=>setEduForm({...eduForm, year: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" required/>
                                <input placeholder="Grade/GPA" value={eduForm.grade} onChange={e=>setEduForm({...eduForm, grade: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" />
                            </div>
                            <button type="submit" className="bg-stone-900 text-white px-8 py-2 font-bold rounded-sm hover:bg-stone-800 w-full tracking-widest uppercase text-xs">Save</button>
                        </form>
                    </div>
                </div>
            )}"""

content = content.replace("setShowEdit(!showEdit)}", "setShowEdit(!showEdit); setShowEduModal(false);}")
content = content.replace("{showEdit && (", edu_modal + "\n            {showEdit && (")

# 3. Update Education Display Section
new_edu_display = """                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5 md:col-span-2 relative">
                        <div className="flex justify-between items-center mb-10">
                            <h3 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
                                <span className="w-10 h-10 rounded-sm bg-stone-100 dark:bg-stone-900 flex items-center justify-center text-stone-800 dark:text-stone-300 text-xl shadow-inner">🎓</span>
                                Education
                            </h3>
                            {isAdmin && (
                                <button onClick={() => {setEduForm({ id: null, degree: '', institution: '', year: '', grade: '' }); setShowEduModal(true);}} className="p-2 bg-stone-900 text-white rounded-full hover:scale-110 transition-transform">
                                    <Plus size={18}/>
                                </button>
                            )}
                        </div>
                        
                        <div className="space-y-8">
                            {education.length > 0 ? education.map((edu) => (
                                <div key={edu.id} className="relative pl-8 border-l-2 border-stone-200 dark:border-stone-800 group">
                                    <div className="absolute -left-[9px] top-0 w-4 h-4 bg-stone-700 rounded-full border-4 border-white dark:border-stone-900" />
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <h4 className="text-xl font-bold text-slate-800 dark:text-white">{edu.degree}</h4>
                                            <p className="text-stone-600 dark:text-stone-400 font-medium">{edu.institution}</p>
                                            <div className="flex gap-4 mt-1 text-sm font-bold uppercase tracking-wider text-stone-500">
                                                <span>{edu.year}</span>
                                                {edu.grade && <span className="text-stone-700 dark:text-stone-300">Grade: {edu.grade}</span>}
                                            </div>
                                        </div>
                                        {isAdmin && (
                                            <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <button onClick={() => {setEduForm(edu); setShowEduModal(true);}} className="p-1.5 text-stone-600 hover:text-stone-900"><Edit3 size={16}/></button>
                                                <button onClick={() => deleteEdu(edu.id)} className="p-1.5 text-red-500 hover:text-red-700"><Trash2 size={16}/></button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )) : (
                                <p className="text-slate-500 italic">No education entries added yet.</p>
                            )}
                        </div>
                    </motion.div>"""

# Using re to find the previous dynamic education block and replace it
import re
pattern = r'<motion\.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5 md:col-span-2">.*?Education.*?{profile\.education ||.*? </motion\.div>'
content = re.sub(pattern, new_edu_display, content, flags=re.DOTALL)

# Cleanup the profile.education from edit modal since it's now separate
content = content.replace('education: \'\'', '')
content = content.replace('<textarea placeholder="Education (e.g. B.Tech in ECE, 2020-2024)" value={formProfile.education || \'\'} onChange={e=>setFormProfile({...formProfile, education: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="3" />', '')

with open(home_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Education CMS implemented on Home page")
