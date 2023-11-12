import CriteriaCategoryRow from './CriteriaCategoryRow';

const CriteriaTable = ({ criteriaData, onToggle }) => {
  return (
    <table>
      <tbody>
        {criteriaData.map((category, index) => (
          <CriteriaCategoryRow key={index} category={category} onToggle={onToggle} />
        ))}
      </tbody>
    </table>
  );
};

export default CriteriaTable;
