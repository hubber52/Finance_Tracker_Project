import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { APIContext } from '../Contexts/APIContext';

import "../Styles/Pages/landing.css";

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [responseMessage, setResponseMessage] = useState('');
    const [responseError, setResponseError] = useState(false);
    const navigate = useNavigate();
    const url = useContext(APIContext);

    //Make login request to server login API
    const handleSubmit = async (e : any) => {
        e.preventDefault();

        axios.post(url + 'login/', {"username":username, "password":password})
            .then(function(response){
                console.log('Response:', response.data);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('username', username);
                navigate('/overview');
            })

            .catch(function(response){
                setResponseMessage('Error creating post.');
                setResponseError(true)
                console.log(responseError);
                if (!window.confirm('Invalid Credentials')) return;
            });
    console.log('Username:', {username});
    };

    return (
    <div className="landing">
        <button className="login-button" onClick = {() => navigate('/')}> Back </button>
        <div className="landing-header"> Log in to your account </div>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="username">Username:</label>
                <input
                    type="username"
                    id="username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                />
            </div>
            <button className="login-button" type="submit">Login</button>
        </form>
        <button className="register-button" onClick = {() => navigate('/register')}> Sign Up </button>
    </div>
    );
};

export default Login;