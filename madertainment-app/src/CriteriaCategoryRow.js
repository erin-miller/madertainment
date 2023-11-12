import CriteriaRow from './CriteriaRow';

const CriteriaCategoryRow = ({ category, onToggle }) => {
  return (
    <>
      <tr>
        <th colSpan="2">{category.name}</th>
      </tr>
      {/* Maps each criteria to a row in this category */}
      {category.criteria.map((criteria, index) => (
        <CriteriaRow key={index} criteria={criteria} onToggle={onToggle} />
      ))}
    </>
  );
};

export default CriteriaCategoryRow;
