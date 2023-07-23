import React from 'react';
import Chat from './components/Chat/Chat';
import PropertyList from './components/PropertyList/PropertyList';
import Map from './components/Map/Map';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="pane">
        <Chat />
      </div>
      <div className="pane">
        <PropertyList />
      </div>
      <div className="pane">
        <Map />
      </div>
    </div>
  );
}

export default App;
