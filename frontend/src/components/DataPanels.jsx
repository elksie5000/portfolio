import React from 'react';
import { VegaEmbed } from 'react-vega';
import panelsData from '../data/war_dead_panels.json';

const DataPanels = () => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full">
            {panelsData.map((spec, index) => (
                <div
                    key={index}
                    className={`
            bg-bg-base border border-brand-sage/20 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow
            ${index === 0 ? 'md:col-span-2 lg:col-span-3' : ''} /* Make the first chart (Timeline) full width */
          `}
                >
                    <div className="w-full h-full min-h-[300px]">
                        <VegaEmbed spec={spec} className="w-full" />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default DataPanels;
