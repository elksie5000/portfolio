import React, { useEffect, useState } from 'react';
import { VegaEmbed } from 'react-vega';
import { getApiBaseUrl } from '../utils/api';
import spec from '../data/line_chart_spec.json';

const SexesLineChart = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const baseUrl = getApiBaseUrl();
                const response = await fetch(`${baseUrl}/api/sexes/time-series`);
                if (!response.ok) throw new Error('Failed to fetch data');
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching sexes time series:', error);
            }
        };
        fetchData();
    }, []);

    // Inject data into the spec
    // The spec expects data to be in a specific format or name.
    // We can pass data via the `data` prop to VegaEmbed which maps { name: values }

    // The extracted spec likely has "data": { "name": "table" } or similar if I cleaned it right.
    // Let's check the spec content or just force it.

    // If the spec has a hardcoded data name, we need to match it.
    // My extractor set "data": {"name": "table"}

    // Split the hconcat spec into two separate specs for vertical stacking
    // This fits better in the grid column layout
    const chart1Spec = {
        ...spec,
        hconcat: undefined, // Remove hconcat
        ...spec.hconcat[0], // Merge first chart props
        data: { values: data },
        width: "container",
        height: 300,
        config: spec.config // Preserve config
    };

    const chart2Spec = {
        ...spec,
        hconcat: undefined,
        ...spec.hconcat[1], // Merge second chart props
        data: { values: data },
        width: "container",
        height: 300,
        config: spec.config
    };

    if (data.length === 0) {
        return <div className="p-4">Loading data...</div>;
    }

    return (
        <div className="w-full bg-white p-4 rounded-lg shadow-sm border border-brand-sage/20 space-y-8">
            <div className="w-full">
                <VegaEmbed
                    spec={chart1Spec}
                    actions={false}
                    className="w-full"
                />
            </div>
            <div className="w-full border-t border-brand-sage/10 pt-8">
                <VegaEmbed
                    spec={chart2Spec}
                    actions={false}
                    className="w-full"
                />
            </div>
            {/* Debug info */}
            <div className="text-xs text-gray-400 mt-2">
                Loaded {data.length} records.
            </div>
        </div>
    );
};

export default SexesLineChart;
