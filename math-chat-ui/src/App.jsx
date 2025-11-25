import './App.css'
import Sidebar from './components/Sidebar'
import MathChat from './pages/MathChat'

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <MathChat />
      </div>
    </div>
  )
}

export default App