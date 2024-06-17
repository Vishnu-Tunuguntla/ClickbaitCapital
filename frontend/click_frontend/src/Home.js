// Home.js
import React, { useState, useEffect } from 'react';
import './Home.css';

function Home({ topStocks, setTopStocks }) {
  const [reddit, setReddit] = useState(5);
  const [instagram, setInstagram] = useState(5);
  const [facebook, setFacebook] = useState(5);
  const [isPolling, setIsPolling] = useState(false);

  const fetchTopStocks = async () => {
    const response = await fetch(`http://localhost:5000/api/top-stocks?reddit_weight=${reddit/10}&twitter_weight=${instagram/10}&facebook_weight=${facebook/10}`);
    const data = await response.json();
    setTopStocks(data);
  };

  const handleRunClick = () => {
    fetchTopStocks();
    setIsPolling(true);
  };

  useEffect(() => {
    let interval;
    if (isPolling) {
      interval = setInterval(() => {
        fetchTopStocks();
      }, 10000); // Fetch every 10 seconds
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isPolling, reddit, instagram, facebook]);

  return (
    <div className="Home">
      <div className="grey-box">
        <div className="slider-container">
          <div className="slider-label">Reddit: <span>{reddit}</span></div>
          <input
            type="range"
            min="0"
            max="10"
            value={reddit}
            onChange={(e) => setReddit(e.target.value)}
          />
        </div>
        <div className="slider-container">
          <div className="slider-label">Instagram: <span>{instagram}</span></div>
          <input
            type="range"
            min="0"
            max="10"
            value={instagram}
            onChange={(e) => setInstagram(e.target.value)}
          />
        </div>
        <div className="slider-container">
          <div className="slider-label">Facebook: <span>{facebook}</span></div>
          <input
            type="range"
            min="0"
            max="10"
            value={facebook}
            onChange={(e) => setFacebook(e.target.value)}
          />
        </div>
        <button onClick={handleRunClick}>Run</button>
      </div>
      <div className="cards-container">
        {topStocks.map((stock, index) => (
          <div className="card" key={index}>
            <h3>{stock.Stock}</h3>
            <p>Preference Score: {stock.preference_score}</p>
            <p>Sentiment: {stock.sentiment}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
