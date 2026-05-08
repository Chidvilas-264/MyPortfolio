import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';

export default function About() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        supabase.from('profiles').select('*').maybeSingle().then(({ data }) => {
            if (data) setProfile(data);
        }).catch(console.error);
    }, []);

    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-4xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-12 text-center text-slate-800 dark:text-white">About <span className="text-stone-800 dark:text-stone-300">Me</span></h2>
            <div className="glass-card p-8 md:p-10 mb-10 border-t-4 border-t-stone-700">
                <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">{profile.bio || "Write something about yourself here."}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="glass-card p-8">
                    <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-2">
                        <span className="w-8 h-8 rounded bg-stone-100 dark:bg-emerald-900/50 flex items-center justify-center text-stone-800 dark:text-stone-300 text-lg">🎓</span>
                        Education
                    </h3>
                    <ul className="space-y-6">
                        <li className="relative pl-6 before:absolute before:left-0 before:top-2 before:w-2 before:h-2 before:bg-stone-700 before:rounded-full after:absolute after:left-[3px] after:top-4 after:w-0.5 after:h-full after:bg-slate-200 dark:after:bg-slate-800">
                            <h4 className="font-bold text-slate-800 dark:text-white text-lg">B.Tech in Electronics & Communication</h4>
                            <p className="text-sm font-medium text-stone-800 dark:text-stone-300 mt-1">2020 - 2024</p>
                        </li>
                    </ul>
                </div>
                <div className="glass-card p-8">
                    <h3 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white flex items-center gap-2">
                        <span className="w-8 h-8 rounded bg-stone-100 dark:bg-teal-900/50 flex items-center justify-center text-stone-800 dark:text-stone-300 text-lg">⚡</span>
                        Technical Domains
                    </h3>
                    <div className="flex flex-wrap gap-2.5">
                        {['FPGA Development', 'Embedded Systems', 'Verilog', 'Full Stack', 'Signal Processing'].map(domain => (
                            <span key={domain} className="px-4 py-2 bg-slate-100 dark:bg-slate-800 rounded-sm text-sm font-medium text-slate-700 dark:text-slate-300 shadow-sm border border-slate-200 dark:border-slate-700">{domain}</span>
                        ))}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}