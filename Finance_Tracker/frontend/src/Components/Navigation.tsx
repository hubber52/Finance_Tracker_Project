import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Logout from './Logout';
import {APIContext} from '../Contexts/APIContext';
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import '../Styles/Components/Navigation.css';

const Navigation = () => {
    const url = useContext(APIContext) + 'logout/';
    const access_token = localStorage.getItem('access_token')
    const refresh_token = localStorage.getItem('refresh_token')
    const navigate = useNavigate();
    
    const logout = async (event : any) => {
      Logout(url, access_token, refresh_token, event)
      navigate('/')
    }

    return(
      <div className="main-navigation-bar">
        <Navbar >
          <Container className="container-fluid">
            <Nav className="main-navigation">
              <Nav.Link href='/overview'> Overview </Nav.Link>
              <Nav.Link href='./about'> About </Nav.Link>
              <Nav.Link href='./contact'> Contact Us</Nav.Link>
            </Nav>
          </Container>
        </Navbar>

        <p className="welcome-name"> Welcome {localStorage.getItem('username')} </p>
        <button className="logout-button" onClick={logout}> Logout </button>
      </div>
  );
}

export default Navigation;