import React, { useEffect, useState } from 'react'
import './TranscriptDataRows.css'
import { BASE_URL } from '../App'
import DataInsights from './DataInsights'

const TranscriptDataRows = ({params}) => {
    const [rows, setRows] = useState([])
    const [loading, setLoading] = useState(false)
    const [summaryAll, setSummaryAll] = useState("");

    const [modalOpen, setModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState("");

    const fetchRows = async () => {
        console.log(params.col_name + params.operator + params.col_value)
        if (!params || !params.col_name || !params.col_value || !params.operator) return
        setLoading(true)

        let endpoint = BASE_URL + '/get_transcript_data';

        if (params.operator === '=' && ['transcript_id', 'month', 'reasoning'].includes(params.col_name)) {
            endpoint = BASE_URL + '/search_transcript_data'
        }

        if (['>', '>=', '<', '<='].includes(params.operator) && ['transcript_id', 'month', 'reasoning'].includes(params.col_name)) {
            alert("!! Invalid operation is being performed !!")
            return
        }

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params),
            })

            const data = await res.json()
            setRows(data || [])

        } catch (err) {
            console.error('Error fetching rows:', err)
            setRows([])
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        if (params) {
            fetchRows()
        }
    }, [params])

    const handleFetchSummaryAll = async() => {
        const payload = {
          rows: rows,
          query: params.col_name + params.operator + params.col_value
        }
        setLoading(true)
        try {
            const res = await fetch(BASE_URL+'/get_analyzed_transcript_data', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            })
        
            const data = await res.json()
        
            if (data.analysis) {
                setSummaryAll(data.analysis)
                setModalContent(data.analysis)
                setModalOpen(true)
            } else {
                setModalContent("No analysis available :/")
                setModalOpen(true)
            }
    
        } catch (error) {
          console.error('Error submitting:', error)
        } finally {
            setLoading(false)
        }
    }

    const handleFetchStrategy = async() => {
        const payload = {
          insights: summaryAll,
          query: params.col_name + params.operator + params.col_value
        }
        setLoading(true)
        try {
            const res = await fetch(BASE_URL+'/get_fallback_strategy_for_insights', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            })
    
            const data = await res.json()
        
            if (data.analysis) {
                setModalContent(data.analysis);
                setModalOpen(true);
            } else {
                setModalContent("No strategy available :/");
                setModalOpen(true);
            }
    
        } catch (error) {
          console.error('Error submitting:', error)
        } finally {
            setLoading(false)
        }
    }
    
    const handleRowAnalyze = async (transcript_id) => {
        setLoading(true)
        try {
            const res = await fetch(BASE_URL+'/get_transcript_summary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                col_value: transcript_id,
                }),
            })

            const data = await res.json()

            if (data.analysis) {
                setModalContent(data.analysis);
                setModalOpen(true);
            } else {
                setModalContent("No summary available :/");
                setModalOpen(true);
            }
        } catch (err) {
          setModalContent("Failed to fetch analysis.");
          setModalOpen(true);
        } finally {
            setLoading(false)
        }
    }

    const HandleRowTranscriptText = async (transcript_id) => {
        setLoading(true)
        try {
            const res = await fetch(BASE_URL+'/get_transcript_text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                col_value: transcript_id,
                }),
            })

            const data = await res.json()
            const text = data.transcript_text

            if (text) {
                setModalContent(text);
                setModalOpen(true);
            } else {
                setModalContent("No transcript text available :/");
                setModalOpen(true);
            }
        } catch (err) {
            console.log(err)
            setModalContent("Failed to transcript text.");
            setModalOpen(true);
        } finally {
            setLoading(false)
        }
    }

    if (!params) return null;
    if (loading) {
        return (
          <div className="loading-overlay">
            <div className="spinner">Loading...</div>
          </div>
        )
    }
    if (rows.length === 0) return <p>No data available</p>

    const columnNames = rows.length > 0 ? Object.keys(rows[0]) : []

    return (
        <>
            <div className='questions'>
                <button className='analysis_button' onClick={handleFetchSummaryAll}>Transcripts Analysis??</button>
                <button className='analysis_button' onClick={handleFetchStrategy}>Fallback Strategy?</button>
                <DataInsights isOpen={modalOpen} onClose={() => setModalOpen(false)}>
                    <textarea
                    readOnly
                    style={{ width: '900px', height: '600px', overflow: 'auto', fontSize: 'x-large',
                        fontWeight: 'bold', backgroundColor: 'rgb(0, 0, 0)'
                     }}
                    value={modalContent}
                    />
                </DataInsights>
            </div>
            <div className='data_rows'>
                <table border="1" cellPadding="8" style={{ width: '100%', marginTop: '1rem' }}>
                    <thead>
                        <tr>
                        {columnNames.map(col => <th key={col}>{col}</th>)}
                        <th colSpan="2">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.map((row, idx) => (
                        <tr key={idx}>
                            {columnNames.map(col => <td key={col}>{row[col]}</td>)}
                            <td>
                                <button onClick={() => handleRowAnalyze(row.transcript_id)}>Fetch Summary</button>
                            </td>
                            <td>
                                <button onClick={() => HandleRowTranscriptText(row.transcript_id)}>Fetch Transcript</button>
                            </td>
                        </tr>
                        ))}
                    </tbody>
                </table>
                <DataInsights isOpen={modalOpen} onClose={() => setModalOpen(false)}>
                    <textarea
                    readOnly
                    style={{ width: '900px', height: '600px', overflow: 'auto', fontSize: 'x-large',
                        fontWeight: 'bold', backgroundColor: 'rgba(0,0,0,0)'
                     }}
                    value={modalContent}
                    />
                </DataInsights>
            </div>
        </>
    )
    }

export default TranscriptDataRows