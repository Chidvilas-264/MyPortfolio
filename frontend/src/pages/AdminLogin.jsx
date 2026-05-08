import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';

export default function AdminLogin() {
    const [credentials, setCredentials] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const { data, error: authError } = await supabase.auth.signInWithPassword({
                email: credentials.email,
                password: credentials.password,
            });
            
            if (authError) throw authError;
            
            if (data.session) {
                navigate('/');
            }
        } catch (err) {
            setError(err.message || 'Login failed');
        }
    };

    return (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-center items-center h-[60vh]">
            <div className="glass-card p-8 w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6 text-center text-white">Admin Login</h2>
                <form onSubmit={handleLogin} className="space-y-4">
                    <div>
                        <input type="email" placeholder="Email Address" value={credentials.email} onChange={e => setCredentials({...credentials, email: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white" required />
                    </div>
                    <div>
                        <input type="password" placeholder="Password" value={credentials.password} onChange={e => setCredentials({...credentials, password: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white" />
                    </div>
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button type="submit" className="w-full bg-stone-900 hover:bg-stone-800 text-white dark:bg-stone-100 dark:text-stone-900 dark:hover:bg-stone-300 font-bold py-2 rounded">Login</button>
                </form>
            </div>
        </motion.div>
    );
}