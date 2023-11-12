const EventRow = ({ event }) => {

    return (
        <tr>
            <div>
                <p>{event.setting.date.date} {event.setting.time} {event.setting.location}</p>
                <p>{event.price}</p>
                <p>{event.description}</p>
            </div>
        </tr>
    );
};

export default EventRow;
