import React from 'react';

const SearchBar = (props) => (
  <div>
    <input
      type="text"
      className={props.className}
      onChange={props.onChange}
    >
    </input>
    <input type="submit" value="Search" onClick={props.handleSubmit} />
  </div>
);
export default SearchBar;
