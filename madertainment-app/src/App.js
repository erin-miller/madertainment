// react_app/src/App.js
import React from 'react';
import PageTitle from './PageTitle';
import CriteriaTable from './CriteriaTable';
import Box from './Box';
import { useState, useEffect } from 'react';

const App = () => {
    const [events, setEvents] = useState([]);

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
    }

    const [criteriaData, setCriteriaData] = useState([
        { category: "Time", name: 'Morning (6am-10:59am)', selected: false }, // if event.time >= 6am && event.time < 11am
        { category: "Time", name: 'Afternoon (11am-5:59pm)', selected: false }, // if event.time > 11am && event.time < 6pm
        { category: "Time", name: 'Night (6pm-12am)', selected: false }, // if event.time => 6pm && event.time < 12am
        { category: "Other", name: 'Free', selected: false }, // if event.price == 'Free'
    ])

    // for each criteria in criteriaData, if the critera's name matches criteriaName, then flip selected
    const handleToggle = (criteriaName) => {
        setCriteriaData((criteriaData) =>
        (criteriaData.map((criteria) =>
            criteria.name === criteriaName ? (!criteria.selected) : criteria
        )))
    };

    // For every event in events, choose each one that matches all selected criteria or is free (if free is selected)
    const filteredEvents = events.filter((event) => {
        return criteriaData.some((criteria) => event.price === criteria.name && criteria.selected);
    });

    return (
        <div className="App">
            <PageTitle title="Madertainment" />
            <CriteriaTable criteriaData={criteriaData} onToggle={handleToggle} />
            {/* Maps every filtered event into a box and renders it */}
            {filteredEvents.map((event) => (
                <h1>{event.name}</h1>
            ))}
            
        </div>
    );
};

export default App;
