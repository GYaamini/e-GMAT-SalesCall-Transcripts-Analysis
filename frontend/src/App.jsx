import './App.css'
import TranscriptsDataAnalysis from './components/TranscriptsDataAnalysis'

export const BASE_URL = import.meta.env.VITE_BASE_URL

function App() {
  return (
    <>
      <h2 className='heading'>e-GMAT Sales Call Transcripts Data Analysis</h2>
      <section className='main_section'>
        <TranscriptsDataAnalysis />
      </section>
    </>
  )
}

export default App
