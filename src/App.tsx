import React from 'react';
import logo from './logo.svg';
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
