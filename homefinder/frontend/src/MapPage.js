import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import axios from 'axios';
import L, { LatLngBounds, LatLng } from 'leaflet';
import 'leaflet/dist/leaflet.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function MapPage(properties) {
    var [locations, setLocations] = useState([]);
    // console.log(properties.properties)

    var locations = properties.properties
    // useEffect(() => {
    //     axios.get('http://localhost:5000/get_locations')
    //         .then(response => {
    //             setLocations(response.data);
    //         })
    //         .catch(error => {
    //             console.log('Error fetching locations:', error);
    //         });
    // }, []);

    const ChangeView = ({ bounds }) => {
        const map = useMap();
        bounds && map.fitBounds(bounds);
        return null;
    }

    let bounds;
    if (locations.length > 0) {
        bounds = new LatLngBounds(locations.map(location => new LatLng(location.latitude, location.longitude)));
    }

    return (
        <MapContainer center={[0, 0]} zoom={13} style={{ height: "100vh", width: "100%" }}>
            <ChangeView bounds={bounds} />
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {locations.map((location, index) => {
                let infoWithoutImageUrls = location.info;
                const imageUrlIndex = infoWithoutImageUrls.indexOf("image_urls: ");
                if(imageUrlIndex !== -1) {
                  infoWithoutImageUrls = infoWithoutImageUrls.substring(0, imageUrlIndex);
                }
                
                return (
                  <Marker key={index} position={[location.latitude, location.longitude]}>
                    <Popup className="large-popup">
                      <div className="custom-popup-content">
                        <span style={{whiteSpace: "pre-line"}}>{infoWithoutImageUrls}</span>
                        {
                        (location.image_urls && location.image_urls.length > 0) ? 
                            location.image_urls.split(',').slice(0, 6).map((url, index) => 
                            <img key={index} src={url} alt="Property" width="50" height="50"/>
                            ) : null
                        }
                      </div>
                    </Popup>
                  </Marker>
                );

            })}
        </MapContainer>
    );
}

export default MapPage;
