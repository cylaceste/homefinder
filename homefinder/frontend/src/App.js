import React, { useState } from 'react';
import Chat from './Chat';
import logo from './images/logo.png';  // Path to your local logo file
import MapPage from './MapPage';
import './App.css';

function App() {

  const [properties, setProperties] = useState( [{'latitude': 53.5058838, 'longitude': -113.4772348, 'info': 'property_name: "Beautiful Home in Hazeldean"\ndescription: "Steps from the Mill Creek ravine"\nnum_bedroom: 3\nnum_bathroom: 2\narea_size: 925\nprice: 2,100\ntransaction_type: Rent\nproperty_type: House\nparking: outdoor\nlaundry: in_suite\nfurnished: 0\npet_friendly: 1\nbuild_year: 1954\nsmoking_allowed: None\nair_conditioning: 0\nhardwood_floors: 1\nbalcony: 0\nimage_urls: https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073520.v.3de8f1cdf56610ab4feca0b792edc3fa.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073521.v.012bda82cb4dbc83aa770ff698a4befd.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073525.v.db3ea5fd38026943865951be022aad19.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073551.v.8904aeeb125ddbbca0ffdbd304e662ab.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073530.v.8951947b2d41c42bfd273b6aab3ccaa9.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073531.v.6c8979c81a8b9193342295f5380b0a93.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073535.v.2aa80403cce3f1c0d19c89eaecd0e5a6.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073536.v.0c7f7840184e64da8c678732872e9360.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8083946.v.e47e50eadf1972148ca451ad5df7a6b5.jpg', 'image_urls': 'https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073520.v.3de8f1cdf56610ab4feca0b792edc3fa.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073521.v.012bda82cb4dbc83aa770ff698a4befd.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073525.v.db3ea5fd38026943865951be022aad19.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073551.v.8904aeeb125ddbbca0ffdbd304e662ab.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073530.v.8951947b2d41c42bfd273b6aab3ccaa9.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073531.v.6c8979c81a8b9193342295f5380b0a93.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073535.v.2aa80403cce3f1c0d19c89eaecd0e5a6.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8073536.v.0c7f7840184e64da8c678732872e9360.jpg,https://f1a3d4fea3a9a877e732-356deb4d9644d2835b7712e712dbd1ea.ssl.cf2.rackcdn.com/494365/8083946.v.e47e50eadf1972148ca451ad5df7a6b5.jpg'}]);
  // console.log('Appjs', setProperties)
  return (
    <div className="App">
      <img src={logo} alt="Logo" className="logo"/>
      <Chat setProperties={setProperties} />
      {properties && <MapPage properties={properties} />}
    </div>
  );
}

export default App;

