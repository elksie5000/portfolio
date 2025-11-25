import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => setIsOpen(!isOpen);

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-bg-base/90 backdrop-blur-sm border-b border-brand-sage/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Mobile Menu Button */}
                    <div className="flex md:hidden">
                        <button
                            onClick={toggleMenu}
                            className="text-text-main hover:text-brand-sage focus:outline-none"
                        >
                            {isOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex flex-1 justify-center">
                        <ul className="flex space-x-8 text-sm font-medium tracking-widest uppercase text-text-main">
                            <li>
                                <Link to="/work" className="hover:text-brand-sage transition-colors">[ Work ]</Link>
                            </li>
                            <li>
                                <Link to="/lab" className="hover:text-brand-sage transition-colors">[ Lab ]</Link>
                            </li>
                            <li>
                                <Link to="/baby-names" className="hover:text-brand-sage transition-colors">[ Baby Names ]</Link>
                            </li>
                            <li>
                                <Link to="/" className="hover:text-brand-sage transition-colors">[ About ]</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Mobile Navigation Menu */}
            {isOpen && (
                <div className="md:hidden bg-bg-base border-b border-brand-sage/10">
                    <ul className="px-2 pt-2 pb-3 space-y-1 sm:px-3 text-center text-sm font-medium tracking-widest uppercase text-text-main">
                        <li>
                            <Link
                                to="/work"
                                className="block px-3 py-2 rounded-md hover:text-brand-sage hover:bg-brand-sage/10 transition-colors"
                                onClick={toggleMenu}
                            >
                                [ Work ]
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/lab"
                                className="block px-3 py-2 rounded-md hover:text-brand-sage hover:bg-brand-sage/10 transition-colors"
                                onClick={toggleMenu}
                            >
                                [ Lab ]
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/baby-names"
                                className="block px-3 py-2 rounded-md hover:text-brand-sage hover:bg-brand-sage/10 transition-colors"
                                onClick={toggleMenu}
                            >
                                [ Baby Names ]
                            </Link>
                        </li>
                        <li>
                            <Link
                                to="/"
                                className="block px-3 py-2 rounded-md hover:text-brand-sage hover:bg-brand-sage/10 transition-colors"
                                onClick={toggleMenu}
                            >
                                [ About ]
                            </Link>
                        </li>
                    </ul>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
