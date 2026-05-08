import { motion } from 'framer-motion';
import { useState } from 'react';
import { supabase } from '../supabaseClient';

export default function Contact() {
    const [formData, setFormData] = useState({ name: '', email: '', content: '' });
    const [status, setStatus] = useState('');
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await supabase.from('messages').insert([{ ...formData, created_at: new Date() }]);
            setStatus('success');
            setFormData({ name: '', email: '', content: '' });
        } catch(err) {
            setStatus('error');
        }
    };
    return (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-xl mx-auto">
            <div className="text-center mb-10">
                <h2 className="text-4xl font-bold text-slate-800 dark:text-white">Let's <span className="text-stone-800 dark:text-stone-300">Connect</span></h2>
                <p className="text-slate-500 dark:text-slate-400 mt-2">Have a project in mind or want to hire me? Send a message!</p>
            </div>
            <div className="glass-card p-8 md:p-10 shadow-2xl shadow-stone-700/10">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Name</label>
                        <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-sm px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-stone-700 transition-shadow" placeholder="John Doe" />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Email</label>
                        <input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-sm px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-stone-700 transition-shadow" placeholder="john@example.com" />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Message</label>
                        <textarea rows="5" value={formData.content} onChange={e => setFormData({...formData, content: e.target.value})} required className="w-full bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-sm px-4 py-3 text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-stone-700 transition-shadow resize-none" placeholder="How can I help you?"></textarea>
                    </div>
                    <button type="submit" className="w-full bg-gradient-to-r from-stone-800 to-stone-800 hover:from-stone-700 hover:to-stone-700 text-white font-bold py-4 rounded-sm shadow-lg shadow-stone-700/30 transition-all hover:-translate-y-1">Send Message</button>
                    {status === 'success' && <div className="p-4 bg-stone-50 dark:bg-stone-700/10 border border-emerald-200 dark:border-stone-700/20 text-stone-800 dark:text-stone-300 rounded-sm text-center font-medium">Message sent successfully! I'll get back to you soon.</div>}
                    {status === 'error' && <div className="p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 text-red-600 dark:text-red-400 rounded-sm text-center font-medium">Failed to send message. Please try again.</div>}
                </form>
            </div>
        </motion.div>
    );
}