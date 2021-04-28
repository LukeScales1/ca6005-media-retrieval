import React from 'react';
import Autocomplete from "../Autocomplete/Autocomplete";

const SearchBar = (props) => (
  <div>
    {/*<input*/}
    {/*  type="text"*/}
    {/*  className={props.className}*/}
    {/*  onChange={props.onChange}*/}
    {/*>*/}
    {/*</input>*/}
    <Autocomplete
      suggestions={props.list} onChange={props.onChange} onSubmit={props.handleSubmit}
    />
    {/*<input type="submit" value="Search" onClick={props.handleSubmit} />*/}
  </div>
);
export default SearchBar;
