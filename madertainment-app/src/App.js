// react_app/src/App.js
import React from 'react';
import PageTitle from './PageTitle';
import CriteriaTable from './CriteriaTable';

const App = () => {
    const [criteriaData, setCriteriaData] = useState([
        { name: 'Free', selected: false }, // if event.price == 'Free'
        { name: 'Morning (6am-10:59am)', selected: false }, // if event.time >= 6am && event.time < 11am
        { name: 'Afternoon (11am-5:59pm)', selected: false }, // if event.time > 11am && event.time < 6pm
        { name: 'Night (6pm-12am)', selected: false }, // if event.time => 6pm && event.time < 12am
    ])

    const [events, setEvents] = useState([
        { name: 'Event1', setting: { date: '2023-01-01', time: '18:00', location: 'Venue1' }, price: 'Free', description: 'Description1' },
        { name: 'Event2', setting: { date: '2023-02-15', time: '20:00', location: 'Venue2' }, price: '10', description: 'Description2' },
    ]);

    // for each criteria in criteriaData, if the critera's name matches criteriaName, then flip selected
    const handleToggle = (criteriaName) => {
        setCriteriaData(() =>
            prevData.map((criteria) =>
                criteria.name === criteriaName ? { ...criteria, selected: !criteria.selected } : criteria
            )
        );
    };

    // For every event in events, choose each one that matches all selected criteria or is free (if free is selected)
    const filteredEvents = events.filter((event) => {
        return criteriaData.every((criteria) => criteria.selected || (event.price === criteria.name && criteria.selected));
    });


    return (
        <div>
            <PageTitle title="Madertainment" />
            <CriteriaTable criteriaData={criteriaData} onToggle={handleToggle} />
            {/* Maps every filtered event into a box and renders it */}
            {filteredEvents.map((event, index) => (
                <Box key={index} event={event} />
            ))}
        </div>
    );
};

export default App;
