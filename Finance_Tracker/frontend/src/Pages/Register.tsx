import { useState, useContext, useRef } from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import { APIContext } from '../Contexts/APIContext';

import "../Styles/Pages/landing.css";

const Register = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [responseMessage, setResponseMessage] = useState('');
    const navigate = useNavigate();
    const url = useContext(APIContext);
    const cancelAsync = useRef(false) 

    const validatePhone = (phone: any) => {
        const validateNumber = /^\+1[0-9]{10}$/
        if (!validateNumber.test(phone)){
            if (!window.confirm('Phone number does not meet required format')) return;
                cancelAsync.current = true
        }
    }
    
    const handleSubmit = async (e : any) => {
        e.preventDefault();
        cancelAsync.current = false;
    // API call to register a user
        try {
          console.log("Try Register")
          validatePhone(phone);
          if (cancelAsync.current){
            return;
          }
          console.log("Validated Phone")
          const response = await axios.post(url+'register/', 
                                            {"username":username, 
                                            "password":password, 
                                            "email":email, 
                                            "phone":phone});
          console.log("Created response object")
          setResponseMessage('Post created successfully!');
          console.log('Response:', response.data);
          if(!window.confirm('Account creation successful, please log in')) return;
          navigate('/login')
        } 
        catch (error) {
          setResponseMessage('Error creating post.');
          console.error('Error:', error);
          if (!window.confirm('Please try another username')) return;
          return;
        }
    console.log('Username:', {username});
    };

    return (
        <div className="landing">
            <button className="login-button" onClick = {() => navigate('/')}> Back </button>
            <div className="landing-header"> Register for a new account </div>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                        <input
                            type="username"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="email">Email</label>
                        <input
                        type = "email"
                        id = "email"
                        value = {email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="phone"> Phone </label>
                        <input
                        type = "tel"
                        id = "phone"
                        value = {phone}
                        name = "phone"
                        onChange = {(e) => setPhone(e.target.value)}
                        />
                </div>
                <button className="register-button" type="submit">Sign Up</button>
 
            </form>
            <button className="login-button" onClick = {() => navigate('/login')}> Login</button>
        </div>
    );
};

export default Register;