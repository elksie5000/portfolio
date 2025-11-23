import React, { useEffect, useState, useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { getApiBaseUrl } from '../utils/api';

const CrimeMap = () => {
    const [crimeData, setCrimeData] = useState([]);
    const [selectedCrime, setSelectedCrime] = useState('All');

    // Center based on the Folium map: [52.814172, -2.079479]
    const center = [52.814172, -2.079479];
    const zoom = 9;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const baseUrl = getApiBaseUrl();
                const response = await fetch(`${baseUrl}/api/crime/all`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setCrimeData(data);
            } catch (error) {
                console.error('Error fetching crime data:', error);
            }
        };

        fetchData();
    }, []);

    // Extract unique crime types for the selector
    const crimeTypes = useMemo(() => {
        const types = new Set(crimeData.map(d => d.crime_type));
        return ['All', ...Array.from(types).sort()];
    }, [crimeData]);

    // Filter data based on selection
    const filteredData = useMemo(() => {
        if (selectedCrime === 'All') return crimeData;
        return crimeData.filter(d => d.crime_type === selectedCrime);
    }, [crimeData, selectedCrime]);

    return (
        <div className="w-full h-full min-h-[600px] bg-bg-base relative z-0 group">
            {/* Map Controls - Absolute positioned on top */}
            <div className="absolute top-4 right-4 z-[1000] bg-white/90 backdrop-blur-sm p-4 rounded-lg shadow-lg border border-brand-sage/20 max-w-xs">
                <label htmlFor="crime-select" className="block text-sm font-bold text-brand-sage mb-2">
                    Filter by Crime Type
                </label>
                <select
                    id="crime-select"
                    value={selectedCrime}
                    onChange={(e) => setSelectedCrime(e.target.value)}
                    className="w-full p-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-brand-sage focus:border-transparent outline-none bg-white text-gray-700"
                >
                    {crimeTypes.map(type => (
                        <option key={type} value={type}>{type}</option>
                    ))}
                </select>
                <div className="mt-2 text-xs text-gray-500">
                    Showing {filteredData.length} incidents
                </div>
            </div>

            <MapContainer
                center={center}
                zoom={zoom}
                scrollWheelZoom={true}
                style={{ height: "100%", width: "100%" }}
                className="z-0"
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                />
                {filteredData.map((point, index) => (
                    <CircleMarker
                        key={index}
                        center={point.coordinates}
                        pathOptions={{
                            color: point.original_color,
                            fillColor: point.original_color,
                            fillOpacity: 0.6,
                            weight: 1,
                            radius: 5 // Fixed pixel radius for visibility at all zoom levels
                        }}
                    >
                        <Popup className="botanical-popup">
                            <div className="font-sans text-sm leading-relaxed text-gray-800">
                                <h3>{point.crime_type}</h3>
                                <p>{point.location}</p>
                            </div>
                        </Popup>
                    </CircleMarker>
                ))}
            </MapContainer>

            {/* Reuse the same popup styles or define new ones if needed */}
            <style>{`
        .botanical-popup .leaflet-popup-content-wrapper {
          background: #F0F4EF;
          border-radius: 4px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          padding: 0;
        }
        .botanical-popup .leaflet-popup-content {
          margin: 12px;
          line-height: 1.5;
        }
        .botanical-popup h3 {
          font-family: 'Inter', sans-serif;
          font-weight: 700;
          color: #4A7C59;
          margin-bottom: 4px;
          font-size: 1rem;
          border-bottom: 1px solid #D8F1A0;
          padding-bottom: 4px;
        }
        .botanical-popup p {
          margin: 0;
          font-size: 0.9rem;
          color: #555;
        }
      `}</style>
        </div>
    );
};

export default CrimeMap;
