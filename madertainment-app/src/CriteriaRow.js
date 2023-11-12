const CriteriaRow = ({ criteria, onToggle }) => {
  return (
    <tr>
      <td>{criteria.name}</td>
      <td>
        <input
          type="checkbox"
          checked={criteria.selected}
          onChange={() => onToggle(criteria.name)}
        />
      </td>
    </tr>
  );
};

export default CriteriaRow;
