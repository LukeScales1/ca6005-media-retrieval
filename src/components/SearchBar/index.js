import React from 'react';
import Autocomplete from "../Autocomplete/Autocomplete";

const SearchBar = (props) => (
  <div>
    <div>
      <select value={props.searchType} onChange={props.onSearchTypeUpdate}>
        <option value="classes">Classes</option>
        <option value="tags">Tags</option>
      </select>
    </div>
    <div>
      {/*<input*/}
      {/*  type="text"*/}
      {/*  className={props.className}*/}
      {/*  onChange={props.onChange}*/}
      {/*>*/}
      {/*</input>*/}
      <Autocomplete
        suggestions={props.list} onUpdate={props.onChange} onSubmit={props.handleSubmit}
      />
      {/*<input type="submit" value="Search" onClick={props.handleSubmit} />*/}
    </div>
  </div>
);
export default SearchBar;
