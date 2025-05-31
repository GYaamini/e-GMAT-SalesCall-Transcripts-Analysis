import React from 'react'

const DataInsights = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null

    return (
        <div style={{
            position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
            backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', flexDirection: 'column',
            justifyContent: 'center', alignItems: 'center', zIndex: 1000
        }}>
            <div style={{
              backgroundColor: 'rgb(0,0,0)', padding: '1rem', borderRadius: '8px',
              width: '900px', height: '700px', boxShadow: '0 2px 10px rgba(0,0,0,0.3)'
            }}>
              {children}
              <button onClick={onClose} style={{ marginTop: '1rem' }}>Close</button>
            </div>
        </div>
    )
}

export default DataInsights