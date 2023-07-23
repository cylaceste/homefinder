import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.css';

function MapPage({ properties }) {
    return (
        <MapContainer center={[0, 0]} zoom={13} style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {properties.map((property, index) => (
                <Marker key={index} position={[property.latitude, property.longitude]}>
                    <Popup className="large-popup">
                        <span style={{whiteSpace: "pre-line"}}>{property.info}</span>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}

export default MapPage;
