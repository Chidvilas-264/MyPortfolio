import { useEffect, useState } from 'react';
import { Mail, Phone, Download, MapPin } from 'lucide-react';
import { FaGithub, FaLinkedin } from 'react-icons/fa';
import { supabase } from '../supabaseClient';

export default function Footer() {
    const [profile, setProfile] = useState({});
    
    useEffect(() => {
        supabase.from('profiles').select('*').maybeSingle().then(({ data }) => {
            if (data) setProfile(data);
        }).catch(console.error);
    }, []);

    return (
        <footer className="mt-0 border-t border-slate-200 dark:border-white/10 bg-white/50 dark:bg-slate-950/50 backdrop-blur-md">
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
                            {profile.phone_number && (
                                <p className="flex items-center gap-2 justify-center md:justify-start">
                                    <Phone size={14}/> {profile.phone_number}
                                </p>
                            )}
                            <p className="flex items-center gap-2 justify-center md:justify-start">
                                <MapPin size={14}/> Hyderabad, India
                            </p>
                        </div>
                    </div>
                    
                    <div className="flex items-center space-x-6">
                        {profile.github_link && (
                            <a href={profile.github_link} target="_blank" rel="noreferrer" className="text-slate-500 hover:text-stone-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                                <FaGithub className="h-6 w-6" />
                            </a>
                        )}
                        {profile.linkedin_link && (
                            <a href={profile.linkedin_link} target="_blank" rel="noreferrer" className="text-slate-500 hover:text-stone-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                                <FaLinkedin className="h-6 w-6" />
                            </a>
                        )}
                        {profile.resume_url && (
                            <a href={profile.resume_url} download target="_blank" rel="noreferrer" title="Download Resume" className="text-slate-500 hover:text-stone-900 dark:text-slate-400 dark:hover:text-white transition-colors">
                                <Download className="h-6 w-6" />
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
