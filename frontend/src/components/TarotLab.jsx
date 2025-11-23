import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { getApiBaseUrl } from '../utils/api';

const TarotLab = () => {
    const [question, setQuestion] = useState('');
    const [isFlipped, setIsFlipped] = useState(false);
    const [answer, setAnswer] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        setLoading(true);
        try {
            const response = await fetch(`${getApiBaseUrl()}/api/submit-question`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });
            const data = await response.json();
            setAnswer(data.answer);
            setIsFlipped(true);
        } catch (error) {
            console.error('Error:', error);
            setAnswer("Error");
            setIsFlipped(true);
        } finally {
            setLoading(false);
        }
    };

    const resetCard = () => {
        setIsFlipped(false);
        setQuestion('');
        setAnswer(null);
    };

    return (
        <section id="lab" className="min-h-screen flex flex-col items-center justify-center bg-bg-base p-8 relative overflow-hidden">
            <div className="absolute inset-0 pointer-events-none opacity-5">
                {/* Optional background texture */}
            </div>

            <div className="z-10 w-full flex flex-col items-center">
                <h2 className="text-3xl font-bold text-text-main mb-12 text-center">The Lab</h2>

                <div className="perspective-1000 w-full max-w-sm aspect-[3/4] relative" style={{ perspective: '1000px' }}>
                    <motion.div
                        className="w-full h-full relative preserve-3d"
                        style={{ transformStyle: 'preserve-3d' }}
                        animate={{ rotateY: isFlipped ? 180 : 0 }}
                        transition={{ duration: 0.8, type: "spring", stiffness: 200, damping: 20 }}
                    >
                        {/* Front of Card (Input) */}
                        <div
                            className="absolute inset-0 backface-hidden bg-bg-base border-2 border-brand-sage rounded-xl shadow-2xl flex flex-col items-center justify-center p-6 sm:p-12"
                            style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}
                        >
                            <div className="w-full text-center">
                                <h3 className="text-xl sm:text-2xl font-bold text-text-main mb-8 sm:mb-12">Consult the Data</h3>
                                <form onSubmit={handleSubmit} className="flex flex-col items-center w-full">
                                    <input
                                        type="text"
                                        value={question}
                                        onChange={(e) => setQuestion(e.target.value)}
                                        placeholder="What is your question?"
                                        className="w-full bg-transparent border-b-2 border-brand-sage text-center text-lg sm:text-xl py-2 text-text-main placeholder-brand-sage/50 focus:outline-none focus:border-brand-lime transition-colors"
                                        disabled={loading}
                                    />
                                    <button
                                        type="submit"
                                        disabled={loading || !question}
                                        className="mt-8 sm:mt-12 bg-brand-sage text-white px-6 sm:px-8 py-2 sm:py-3 rounded-full hover:bg-brand-lime hover:text-text-main transition-all uppercase tracking-widest font-bold text-xs sm:text-sm shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {loading ? 'Processing...' : 'Consult'}
                                    </button>
                                </form>
                            </div>
                        </div>

                        {/* Back of Card (Answer) */}
                        <div
                            className="absolute inset-0 backface-hidden bg-bg-base border-2 border-brand-sage rounded-xl shadow-2xl flex flex-col items-center justify-center p-6 sm:p-12 rotate-y-180"
                            style={{
                                transform: 'rotateY(180deg)',
                                backfaceVisibility: 'hidden',
                                WebkitBackfaceVisibility: 'hidden'
                            }}
                        >
                            <div className="text-center">
                                <p className="text-brand-sage text-xs sm:text-sm uppercase tracking-widest mb-4 sm:mb-6">The Data Says</p>
                                <h3 className="text-4xl sm:text-5xl font-bold text-text-main mb-8 sm:mb-12">{answer}</h3>
                                <button
                                    onClick={resetCard}
                                    className="px-4 sm:px-6 py-2 border border-brand-sage text-brand-sage hover:bg-brand-sage hover:text-white transition-colors text-xs sm:text-sm uppercase tracking-wider rounded-full"
                                >
                                    Ask Another
                                </button>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
};

export default TarotLab;
