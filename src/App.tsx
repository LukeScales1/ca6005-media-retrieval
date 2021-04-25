import React from 'react';
import { apiUrl } from './constants';
import axios from 'axios';
import './App.css';
import sampleUrls from './sample_urls.json'

function App() {

  const sampleImages = () => {
    if (sampleUrls !== undefined) {
      return sampleUrls.urls;
    } return [];
  };

  const urls = sampleImages();
  console.log(urls);

  const fetchData = async () => {
    let response = "nada";
    try {
      response = await axios.get(apiUrl);
    } catch (exception) {
      process.stderr.write(`ERROR: ${exception}`);
    }
    return response;
  }

  const initResponse = fetchData()
  console.log(initResponse)

  return (
    <div className="App">
      <header className="App-header">
        <div>Imagenet Class Searcher</div>
        <input/>
      </header>
      <body>
        <div className="image-container">
          {sampleImages() !== undefined &&
          sampleImages().length !== 0 &&
          sampleImages().map((i) => (
            <div>
              <img
                src={i}
                alt="new"
                className="images"
                />
            </div>
          ))}
        </div>
      </body>
    </div>
  );
}

export default App;
