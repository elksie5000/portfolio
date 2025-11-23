import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Circle, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { getApiBaseUrl } from '../utils/api';

const CrimeMap = () => {
    const [crimeData, setCrimeData] = useState([]);
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

    return (
        <div className="w-full h-full min-h-[600px] bg-bg-base relative z-0">
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
                {crimeData.map((point, index) => (
                    <Circle
                        key={index}
                        center={point.coordinates}
                        pathOptions={{
                            color: point.original_color,
                            fillColor: point.original_color,
                            fillOpacity: 0.6,
                            weight: 1,
                            radius: 100 // Radius from original map
                        }}
                    >
                        <Popup className="botanical-popup">
                            <div className="font-sans text-sm leading-relaxed text-gray-800">
                                <h3>{point.crime_type}</h3>
                                <p>{point.location}</p>
                            </div>
                        </Popup>
                    </Circle>
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
