// Home.js
import React, { useState } from 'react';
import './Home.css';

function Home() {
  const [reddit, setReddit] = useState(5);
  const [instagram, setInstagram] = useState(5);
  const [facebook, setFacebook] = useState(5);

  return (
    <div className="Home">
      <div className="grey-box">
        <div className="slider-container">
          <div className="slider-label">Reddit: <span>{reddit}</span></div>
          <input
            type="range"
            min="1"
            max="10"
            value={reddit}
            onChange={(e) => setReddit(e.target.value)}
          />
        </div>
        <div className="slider-container">
          <div className="slider-label">Instagram: <span>{instagram}</span></div>
          <input
            type="range"
            min="1"
            max="10"
            value={instagram}
            onChange={(e) => setInstagram(e.target.value)}
          />
        </div>
        <div className="slider-container">
          <div className="slider-label">Facebook: <span>{facebook}</span></div>
          <input
            type="range"
            min="1"
            max="10"
            value={facebook}
            onChange={(e) => setFacebook(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}

export default Home;
