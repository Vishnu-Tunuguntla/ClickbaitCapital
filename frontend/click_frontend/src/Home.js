// Home.js
import React, { useState, useEffect } from 'react';
import './Home.css';

function Home({ topStocks, setTopStocks }) {
  const [reddit, setReddit] = useState(5);
  const [twitter, setTwitter] = useState(5);
  const [facebook, setFacebook] = useState(5);
  const [isPolling, setIsPolling] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(Date.now());
  const [currentTime, setCurrentTime] = useState(Date.now());

  const fetchTopStocks = async () => {
    const response = await fetch(`http://localhost:5000/api/top-stocks?reddit_weight=${reddit/10}&twitter_weight=${twitter/10}&facebook_weight=${facebook/10}`);
    const data = await response.json();
    setTopStocks(data);
    setLastRefresh(Date.now());
  };

  const handleRunClick = () => {
    fetchTopStocks();
    setIsPolling(true);
  };

  const handleStopClick = () => {
    setIsPolling(false);
    setReddit(5);
    setFacebook(5);
    setTwitter(5);  
  };

  useEffect(() => {
    let pollingInterval;
    if (isPolling) {
      pollingInterval = setInterval(() => {
        fetchTopStocks();
      }, 10000); // Fetch every 10 seconds
    }

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [isPolling, reddit, twitter, facebook]);

  useEffect(() => {
    const timeInterval = setInterval(() => {
      setCurrentTime(Date.now());
    }, 1000); // Update every second

    return () => clearInterval(timeInterval);
  }, []);

  const timeSinceLastRefresh = () => {
    const seconds = Math.floor((currentTime - lastRefresh) / 1000);
    return `${seconds} seconds ago`;
  };

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
          <div className="slider-label">Twitter: <span>{twitter}</span></div>
          <input
            type="range"
            min="0"
            max="10"
            value={twitter}
            onChange={(e) => setTwitter(e.target.value)}
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
        <button onClick={handleStopClick}>Stop</button>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Stock</th>
              <th>Preference Score</th>
              <th>Sentiment</th>
              <th>Website</th>
              <th>Last Refresh</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(topStocks) && topStocks.length > 0 ? (
              topStocks.map((stock, index) => (
                <tr key={index}>
                  <td>{stock.Stock || ''}</td>
                  <td>{stock.preference_score || ''}</td>
                  <td>{stock.sentiment || ''}</td>
                  <td>{stock.website || ''}</td>
                  <td>{timeSinceLastRefresh()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">No data available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Home;
