import Checkbox from "./Checkbox"
const CriteriaRow = ({ criteria }) => {

    return (
        <tr>
            <td>{criteria.name}</td>
            <div>
                <Checkbox label={criteria.name} />
            </div>
        </tr>
    );
};

export default CriteriaRow;
