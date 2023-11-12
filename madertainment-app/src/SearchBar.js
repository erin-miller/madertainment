import { useState } from 'react'

function SearchBar() {
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = () => {
        console.log("Search term: ", searchTerm);
    }

    return (
      <div className="search-bar">
        <input type="text" placeholder="Search..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}/>
        <button onClick={handleSearch}>Search</button>
      </div>
    );
  }

  export default SearchBar;