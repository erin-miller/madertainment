import Checkbox from "./Checkbox"
const CriteriaRow = ({ criteria, onToggle }) => {

    return (
        <tr>
            <div>
                <Checkbox criteria={criteria} onToggle={onToggle} key={criteria}/>
            </div>
        </tr>
    );
};

export default CriteriaRow;
