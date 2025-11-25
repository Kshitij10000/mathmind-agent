import logo from '/logo.png'
import './Sidebar.css'

function Sidebar() {
    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <img
                    src={logo}
                    alt="MathMind Logo"
                    className="sidebar-logo"
                />
                <h1 className="sidebar-title">MathMind</h1>
                <p className="sidebar-subtitle">AI Mathematical Assistant</p>
            </div>

            <div className="sidebar-content">
                <div className="sidebar-section">
                    <h3 className="section-title">About</h3>
                    <p className="section-description">
                        Advanced AI-powered platform for solving complex mathematical problems with step-by-step explanations and real-time feedback.
                    </p>
                </div>

                <div className="sidebar-section">
                    <h3 className="section-title">Features</h3>
                    <ul className="features-list">
                        <li>Problem-solving assistance</li>
                        <li>Step-by-step solutions</li>
                        <li>Interactive feedback</li>
                        <li>Solution verification</li>
                    </ul>
                </div>
            </div>

            <div className="sidebar-footer">
                <div className="status-indicator">
                    <span className="status-dot"></span>
                    <span className="status-text">System Active</span>
                </div>
            </div>
        </div>
    )
}

export default Sidebar