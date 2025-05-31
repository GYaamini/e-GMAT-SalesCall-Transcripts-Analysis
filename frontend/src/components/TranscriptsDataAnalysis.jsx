import React, { useRef, useState } from 'react'
import './TranscriptsDataAnalysis.css'
import TranscriptDataRows from './TranscriptDataRows';
import { BASE_URL } from '../App';

const TranscriptsDataAnalysis = () => {
  const [columnName, setColumnName] = useState('transcript_id');
  const columnValue = useRef()
  const [operator, setOperator] = useState('=');
  
  const [submittedParams, setSubmittedParams] = useState(null);

  const handleSubmit = () => {
    const value = columnValue.current?.value?.trim()
    if (operator && columnName && value) {
      setSubmittedParams({
        operator: operator,
        col_name: columnName,
        col_value: value,
      })
    } else {
      alert("Enter all the required values")
    }
  }

  return (
    <>
      <div className='searchbar'>
        <select value={columnName} onChange={e => setColumnName(e.target.value)}>
          <option value="transcript_id">Transcript ID</option>
          <option value="month">Month</option>
          <option value="conversion_likelihood">Conversion Likelihood</option>
          <option value="reasoning">Reasoning</option>
        </select>

        <select value={operator} onChange={e => setOperator(e.target.value)}>
          <option value="=">= or LIKE</option>
          <option value="!=">!=</option>
          <option value=">">&gt;</option>
          <option value=">=">&gt;=</option>
          <option value="<">&lt;</option>
          <option value="<=">&lt;=</option>
        </select>

        <input 
            placeholder="Enter a value..."
            required 
            ref={columnValue}
        />

        <button onClick={handleSubmit}>Submit</button>
      </div>
      <div className='data'>
        <TranscriptDataRows params={submittedParams}/>
      </div>
    </>
  )
}

export default TranscriptsDataAnalysis