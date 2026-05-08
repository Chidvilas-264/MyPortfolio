import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Menu, X, Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';
import { supabase } from '../supabaseClient';

const Navbar = ({ isDark, toggleTheme }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        const checkAuth = async () => {
            const { data: { session } } = await supabase.auth.getSession();
            setIsAdmin(!!session);
        };
        checkAuth();
        
        const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
            setIsAdmin(!!session);
        });

        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        
        return () => {
            window.removeEventListener('scroll', handleScroll);
            subscription.unsubscribe();
        };
    }, []);

    const links = [
        { name: 'Skills', path: '/skills' },
        { name: 'Experience', path: '/experience' },
        { name: 'Projects', path: '/projects' },
        { name: 'Certifications', path: '/certifications' },
        { name: 'Achievements', path: '/achievements' }
    ];

    const handleLogout = async () => {
        await supabase.auth.signOut();
        window.location.href = '/';
    };
    return (
        <nav className={`fixed w-full top-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-200 dark:border-white/10 shadow-sm' : 'bg-transparent py-2'}`}>
            <div className="max-w-full mx-auto px-4 md:px-8">
                <div className="flex items-center justify-between h-16">
                    <Link to="/" onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})} className="text-2xl font-bold tracking-tight text-stone-900 dark:text-white hover:opacity-80 transition-opacity">
                        My Portfolio
                    </Link>
                    <div className="hidden md:flex items-center space-x-1">
                        {links.map(link => (
                            <Link key={link.name} to={link.path} className="px-3 py-2 rounded-sm text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-stone-800 dark:hover:text-stone-300 hover:bg-slate-100 dark:hover:bg-white/5 transition-all">
                                {link.name}
                            </Link>
                        ))}
                        <div className="pl-4 ml-2 border-l border-slate-200 dark:border-slate-700">
                            <button onClick={toggleTheme} className="p-2 rounded-full text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-white/10 transition-colors">
                                {isDark ? <Sun size={20} /> : <Moon size={20} />}
                            </button>
                            {isAdmin && (
                                <button onClick={handleLogout} className="ml-2 px-3 py-1.5 text-xs font-bold tracking-widest uppercase bg-stone-900 text-white hover:bg-stone-800 rounded-sm">
                                    Logout
                                </button>
                            )}
                        </div>
                    </div>
                    <div className="md:hidden flex items-center gap-2">
                        <button onClick={toggleTheme} className="p-2 text-slate-500 dark:text-slate-400">
                            {isDark ? <Sun size={20} /> : <Moon size={20} />}
                        </button>
                        <button onClick={() => setIsOpen(!isOpen)} className="text-slate-600 dark:text-slate-300">
                            {isOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>
                </div>
            </div>
            {isOpen && (
                <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="md:hidden absolute w-full bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-white/10 shadow-xl">
                    <div className="px-4 py-4 space-y-1">
                        {links.map(link => (
                            <Link key={link.name} to={link.path} onClick={() => setIsOpen(false)} className="block px-4 py-3 rounded-sm text-base font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5">
                                {link.name}
                            </Link>
                        ))}
                    </div>
                </motion.div>
            )}
        </nav>
    );
};
export default Navbar;
