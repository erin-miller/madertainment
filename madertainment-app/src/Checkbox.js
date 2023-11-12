const Checkbox = ({ text }) => {
    return (
        <div className="checkbox-wrapper">
            <label>
                <input type="checkbox" />
                <span>{text}</span>
            </label>
        </div>
    );
};

export default Checkbox;
