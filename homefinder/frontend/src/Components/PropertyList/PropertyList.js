import React from 'react';
import './PropertyList.css';

function PropertyList({ properties }) {
    return (
        <div className="PropertyList">
            {properties.map((property, index) => (
                <div key={index} className="property-item">
                    <h2>{property.address}</h2>
                    {/* Add more details here as needed */}
                </div>
            ))}
        </div>
    );
}

export default PropertyList;
