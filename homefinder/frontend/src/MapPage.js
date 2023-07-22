import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Tooltip } from 'react-leaflet';
import axios from 'axios';
import L, { Icon } from 'leaflet';

const redIcon = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

function MapPage() {
    const [locations, setLocations] = useState([]);

    const ChangeView = ({ bounds }) => {
        const map = useMap();
        bounds && map.fitBounds(bounds);
        return null;
    }

    useEffect(() => {
        axios.get('http://localhost:5000/get_locations')
            .then(response => {
                setLocations(response.data);
            })
            .catch(error => {
                console.log('Error fetching locations:', error);
            });
    }, []);

    let bounds;
    if (locations.length > 0) {
        bounds = locations.map(location => [location.latitude, location.longitude]);
    }

    return (
        <MapContainer center={[0, 0]} zoom={13} style={{ height: "100vh", width: "100%" }}>
            <ChangeView bounds={bounds} />
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {locations.map((location, index) => (
                <Marker key={index} position={[location.latitude, location.longitude]} icon={redIcon}>
                    <Popup>
                        {location.info}
                    </Popup>
                    <Tooltip>{location.info}</Tooltip>
                </Marker>
            ))}
        </MapContainer>
    );
}

export default MapPage;
