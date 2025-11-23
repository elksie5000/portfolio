import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import PortfolioGrid from './components/PortfolioGrid';
import TarotLab from './components/TarotLab';
import Home from './components/Home';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-bg-base text-text-main font-sans selection:bg-brand-lime selection:text-text-main">
        <Navbar />
        <main className="pt-20 w-full max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/work" element={<PortfolioGrid />} />
            <Route path="/lab" element={<TarotLab />} />
            <Route path="/about" element={<Home />} />
          </Routes>
        </main>

        <footer className="py-8 text-center text-sm text-brand-sage">
          <p>&copy; {new Date().getFullYear()} David Elks. Botanical Data.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
