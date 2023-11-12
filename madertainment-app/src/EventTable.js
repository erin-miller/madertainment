import EventNameRow from './EventNameRow';
import EventRow from './EventRow';

const EventTable = ({ eventData }) => {
    const rows = [];
    let lastEvent = null;

    eventData.forEach((event) => {
        // do not start a new row until a different event is found
        if (event.name !== lastEvent) {
            rows.push(
                <EventNameRow
                    event={event}
                    key={event}
                />
            )
        }
        rows.push(
            <EventRow
                event={event}
                key={event}
            />
        )
        lastEvent = event.name
    })

    rows.push()

    return (
        <table className="event-table">
            <tbody>{rows}</tbody>
        </table>
    );
};

export default EventTable;
