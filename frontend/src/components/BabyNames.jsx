import React, { useState, useEffect, useMemo } from 'react';
import { VegaEmbed } from 'react-vega';
import { getApiBaseUrl } from '../utils/api';
import { debounce } from 'lodash';

const BabyNames = () => {
    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [selectedNames, setSelectedNames] = useState([]);
    const [chartData, setChartData] = useState([]);
    const [metric, setMetric] = useState('count'); // 'count' or 'rank'
    const [loading, setLoading] = useState(false);

    // Debounced search
    const debouncedSearch = useMemo(
        () => debounce(async (q) => {
            if (q.length < 2) {
                setSearchResults([]);
                return;
            }
            try {
                const baseUrl = getApiBaseUrl();
                const res = await fetch(`${baseUrl}/api/baby-names/search?query=${q}`);
                if (res.ok) {
                    const data = await res.json();
                    setSearchResults(data);
                }
            } catch (err) {
                console.error("Search error:", err);
            }
        }, 300),
        []
    );

    useEffect(() => {
        debouncedSearch(query);
        return () => debouncedSearch.cancel();
    }, [query, debouncedSearch]);

    // Fetch trend data when selectedNames changes
    useEffect(() => {
        const fetchData = async () => {
            if (selectedNames.length === 0) {
                setChartData([]);
                return;
            }
            setLoading(true);
            try {
                const baseUrl = getApiBaseUrl();
                const namesParam = selectedNames.map(n => n).join(',');
                const res = await fetch(`${baseUrl}/api/baby-names/trends?names=${namesParam}`);
                if (res.ok) {
                    const data = await res.json();
                    // Process data to add a display name with sex if needed
                    // For now, just use name.
                    // If we want to distinguish sex, we might need to handle that in the selection or post-processing.
                    // The API returns all records for the name.
                    // Let's create a "Label" field: "Name (Sex)"
                    const processed = data.map(d => ({
                        ...d,
                        label: `${d.name} (${d.sex})`
                    }));
                    setChartData(processed);
                }
            } catch (err) {
                console.error("Fetch trends error:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [selectedNames]);

    const addName = (name) => {
        if (selectedNames.length >= 10) return;
        if (!selectedNames.includes(name)) {
            setSelectedNames([...selectedNames, name]);
        }
        setQuery('');
        setSearchResults([]);
    };

    const removeName = (name) => {
        setSelectedNames(selectedNames.filter(n => n !== name));
    };

    // Vega-Lite Spec
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": "container",
        "height": 400,
        "data": { "values": chartData },
        "mark": { "type": "line", "point": true },
        "encoding": {
            "x": { "field": "year", "type": "ordinal", "title": "Year" },
            "y": {
                "field": metric,
                "type": "quantitative",
                "title": metric === 'count' ? "Count" : "Rank",
                "scale": metric === 'rank' ? { "reverse": true } : {}
            },
            "color": { "field": "label", "type": "nominal", "title": "Name" },
            "tooltip": [
                { "field": "name", "title": "Name" },
                { "field": "sex", "title": "Sex" },
                { "field": "year", "title": "Year" },
                { "field": metric, "title": metric === 'count' ? "Count" : "Rank" }
            ]
        }
    };

    return (
        <div className="space-y-8">
            <header className="space-y-4">
                <h1 className="text-4xl font-bold text-text-main">Baby Name Trends</h1>
                <p className="text-text-main/80 max-w-2xl">
                    Explore the popularity of baby names over time. Search for a name to see its rank or count history.
                    Compare up to 10 names.
                </p>
            </header>

            <div className="bg-white p-6 rounded-lg shadow-sm border border-brand-sage/20 space-y-6">
                {/* Controls */}
                <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
                    <div className="relative w-full md:w-96">
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Search for a name..."
                            className="w-full px-4 py-2 border border-brand-sage/30 rounded focus:outline-none focus:border-brand-sage focus:ring-1 focus:ring-brand-sage"
                        />
                        {searchResults.length > 0 && (
                            <ul className="absolute z-10 w-full bg-white border border-brand-sage/20 rounded-b shadow-lg mt-1 max-h-60 overflow-y-auto">
                                {searchResults.map((name) => (
                                    <li
                                        key={name}
                                        onClick={() => addName(name)}
                                        className="px-4 py-2 hover:bg-brand-sage/10 cursor-pointer"
                                    >
                                        {name}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>

                    <div className="flex items-center space-x-4">
                        <span className="text-sm font-medium text-text-main">Metric:</span>
                        <div className="flex bg-gray-100 rounded p-1">
                            <button
                                onClick={() => setMetric('count')}
                                className={`px-4 py-1 rounded text-sm font-medium transition-colors ${metric === 'count' ? 'bg-white shadow text-brand-sage' : 'text-gray-500 hover:text-gray-700'
                                    }`}
                            >
                                Count
                            </button>
                            <button
                                onClick={() => setMetric('rank')}
                                className={`px-4 py-1 rounded text-sm font-medium transition-colors ${metric === 'rank' ? 'bg-white shadow text-brand-sage' : 'text-gray-500 hover:text-gray-700'
                                    }`}
                            >
                                Rank
                            </button>
                        </div>
                    </div>
                </div>

                {/* Selected Names Tags */}
                <div className="flex flex-wrap gap-2">
                    {selectedNames.map(name => (
                        <span key={name} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-brand-sage/10 text-brand-sage">
                            {name}
                            <button
                                onClick={() => removeName(name)}
                                className="ml-2 hover:text-brand-lime focus:outline-none"
                            >
                                ×
                            </button>
                        </span>
                    ))}
                    {selectedNames.length === 0 && (
                        <span className="text-sm text-gray-400 italic">No names selected.</span>
                    )}
                </div>

                {/* Chart */}
                <div className="w-full min-h-[400px]">
                    {loading ? (
                        <div className="flex items-center justify-center h-full text-gray-400">Loading data...</div>
                    ) : selectedNames.length > 0 ? (
                        <VegaEmbed spec={spec} actions={false} className="w-full" />
                    ) : (
                        <div className="flex items-center justify-center h-full text-gray-300 border-2 border-dashed border-gray-200 rounded">
                            Select a name to view trends
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default BabyNames;
