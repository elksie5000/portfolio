import React, { useMemo } from 'react';
import portfolioData from '../data/portfolio.json';
import PdfThumbnail from './PdfThumbnail';

const PortfolioGrid = () => {
    // Group articles by Title (Story)
    const groupedArticles = useMemo(() => {
        const groups = {};
        portfolioData.forEach(item => {
            const title = item.title.replace(/"/g, '');
            if (!groups[title]) {
                groups[title] = {
                    title: title,
                    summary: item.summary,
                    articles: []
                };
            }
            groups[title].articles.push(item);
        });
        return Object.values(groups);
    }, []);

    return (
        <section className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
            {/* Journalist Intro */}
            <div className="mb-16 space-y-6">
                <h1 className="text-3xl md:text-4xl font-bold text-text-main">
                    I spent 20 years as a journalist...
                </h1>
                <h2 className="text-xl md:text-2xl text-text-main/80">
                    Here's a few of the articles I wrote for print:
                </h2>
            </div>

            {/* Stories Grid */}
            <div className="space-y-20">
                {groupedArticles.map((group) => (
                    <div key={group.title} className="space-y-6">
                        <div className="border-l-4 border-brand-sage pl-6">
                            <h3 className="text-2xl font-bold text-text-main mb-2">{group.title}</h3>
                            <p className="text-text-main/80 leading-relaxed">
                                {group.summary}
                            </p>
                        </div>

                        {/* PDF Grid for this Story */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
                            {group.articles.map((article) => (
                                <a
                                    key={article.id}
                                    href={article.pdf_path}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="group block transition-transform duration-300 hover:-translate-y-2"
                                >
                                    {/* Thumbnail Container */}
                                    <div className="relative w-full overflow-hidden bg-gray-100 border-4 border-gray-700 shadow-sm group-hover:shadow-xl transition-all duration-300">
                                        <PdfThumbnail pdfPath={article.pdf_path} />

                                        {/* Hover Overlay */}
                                        <div className="absolute inset-0 bg-brand-sage/0 group-hover:bg-brand-sage/10 transition-colors duration-300" />
                                    </div>
                                </a>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default PortfolioGrid;
