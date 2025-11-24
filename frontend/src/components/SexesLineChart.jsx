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

    // Inject data directly into the spec to avoid potential react-vega data prop issues
    const specWithData = {
        ...spec,
        data: { values: data }
    };

    console.log("Vega-Lite spec with data:", specWithData);
    console.log("Data being passed:", data);

    if (data.length === 0) {
        return <div className="p-4">Loading data...</div>;
    }

    return (
        <div className="w-full bg-white p-4 rounded-lg shadow-sm border border-brand-sage/20">
            <VegaEmbed
                spec={specWithData}
                actions={false}
                className="w-full"
            />
            {/* Debug info */}
            <div className="text-xs text-gray-400 mt-2">
                Loaded {data.length} records.
            </div>
        </div>
    );
};

export default SexesLineChart;
