import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import "../Styles/Pages/landing.css";

const LandingPage = () => {

    const [pageState, setPageState] = useState<String>("Landing")
    const navigate = useNavigate();
    return (
    <div className="landing">
        <h1 className="landing-header">Finance Tracker</h1>
        <button className="register-button" onClick = {() => navigate('/register')}> Sign Up </button>
        <button className="login-button" onClick = {() => navigate('/login')}> Login </button>
    </div>
    );

}


export default LandingPage;