import { useState } from 'react';

const Checkbox = ({ criteria, onToggle }) => {
    const [isChecked, setIsChecked] = useState(false);
    return (
        <div className="checkbox-wrapper">
            <label>
                <input type="checkbox" isChecked={isChecked} onChange={() => {
                    setIsChecked((prev) => !prev);
                    onToggle(criteria)
                    console.log(criteria);
                    }} />
            </label>
            <span>{criteria.name}</span>
        </div>
    );
};

export default Checkbox;
