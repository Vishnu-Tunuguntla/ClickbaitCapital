// App.js
import React, { useState } from 'react';
import Home from './Home';

function App() {
  const [topStocks, setTopStocks] = useState([]);

  return (
    <Home topStocks={topStocks} setTopStocks={setTopStocks} />
  );
}

export default App;
