import logo from '/logo.png'

function Sidebar() {
    return (
        <div style={{
            width: '280px',
            backgroundColor: '#f0f0f0',
            color: 'white',
            padding: '20px',
            height: '100vh',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: '2px 0 10px rgba(0, 0, 0, 0.1)',
        }}>
        <img 
        src={logo} 
        alt="MathMind Logo" 
        style={{ width: '60px', height: '60px', marginBottom: '20px' }}
        />
        <h1 style={{ fontSize: '24px', marginBottom: '30px' }}>MathMind</h1>
        <div style={{
            width: '100%',
            padding: '15px',
            backgroundColor: '#34495e',
            borderRadius: '8px',
            marginTop: '20px'
        }}>
            <p style={{ fontSize: '14px', opacity: 0.8 }}>
            Your AI-powered math assistant
            </p>
      </div>
    </div>
    )
}

export default Sidebar