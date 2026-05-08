import os

base_dir = "C:/Portfolio/frontend/src/pages"
comp_dir = "C:/Portfolio/frontend/src/components"

# --- UPDATE HOME.JSX ---
home_path = os.path.join(base_dir, "Home.jsx")
with open(home_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update formProfile initial state and loadProfile
content = content.replace(
    "const [formProfile, setFormProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '', email: '' });",
    "const [formProfile, setFormProfile] = useState({ fullName: '', title: '', bio: '', githubLink: '', linkedinLink: '', email: '', education: '' });"
)

# 2. Add education textarea to the edit modal
education_field = """<textarea placeholder="Education (e.g. B.Tech in ECE, 2020-2024)" value={formProfile.education || ''} onChange={e=>setFormProfile({...formProfile, education: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="3" />"""
content = content.replace(
    '<textarea placeholder="Bio" value={formProfile.bio || \'\'} onChange={e=>setFormProfile({...formProfile, bio: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="5" />',
    '<textarea placeholder="Bio" value={formProfile.bio || \'\'} onChange={e=>setFormProfile({...formProfile, bio: e.target.value})} className="w-full p-3 bg-stone-50 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded-sm" rows="5" />\n                            ' + education_field
)

# 3. Remove Technical Domains and Update Education Display
# Finding the Technical Domains section and removing it
tech_domains_block = """                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-sm bg-stone-100 dark:bg-stone-900 flex items-center justify-center text-stone-800 dark:text-stone-300 text-xl shadow-inner">⚡</span>
                            Technical Domains
                        </h3>
                        <div className="flex flex-wrap gap-3">
                            {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map((domain) => (
                                <span key={domain} className="px-4 py-2 bg-white dark:bg-slate-800/80 rounded-sm text-sm font-bold text-slate-700 dark:text-slate-200 shadow-sm border border-slate-100 dark:border-slate-700/50">{domain}</span>
                            ))}
                        </div>
                    </motion.div>"""

# Replacing the education list with dynamic content and changing grid to span full width or just centering it
education_display = """                    <motion.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5 md:col-span-2">
                        <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-3">
                            <span className="w-10 h-10 rounded-sm bg-stone-100 dark:bg-stone-900 flex items-center justify-center text-stone-800 dark:text-stone-300 text-xl shadow-inner">🎓</span>
                            Education
                        </h3>
                        <div className="text-lg text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed pl-4 border-l-2 border-stone-700 dark:border-stone-400">
                            {profile.education || "Click the edit button to add your education details."}
                        </div>
                    </motion.div>"""

# Find the education block and replace it, then remove tech domains
import re
# Remove tech domains block
content = content.replace(tech_domains_block, "")

# Find the existing education div and replace it
edu_pattern = r'<motion\.div variants={itemVariants} className="glass-card p-8 shadow-sm hover:-translate-y-2 transition-transform duration-300 border border-slate-200/50 dark:border-white/5">.*?Education.*?</ul>.*? </motion\.div>'
content = re.sub(edu_pattern, education_display, content, flags=re.DOTALL)

with open(home_path, "w", encoding="utf-8") as f:
    f.write(content)

# --- UPDATE FOOTER.JSX ---
footer_path = os.path.join(comp_dir, "Footer.jsx")
footer_content = """import { useEffect, useState } from 'react';
import { Mail, Phone } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import api from '../api/axiosConfig';

export default function Footer() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        api.get('/profile').then(res => setProfile(res.data)).catch(console.error);
    }, []);

    return (
        <footer className="mt-20 border-t border-slate-200 dark:border-white/10 bg-white/50 dark:bg-slate-950/50 backdrop-blur-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="flex flex-col md:flex-row justify-between items-center gap-8">
                    <div className="text-center md:text-left space-y-2">
                        <h3 className="text-2xl font-bold text-stone-900 dark:text-white">
                            {profile.fullName || "My Portfolio"}
                        </h3>
                        <div className="flex flex-col gap-1 text-slate-500 dark:text-slate-400 text-sm font-medium">
                            {profile.email && (
                                <a href={`mailto:${profile.email}`} className="hover:text-stone-700 dark:hover:text-stone-300 flex items-center gap-2 justify-center md:justify-start">
                                    <Mail size={14}/> {profile.email}
                                </a>
                            )}
                            <p className="flex items-center gap-2 justify-center md:justify-start">
                                <Phone size={14}/> +91 99999 99999
                            </p>
                        </div>
                    </div>
                    
                    <div className="flex space-x-8">
                        {profile.githubLink && (
                            <a href={profile.githubLink} target="_blank" rel="noreferrer" className="text-slate-500 hover:text-stone-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                                <FaGithub className="h-6 w-6" />
                            </a>
                        )}
                        {profile.linkedinLink && (
                            <a href={profile.linkedinLink} target="_blank" rel="noreferrer" className="text-slate-500 hover:text-stone-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                                <FaLinkedin className="h-6 w-6" />
                            </a>
                        )}
                    </div>
                </div>
                <div className="mt-12 pt-8 border-t border-slate-200 dark:border-white/10 text-center text-xs tracking-widest uppercase font-bold text-slate-400 dark:text-slate-500">
                    &copy; {new Date().getFullYear()} {profile.fullName || "My Portfolio"}. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
"""

with open(footer_path, "w", encoding="utf-8") as f:
    f.write(footer_content)

print("Home and Footer updated successfully")
