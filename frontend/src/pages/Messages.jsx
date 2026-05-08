import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { Mail, User, Phone, Trash2, Clock, CheckCircle, MessageSquare } from 'lucide-react';

export default function Messages() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isAdmin, setIsAdmin] = useState(false);

    const checkAdmin = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        if (!session) {
            window.location.href = '/admin/login';
            return;
        }
        setIsAdmin(true);
        fetchMessages();
    };

    const fetchMessages = async () => {
        setLoading(true);
        const { data } = await supabase.from('messages').select('*').order('created_at', { ascending: false });
        if (data) {
            setMessages(data.map(m => ({
                ...m,
                phoneNumber: m.phone_number
            })));
        }
        setLoading(false);
    };

    useEffect(() => {
        checkAdmin();
    }, []);

    const deleteMessage = async (id) => {
        if (window.confirm('Delete this message?')) {
            await supabase.from('messages').delete().eq('id', id);
            fetchMessages();
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
        <div className="min-h-screen pt-32 pb-20 px-4 bg-white dark:bg-stone-950">
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl mx-auto mb-20 text-center">
                <h1 className="text-5xl md:text-8xl font-bold uppercase tracking-tighter mb-6 text-stone-900 dark:text-white">
                    Client <span className="text-stone-400">Inbox</span>
                </h1>
                <p className="text-sm font-bold uppercase tracking-[0.4em] text-stone-400">Manage communication and inquiries</p>
            </motion.div>

            <motion.div variants={containerVariants} initial="hidden" animate="visible" className="max-w-4xl mx-auto space-y-6">
                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="w-12 h-12 border-4 border-stone-200 border-t-stone-900 rounded-full animate-spin"></div>
                    </div>
                ) : messages.length > 0 ? messages.map((msg, idx) => (
                    <motion.div key={idx} variants={itemVariants} className="bg-stone-50 dark:bg-stone-900/40 border border-stone-100 dark:border-white/5 p-8 rounded-sm group hover:border-stone-900 dark:hover:border-white transition-all relative">
                        <div className="absolute top-8 right-8 flex gap-4">
                             <button onClick={() => deleteMessage(msg.id)} className="text-stone-300 hover:text-red-500 transition-colors">
                                <Trash2 size={20} />
                            </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                            <div className="space-y-4">
                                <div className="flex items-center gap-3 text-stone-500 dark:text-stone-400">
                                    <User size={16} className="text-stone-300"/>
                                    <span className="text-xs font-bold uppercase tracking-widest">{msg.name}</span>
                                </div>
                                <div className="flex items-center gap-3 text-stone-500 dark:text-stone-400">
                                    <Mail size={16} className="text-stone-300"/>
                                    <span className="text-xs font-bold uppercase tracking-widest truncate">{msg.email}</span>
                                </div>
                                {msg.phoneNumber && (
                                    <div className="flex items-center gap-3 text-stone-500 dark:text-stone-400">
                                        <Phone size={16} className="text-stone-300"/>
                                        <span className="text-xs font-bold uppercase tracking-widest">{msg.phoneNumber}</span>
                                    </div>
                                )}
                            </div>
                            <div className="md:col-span-2">
                                <div className="flex items-start gap-4">
                                    <MessageSquare size={20} className="text-stone-300 mt-1 flex-shrink-0" />
                                    <p className="text-stone-800 dark:text-stone-200 leading-relaxed italic">"{msg.content}"</p>
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-between items-center pt-6 border-t border-stone-100 dark:border-white/5">
                            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-stone-400">
                                <Clock size={12}/> Received recently
                            </div>
                            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-green-500">
                                <CheckCircle size={12}/> New Inquiry
                            </div>
                        </div>
                    </motion.div>
                )) : (
                    <div className="text-center py-20 text-stone-400 italic font-medium">Your inbox is currently empty.</div>
                )}
            </motion.div>
        </div>
    );
}
