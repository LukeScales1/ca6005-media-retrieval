import React, {useState, KeyboardEvent} from 'react';
import {apiUrl} from './constants';
import axios from 'axios';
import './App.css';
// import sampleUrls from './results.json'
import SearchBar from "./components/SearchBar";
import imagenetClasses from './imagenetClasses.json'
import tagSuggestions from './tagLabels.json'

function App() {

  const [initialised, setInitialised] = useState(false);
  const [imageData, setImageData] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  // const [autocompleteList, setAutocompleteList] = useState([]);
  const [searchType, setSearchType] = useState('classes');

  const autocompleteList = () => {
    if (searchType === 'classes') {
      if (imagenetClasses !== undefined) {
        return imagenetClasses;
      }
    } else if (searchType === 'tags') {
      return tagSuggestions;
    }
    return [];
  }

  const images = () => {
    console.log('images', imageData);
    if (imageData !== undefined && imageData.length) {
      return imageData.sort(
        (a: {relevance: number;}, b: {relevance: number}) => (a.relevance) - (b.relevance));
    }
    return [];
  };

  const handleQuery = (e: string) => {
    console.log("set query", e);
    setQuery(e);
    console.log("query post set:", query);
  }

  const handleSearch = async () => {
    setLoading(true);
    console.log('search!', query)
    const data = await fetchData()
    console.log('data post search', data);
    setImageData(data);
    if (!initialised) {
      setInitialised(true);
    }
    setLoading(false);
  }

  const fetchData = async () => {
    let data = [];
    try {
      const response = await axios.get(apiUrl, {
        params: {
          q: query,
          search: searchType
        }
      });
      console.log(response);
      data = response.data.images;
    } catch (exception) {
      console.log(`ERROR: ${exception}`);
    }
    return data;
  }

  const updateSearchType = (e: any) => {
    console.log(e);
    setSearchType(e.target.value);
  }

  const checkKeyPress = (e: any) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }
  document.addEventListener("keydown", checkKeyPress);

  return (
    <div className="App">
      <header className="App-header">
        <div>Imagenet Class Searcher</div>

        {initialised ? (
          <div>
            <SearchBar
              list={autocompleteList()}
              searchType={searchType}
              onChange={(e: string) => handleQuery(e)}
              onSearchTypeUpdate={updateSearchType}
              handleSubmit={() => {setInitialised(true); handleSearch();}}/>
            <label >
              <input type="checkbox"/>
              only show relevant results
            </label>
          </div>
        ) : (<></>)}
      </header>
      <body>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="image-container">
          {images() !== undefined &&
          images().length !== 0 ? (
            images().map((i: {
              class: any;
              href: string;
              src: string;
              alt: string;
              relevance: number; }) => (
            <div>
              <div>
                <a href={'https://www.pinterest.ca' + i.href} target="_blank">
                  <img
                    src={i.src}
                    alt={i.alt}
                    className="images"
                  />
                </a>
                <span>
                  {searchType === 'classes' ? (
                    i.relevance === 1 ? ('Highly relevant') : (
                    i.relevance <= 3 ? ('Relevant') : i.relevance <= 5 ? ('Somewhat relevant') : i.relevance < 10 ?
                      ('Slightly relevant') : ('Irrelevant')
                    )
                  ) : (
                    i.class
                  )}
                </span>
              </div>
            </div>
          ))
            ) : (
              <>
                {initialised ? (
                  <>
                    <h2>Sorry! No results for this search. Please try again</h2>
                  </>
                ) :
                  (
                    <>
                      <h2>Ever wondered what some of the ImageNet classes actually looked like?</h2>
                      <p>Some of the classes from the ImageNet Challenge are kind of region-specific.</p>
                      <p>For example, worm (snake) fence: these fences are
                        specific to North America and, as an Irish native, I had never heard of these before this project!</p>
                      <p>Are you wondering what a worm fence is too? Type that, or it's synonyms (snake fence, snake-rail fence,
                        Virginia fence), or any of the other class names of the 1000 classes in ImageNet into the search bar
                        below to see some examples I've scraped from Pinterest.</p>
                      <SearchBar
                        list={autocompleteList()}
                        searchType={searchType}
                        onChange={(e: string) => handleQuery(e)}
                        onSearchTypeUpdate={updateSearchType}
                        handleSubmit={handleSearch}
                      />
                      <p>The results will be ordered by relevance as judged by an instance of InceptionResNetV2 - one of the
                        leading current models for the ImageNet Challenge.</p>
                    </>
                  )
                }
              </>
          )
          }
        </div>
      )}
      </body>
    </div>
  );
}

export default App;
