import React from 'react';
import WarDeadMap from './WarDeadMap';
import DataPanels from './DataPanels';
import CrimeMap from './CrimeMap';
import SexesLineChart from './SexesLineChart';
import SexesDonutChart from './SexesDonutChart';
import RegionsChart from './RegionsChart';

const Home = () => {
    return (
        <div className="max-w-4xl mx-auto px-6 py-12 space-y-16">
            {/* Hero Section */}
            <section className="space-y-6">
                <h1 className="text-4xl font-bold text-text-main leading-tight">
                    Hi, I'm David Elks. I create data-driven stories that are effective, engaging, accurate and provide actionable insights. I hope they are also human.
                </h1>
                <div className="space-y-4 text-lg text-text-main/80 max-w-2xl">
                    <p>
                        Over the course of my career I've been an award-winning business journalist writings stories about companies by interviewing people in start-ups to listed company chiefs, and digging through financial documents.
                    </p>
                    <p>
                        Now I use new tools as a data analyst such as Excel to ask questions of spreadsheets, SQL to explore databases, and Python/R to mine raw data on the internet.
                    </p>
                    <p>
                        Either way, I aim to answer the questions: who, what, where, when, why and how.
                    </p>
                    <p>
                        I collect, clean and analyse data to answer specific questions and then use charts, tables and words to visualise my insights quickly and efficiently. I've answered questions of more than 600 datasets including health, education, crime, planning - even Robbie Williams - and worked within the media, public sector and charities.
                    </p>
                    <p>
                        My experience is backed up by a <a href="https://www.keele.ac.uk/study/postgraduatestudy/postgraduatecourses/advancedcomputerscience/" className="text-brand-sage hover:text-brand-lime underline decoration-1 underline-offset-4">Advanced Computer Science MSc at Keele University</a> in which my research project was a neural network built to detect whether articles published during the 2016 US electoral campaign were real or fake.
                    </p>
                    <p>
                        In short, if there's data and a story to be found, I'll endeavour to find it.
                    </p>
                    <p>
                        Get in touch by <a href="mailto:elksie2500@gmail.com" className="text-brand-sage hover:text-brand-lime underline decoration-1 underline-offset-4">email</a>.
                    </p>
                </div>
            </section>

            {/* Projects List */}
            <section className="space-y-6">
                <h2 className="text-2xl font-bold text-text-main border-b border-brand-sage/20 pb-2">Among some of the projects I've completed:</h2>
                <ol className="list-decimal list-inside space-y-3 text-text-main/80 marker:text-brand-sage marker:font-bold">
                    <li><a href="https://github.com/elksie5000/image_resize_php" className="hover:text-brand-sage transition-colors">Resizing images on the fly using PHP REST-based API.</a></li>
                    <li><a href="https://github.com/elksie5000/tictactoe" className="hover:text-brand-sage transition-colors">Creating a simple Tic Tac Toe varient with HTML, CSS and JavaScript.</a></li>
                    <li><a href="https://github.com/elksie5000/ozone_data_analysis" className="hover:text-brand-sage transition-colors">A fairly comprehensive data analysis of information about ozone production in the U.S.</a></li>
                    <li><a href="https://github.com/elksie5000/java_book_trading_collaboration" className="hover:text-brand-sage transition-colors">Learned Java in a day to create an application designed to allow two or multiple agents to trade in books.</a></li>
                    <li><a href="https://github.com/elksie5000/friendzone" className="hover:text-brand-sage transition-colors">Friendzone. A sort of Facebook clone based in PHP, JavaScript, CSS and HTML.</a></li>
                    <li><a href="https://github.com/elksie5000/infix_to_postfix_translator" className="hover:text-brand-sage transition-colors">A Python project to convert infix mathematical expressions to postfix.</a></li>
                    <li><a href="https://github.com/elksie5000/ngrammer" className="hover:text-brand-sage transition-colors">Creating an n-gram algorithm to predict the authorship of individual. A topic close to my heart.</a></li>
                    <li><a href="https://github.com/elksie5000/pollock_demo" className="hover:text-brand-sage transition-colors">A toy demo in HTML, CSS and JavaScript to generate paint-splatter images like Damian Hirst or Jackson Pollock.</a></li>
                </ol>
            </section>

            {/* War Dead */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">War dead: Lest We Forget</h2>
                <p className="text-text-main/80">The Commonwealth War Graves Commission provides free access to the records of thousands of service personnel who have lost their lives in conflict. This project, started in 2012, allowed readers to explore a map showing the final memorial for up to 13,000 casualties from the North and South Staffordshire Regiments.</p>
                <p className="text-text-main/80">The final work involved significant effort to clean and visualise the data. By zooming in you can see larger circles, presented the memorials with the most casualties - showing the main front line of the war.</p>

                <div className="w-full h-[600px] rounded-lg overflow-hidden border border-brand-sage/20 shadow-lg mb-8">
                    <WarDeadMap />
                </div>
                <DataPanels />
            </section>

            {/* Accident Statistics */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Accident statistics</h2>
                <p className="text-text-main/80">The STAT19 dataset from the Department of Transport provides a fascinating and rich dataset of millions of traffic accidents dating back to the 1970s. I have used it to explore trends accidents over time, at particular hotspots and using technology to bring them to life.</p>
                <div className="w-full aspect-video bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        src="https://elksie5000.carto.com/viz/4d245dd8-57c9-11e5-93d4-0e018d66dc29/embed_map"
                        className="w-full h-full"
                        frameBorder="0"
                        allowFullScreen
                    ></iframe>
                </div>
            </section>

            {/* Robbie Williams */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Robbie Williams</h2>
                <p className="text-text-main/80">A very early attempt to use Python and Tableau to assess the work of Stoke-on-Trent's greatest pop export, Robbie Williams in 2014. I used Python to scrape lyrics from a website from his work - which missed out Angels. I then used NLTK (a module that does natural langauge process in python) to calculate the positive, negative sentiment of those lyrics. I then plotted the data using Tableau with X axis as time, and Y as chart position. The colour and sentiment were based on the sentiment. It is a glorious failure from my early days with Tableau.</p>
                <div className="bg-gray-100 border border-brand-sage/20 rounded p-8 text-center text-brand-sage italic">
                    [Tableau Embed: Robbie Williams Sentiment Analysis]
                    {/* Note: Tableau embeds often require script tags which React handles differently. For now, a placeholder or external link is safer unless we implement a Tableau component. */}
                </div>
            </section>

            {/* Crime Data */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Crime data</h2>
                <p className="text-text-main/80">I have made extensive use of the crime statistics released by the Home Office both to provide snapshots of crime across North Staffordshire, as well as visualising trends over time (see below for August 2014). This map has a selector so it is possible to find out what crimes happen where.</p>
                <div className="w-full h-[600px] rounded-lg overflow-hidden border border-brand-sage/20 shadow-lg">
                    <CrimeMap />
                </div>
            </section>

            {/* Health Data */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Health Data</h2>
                <p className="text-text-main/80">Analysis of hospital admissions data, exploring trends by gender and region.</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-text-main">Admissions by Gender</h3>
                        <SexesLineChart />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-text-main">Gender Split</h3>
                        <SexesDonutChart />
                    </div>
                </div>

                <div className="space-y-2 mt-6">
                    <h3 className="text-lg font-semibold text-text-main">Regional Analysis</h3>
                    <p className="text-sm text-text-main/70">Obesity-related hospital admissions across England regions.</p>
                    <RegionsChart />
                </div>
            </section>

            {/* House Prices */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">House prices</h2>
                <p className="text-text-main/80">The price-paid house prices dataset provides plenty of opportunities for plotting trends of house prices, both at national and local level, and can be combined with earnings data to consider the issue of affordability.</p>

                <div className="bg-gray-100 border border-brand-sage/20 rounded p-8 text-center text-brand-sage italic">
                    [Tableau Embed: House Price Paid Data]
                </div>

                <p className="text-text-main/80">This chart took an idea from the Telegraph newspaper about the most expensive property postcodes in the UK. This chart looks at the most affordable in North Staffordshire and South Cheshire. The legend shows the percentage of the people in the area that could afford to pay a mortgage at 4.5 times median price of homes available as compared to median earnings.</p>
                <div className="w-full aspect-video bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        src="https://elksie5000.carto.com/viz/f9d84790-d4ad-11e5-a681-0ea31932ec1d/embed_map"
                        className="w-full h-full"
                        frameBorder="0"
                        allowFullScreen
                    ></iframe>
                </div>
            </section>

            {/* Education */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Education</h2>
                <p className="text-text-main/80">Results for Key Stage 4 in 2014.</p>
                <div className="w-full aspect-video bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        src="https://elksie5000.carto.com/viz/97f0456e-c021-11e5-b7d4-0e787de82d45/embed_map"
                        className="w-full h-full"
                        frameBorder="0"
                        allowFullScreen
                    ></iframe>
                </div>
            </section>

            {/* Stoke Council Data */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Stoke-on-Trent City Council data</h2>
                <h3 className="text-xl font-bold text-text-main">Parking tickets</h3>
                <p className="text-text-main/80">A Freedom of Information request provided details of more than 100,000 parking tickets issued by Stoke-on-Trent City Council over five years. The map provided a helpful way of being able to highlight hotspots as well as trends on particular streets across the city.</p>
                <div className="w-full aspect-video bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        src="https://elksie5000.carto.com/viz/91739298-5f84-11e5-abfd-0e853d047bba/embed_map"
                        className="w-full h-full"
                        frameBorder="0"
                        allowFullScreen
                    ></iframe>
                </div>
            </section>

            {/* Mining Deaths */}
            <section className="space-y-4">
                <h2 className="text-2xl font-bold text-text-main">Mining deaths in North Staffordshire</h2>
                <p className="text-text-main/80">A retired miner compiled a list of 4,715 men who lost their lives in the pits of North Staffordshire. I cleaned the manually-entered data with reference texts to provide an insight into the changing conditions for those who spent up to 12 hours underground extracting coal to power the region's pottery and steel industries.</p>

                <div className="bg-gray-100 border border-brand-sage/20 rounded p-8 text-center text-brand-sage italic">
                    [Placeholder: /templates/mining.html]
                </div>

                <h3 className="text-xl font-bold text-text-main">A timeline of fatalities</h3>
                <div className="w-full aspect-[800/300] bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        id="datawrapper-chart-fI4B0"
                        src="https://datawrapper.dwcdn.net/fI4B0/2/"
                        scrolling="no"
                        frameBorder="0"
                        style={{ width: '100%', minWidth: '100%', height: '100%' }}
                    ></iframe>
                </div>

                <h3 className="text-xl font-bold text-text-main">How the average age has changed</h3>
                <div className="w-full aspect-[800/400] bg-gray-100 border border-brand-sage/20 rounded overflow-hidden">
                    <iframe
                        src="https://cf.datawrapper.de/r1eTq/1/"
                        width="100%"
                        height="100%"
                        scrolling="no"
                        frameBorder="0"
                    ></iframe>
                </div>
            </section>
        </div>
    );
};

export default Home;
