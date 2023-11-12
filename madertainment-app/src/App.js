import { useState, useEffect } from 'react';
import PageTitle from './PageTitle';
import CriteriaTable from './CriteriaTable';
import EventTable from './EventTable'
import SearchBar from './SearchBar';

export const App = () => {
    const [events, setEvents] = useState([]);
    const [filtered, setFiltered] = useState(deepCopyArray(events));

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch('http://localhost:5000/get_data');
            const jsonData = await response.json();
            setEvents(jsonData);
        } catch (error) {
            console.error('Error fetching JSON data:', error);
        }
    };

    const [criteriaData, setCriteriaData] = useState([
        { category: "Time", name: 'Morning (6am-10:59am)', selected: false },
        { category: "Time", name: 'Afternoon (11am-5:59pm)', selected: false },
        { category: "Time", name: 'Night (6pm-12am)', selected: false },
        { category: "Other", name: 'Free', selected: false }, // if event.price == 'Free'
    ]);

    // for each criteria in criteriaData, if the critera's name matches criteriaName, then flip selected
    const handleToggle = (criteria) => {
        criteriaData.filter(crit => crit.name === criteria.name).forEach((item) => { item.selected = !item.selected; });

        const freeEvents = getFreeEvents();

        setFiltered(freeEvents);
    }

    return (
        <div className="App">
            <PageTitle title="Madertainment" />
            <SearchBar />
            <CriteriaTable criteriaData={criteriaData} onToggle={handleToggle} />
            {/* Maps every filtered event into a box and renders it */}
            <EventTable eventData={filtered} />
        </div>
    );

    function getFreeEvents() {
        let count = 0;
        let temp = events.filter(event => {
            for (const criteria of criteriaData) {
                if (criteria.name === event.price) {
                    if (criteria.selected) {
                        count += 1;
                        return true;
                    }
                }
            }
            return false;
        });

        if (count === 0) {
            return deepCopyArray(events);
        } else {
            return deepCopyArray(temp);
        }
    }

    function deepCopyArray(arr) {
        return JSON.parse(JSON.stringify(arr));
    }
};

export default App;
