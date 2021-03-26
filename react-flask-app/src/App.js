import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import Login from './Login';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    setInterval(async () => {
      fetch('/time').then(res => res.json()).then(data => {
        setCurrentTime(data.time);
      });
    }, 2000);
  }, []);


  return (
    <div className="App">
      <p>The current time iss {currentTime}.</p>
      <Login/>
    </div>
  );
}

export default App;