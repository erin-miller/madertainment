const Box = ({ event }) => {
    return (
        <div className="box">
=            <h2>{event.name}</h2>
            <p>{event.setting.date.date} {event.setting.time} {event.setting.location}</p>
            <p>{event.price}</p>
            <p>{event.description}</p>
=        </div>
    )
}

export default Box;