import './index.css'
import Sidebar from './components/Sidebar'
import MathChat from './pages/MathChat'

function App() {
  return (
    <div style={{
      display: 'flex',
      width: '100%',
      height: '100vh',
      overflow: 'hidden',
    }}>
      <Sidebar />
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
      }}>
        <MathChat />
      </div>
    </div>
  )
}

export default App