import React, { useEffect, useState } from 'react';
import { VegaEmbed } from 'react-vega';
import { getApiBaseUrl } from '../utils/api';
import spec from '../data/donut_chart_spec.json';

const SexesDonutChart = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const baseUrl = getApiBaseUrl();
                const response = await fetch(`${baseUrl}/api/sexes/summary`);
                if (!response.ok) throw new Error('Failed to fetch data');
                const result = await response.json();

                // The donut chart expects fields "Gender", "Percentage", "Admissions"
                // Our API returns lowercase keys "gender", "percentage", "admissions"
                // We need to map them back to Capitalized keys to match the spec
                const mappedData = result.map(d => ({
                    Gender: d.gender,
                    Percentage: d.percentage,
                    Admissions: d.admissions
                }));

                setData(mappedData);
            } catch (error) {
                console.error('Error fetching sexes summary:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="w-full bg-white p-4 rounded-lg shadow-sm border border-brand-sage/20">
            <VegaEmbed
                spec={spec}
                data={{ table: data }}
                actions={false}
                className="w-full"
            />
        </div>
    );
};

export default SexesDonutChart;
