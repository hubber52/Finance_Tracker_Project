import axios from 'axios';

export const Logout = async (url : any, access_token : any, refresh_token: any, event : any) => {
    await axios.post(url, {refresh : `${refresh_token}`}, {headers: {
        Authorization : `Bearer ${access_token}`
    }
    })
    .then((response) => {
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
        if (!window.confirm('Logged Out Successfully')) return;

    }) 
    .catch((response) => {
        console.log(response, "Failed to logout");
        if (!window.confirm('Failed to Logout')) return;
    })
}

export default Logout;