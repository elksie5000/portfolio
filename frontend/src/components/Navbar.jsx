import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 flex justify-center py-6 bg-bg-base/90 backdrop-blur-sm border-b border-brand-sage/10">
            <ul className="flex space-x-8 text-sm font-medium tracking-widest uppercase text-text-main">
                <li>
                    <Link to="/work" className="hover:text-brand-sage transition-colors">[ Work ]</Link>
                </li>
                <li>
                    <Link to="/lab" className="hover:text-brand-sage transition-colors">[ Lab ]</Link>
                </li>
                <li>
                    <Link to="/" className="hover:text-brand-sage transition-colors">[ About ]</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
