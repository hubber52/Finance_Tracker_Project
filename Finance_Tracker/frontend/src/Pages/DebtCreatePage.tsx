import { useState, useContext } from 'react';
import { APIContext } from '../Contexts/APIContext';
import axios from 'axios';
import BudgetNavigation from '../Components/BudgetNavigation';
import Navigation from '../Components/Navigation';

import '../Styles/Pages/crudCreate.css'

type Debt = {
    id: number;
    user: string;
    username: string;
    debt_amount: number;
    debt_payment: number;
    debt_name?: string;
    debt_rate: string;
    debt_interest: number;
    debt_notes?: string;
    debt_datetime: string;
}

function DebtCreate(){
    const token = localStorage.getItem('access_token');
    const url = useContext(APIContext);
    const [createform, setCreateForm] = useState({
        debt_amount : 0,
        debt_payment : 0,
        debt_name : '',
        debt_rate : 'Weekly',
        debt_interest: 0,
        debt_notes : '',

    });

    const handleChange = (event : any) => {
      const { name, value } = event.target; // Destructure name and value from the event target
      setCreateForm(prevFormData => ({
        ...prevFormData, // Spread the previous state to maintain other field values
        [name]: value,   // Update the specific field using its name as a dynamic key
      }));
    };

    const handleDropdown = (event : any) => {
        setCreateForm(event.target.value);
    }

    function debtPost(formData : any){
        formData.preventDefault();
        axios.post(url + 'debt/create',{
                debt_amount : createform.debt_amount,
                debt_payment : createform.debt_payment,
                debt_name : createform.debt_name,
                debt_rate : createform.debt_rate,
                debt_interest : createform.debt_interest,
                debt_notes : createform.debt_notes,
            },
            {headers: { Authorization: `Bearer ${token}` }
        })
        .then(function(response){
            console.log('Response:', response.data);
            if (!window.confirm('Entry Added')) return;
        })
        .catch(function(response){
            console.log("Failed To Create");
        })
    };

    return(
        <div>
            <Navigation />
            <div className="mainContent">
            <BudgetNavigation />
             <form onSubmit={debtPost} className = "crudForm">
                <label>
                Name
                <input
                    type="text"
                    name="debt_name"
                    value={createform.debt_name}
                    onChange={handleChange}
                />
                </label>
                <label>
                Amount
                <input
                    type="number"
                    name="debt_amount"
                    value={createform.debt_amount}
                    onChange={handleChange}
                />
                </label>
                <label> debt_payment
                    <input 
                        type = "number"
                        name = "debt_payment"
                        value = {createform.debt_payment}
                        onChange = {handleChange}
                    />
                </label>
                <label>
                Notes
                <input
                    type="text"
                    name="debt_notes"
                    value={createform.debt_notes}
                    onChange={handleChange}
                />
                </label>
                <label>
                Rate
                <select name = "debt_rate" value = {createform.debt_rate} onChange={handleChange}>
                    <option value="Weekly"> Weekly </option>
                    <option value = "Monthly"> Monthly </option>
                    <option value = "Annually"> Annually </option>
                </select>
                </label>
                <label> debt_interest
                    <input
                        type = "number"
                        name = "debt_interest"
                        value = {createform.debt_interest}
                        onChange = {handleChange}
                    />
                </label>
                <button className = "crudFormSubmitButton" type="submit">Submit</button>
           </form>
           </div>
        </div>
    );



}

export default DebtCreate;