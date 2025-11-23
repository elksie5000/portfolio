import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { getApiBaseUrl } from '../utils/api';

const WarDeadMap = () => {
  const [warDeadData, setWarDeadData] = useState([]);
  // Center the map roughly on Europe/UK as a starting point
  const center = [50.5, 2.5];
  const zoom = 6;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseUrl = getApiBaseUrl();
        const response = await fetch(`${baseUrl}/api/war-dead/all`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setWarDeadData(data);
      } catch (error) {
        console.error('Error fetching war dead data:', error);
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
        {warDeadData.map((point, index) => (
          <CircleMarker
            key={index}
            center={point.coordinates}
            pathOptions={{
              color: '#4A7C59', // brand-sage
              fillColor: '#4A7C59',
              fillOpacity: 0.6,
              weight: 1,
              radius: 5
            }}
          >
            <Popup className="botanical-popup">
              <div
                className="font-sans text-sm leading-relaxed text-gray-800 max-h-64 overflow-y-auto"
                dangerouslySetInnerHTML={{ __html: point.bio_html }}
              />
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      {/* Custom styles for the popup to match Tufte principles (clean, minimal) */}
      <style>{`
        .botanical-popup .leaflet-popup-content-wrapper {
          background: #F0F4EF; /* Light botanical background */
          border-radius: 4px;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
          padding: 0;
        }
        .botanical-popup .leaflet-popup-content {
          margin: 12px;
          line-height: 1.5;
        }
        .botanical-popup h3 {
          font-family: 'Inter', sans-serif;
          font-weight: 700;
          color: #4A7C59; /* brand-sage */
          margin-bottom: 8px;
          font-size: 1.1rem;
          border-bottom: 1px solid #D8F1A0; /* brand-lime */
          padding-bottom: 4px;
        }
        .botanical-popup p {
          margin-bottom: 8px;
          font-size: 0.9rem;
        }
        .botanical-popup b {
          color: #2C4A34; /* Darker sage for emphasis */
        }
      `}</style>
    </div>
  );
};

export default WarDeadMap;
