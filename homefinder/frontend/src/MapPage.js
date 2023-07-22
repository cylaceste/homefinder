import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Tooltip } from 'react-leaflet';
import axios from 'axios';
import {L, Icon} from 'leaflet';

const redIcon = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

function MapPage() {
    const [locations, setLocations] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/get_locations')
            .then(response => {
                setLocations(response.data);
            })
            .catch(error => {
                console.log('Error fetching locations:', error);
            });
    }, []);

    const ChangeView = ({ bounds }) => {
        const map = useMap();
        bounds && map.fitBounds(bounds, { padding: [50, 50] });
        return null;
    }

    let bounds;
    if (locations.length > 0) {
        bounds = L.latLngBounds(locations.map(location => [location.latitude, location.longitude]));
        bounds = bounds.pad(0.1);
    }

    return (
        <MapContainer style={{ height: "100vh", width: "100%" }}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {locations.map((location, index) => (
                <Marker icon={redIcon} key={index} position={[location.latitude, location.longitude]}>
                    <Popup>
                        {location.info}
                    </Popup>
                    <Tooltip>{location.info}</Tooltip>
                </Marker>
            ))}
            <ChangeView bounds={bounds} />
        </MapContainer>
    );
}

export default MapPage;
