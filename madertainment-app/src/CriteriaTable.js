import CriteriaCategoryRow from './CriteriaCategoryRow';

const CriteriaTable = ({ criteriaData, onToggle }) => {
    const rows = [];
    let lastCategory = null;

    criteriaData.forEach((criteria) => {
        // do not start a new row until a different category is found
        if (criteria.category !== lastCategory) {
            rows.push(
            <CriteriaCategoryRow
                        criteria={criteria.category}
                        key={criteria.category}
                        />
                        )
        }
        rows.push(
            <CriteriaRow 
            criteria = {criteria}
            onToggle = {onToggle}
            key={criteria.name}
            />
        )
        lastCategory = criteria.category
    })

    rows.push()

    return (
        <table>
          <tbody>{rows}</tbody>
        </table>
      );
};

export default CriteriaTable;