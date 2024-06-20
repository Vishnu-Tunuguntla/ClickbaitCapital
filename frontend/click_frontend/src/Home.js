import React, { useState, useEffect } from 'react';
import './Home.css';

// Icon components
const HypeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" className="icon">
    <circle cx="50" cy="50" r="45" fill="#8e44ad"/>
    <text x="50" y="57" fontFamily="Arial, sans-serif" fontSize="24" fill="white" textAnchor="middle">Hype</text>
  </svg>
);

const RedditIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" className="icon">
    <circle cx="50" cy="50" r="45" fill="#ff4500"/>
    <text x="50" y="57" fontFamily="Arial, sans-serif" fontSize="20" fill="white" textAnchor="middle">Reddit</text>
  </svg>
);

const TwitterIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" className="icon">
    <circle cx="50" cy="50" r="45" fill="#1da1f2"/>
    <text x="50" y="57" fontFamily="Arial, sans-serif" fontSize="20" fill="white" textAnchor="middle">Twitter</text>
  </svg>
);

function Home({ topStocks, setTopStocks }) {
  const [reddit, setReddit] = useState(5);
  const [twitter, setTwitter] = useState(5);
  const [news, setNews] = useState(5);
  const [lastRefresh, setLastRefresh] = useState(null);
  const [currentTime, setCurrentTime] = useState(Date.now());

  const fetchTopStocks = async () => {
    const response = await fetch(`http://localhost:5000/api/top-stocks?reddit_weight=${reddit/10}&twitter_weight=${twitter/10}&news_weight=${news/10}`);
    const data = await response.json();
    setTopStocks(data);
    setLastRefresh(Date.now());
  };

  const handlePollClick = () => {
    fetchTopStocks();
  };

  useEffect(() => {
    const timeInterval = setInterval(() => {
      setCurrentTime(Date.now());
    }, 1000); // Update every second

    return () => clearInterval(timeInterval);
  }, []);

  const timeSinceLastRefresh = () => {
    if (!lastRefresh) return 'Not refreshed yet';
    const seconds = Math.floor((currentTime - lastRefresh) / 1000);
    return `${seconds} seconds ago`;
  };

  const getIconForWebsite = (website) => {
    switch (website) {
      case 'news':
        return <HypeIcon />;
      case 'reddit.com':
        return <RedditIcon />;
      case 'twitter.com':
        return <TwitterIcon />;
      default:
        return website;
    }
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
          <div className="slider-label">News: <span>{news}</span></div>
          <input
            type="range"
            min="0"
            max="10"
            value={news}
            onChange={(e) => setNews(e.target.value)}
          />
        </div>
        <button onClick={handlePollClick}>Poll</button>
      </div>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Stock</th>
              <th>Price</th>
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
                  <td>{stock.Price || 'NA'}</td>
                  <td>{stock.sentiment || ''}</td>
                  <td>{getIconForWebsite(stock.website)}</td>
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