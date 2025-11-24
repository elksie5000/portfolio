import React, { useEffect, useState } from 'react';
import { VegaEmbed } from 'react-vega';
import { getApiBaseUrl } from '../utils/api';
import spec from '../data/regions_chart_spec.json';

const RegionsChart = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const baseUrl = getApiBaseUrl();
                const response = await fetch(`${baseUrl}/api/regions/time-series`);
                if (!response.ok) throw new Error('Failed to fetch data');
                const result = await response.json();

                // Map keys to match spec expectations
                // Spec uses: "region", "year", "adm_per_100_000_all", "Region" (for legend/filter?)
                // Let's check the spec again or just map everything.
                // The spec likely uses "region" (lowercase) and "Region" (Capitalized) for different things or just one.
                // In the original HTML data: "region", "Region", "major_region", "adm_per_100_000_all"

                const mappedData = result.map(d => ({
                    ...d,
                    adm_per_100_000_all: d.adm_per_100k,
                    Region: d.major_region, // The dropdown likely filters by major region which was called "Region" in dataset
                    region: d.region
                }));

                setData(mappedData);
            } catch (error) {
                console.error('Error fetching regions data:', error);
            }
        };
        fetchData();
    }, []);

    const specWithData = {
        ...spec,
        data: { values: data }
    };

    if (data.length === 0) {
        return <div className="p-4">Loading data...</div>;
    }

    return (
        <div className="w-full bg-white p-4 rounded-lg shadow-sm border border-brand-sage/20 overflow-hidden">
            <VegaEmbed
                spec={specWithData}
                actions={false}
                className="w-full"
            />
            <div className="text-xs text-gray-400 mt-2">
                Loaded {data.length} records.
            </div>
        </div>
    );
};

export default RegionsChart;
