import React, { useContext, useState, useEffect } from 'react';
import BudgetNavigation from '../Components/BudgetNavigation';
import { APIContext } from '../Contexts/APIContext';
import axios from 'axios';
import Navigation from '../Components/Navigation';

import '../Styles/Pages/crudSummary.css';
import '../Styles/Components/CrudTableStyle.css';

interface Debt {
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

interface DebtEdit {
    debt_amount: number;
    debt_payment: number;
    debt_name?: string;
    debt_rate: string;
    debt_interest: number;
    debt_notes?: string;
}

// Only show these columns in our table
type ColumnKey = keyof Omit<Debt, 'user' | 'username' | 'debt_datetime'>;

const columns: ColumnKey[] = [
    'id',
    'debt_amount',
    'debt_payment',
    'debt_name',
    'debt_rate',
    'debt_interest',
    'debt_notes',
];

const DebtSummary: React.FC = () => {
  // Pull baseUrl from the context
  const baseUrl  = useContext(APIContext);
  const fetchUrl = `${baseUrl}/debt/get`;
  const updateUrl = `${baseUrl}/debt/update`;
  const deleteUrl = `${baseUrl}/debt/delete`;

  const [debts, setDebts] = useState<Debt[]>([]);
  const [showEditForm, setShowEditForm] = useState<boolean>(false);
  const [editPk, setEditPk] = useState<number>();
  const [editForm, setEditForm] = useState<DebtEdit>({
    debt_name : '',
    debt_amount : 0,
    debt_notes : '',
    debt_rate : '',
    debt_interest: 0,
    debt_payment: 0,
    }
  );

  // Fetch the list on mount (and whenever fetchUrl changes)
    const getAll = useEffect(() => {
        const loadDebts = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const { data } = await axios.get<Debt[]>(fetchUrl, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setDebts(data);
        } 
            catch (err) {
                console.error('Failed to load debts', err);
            }
        };

        loadDebts();
    }, [fetchUrl]);

  // Delete handler
    const handleDelete = async (id: number) => {
        if (!window.confirm('Delete this debt?')) return;

        try {
            console.log("Primary Key ID: ", id)
            const token = localStorage.getItem('access_token');
            await axios.delete(`${deleteUrl}/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
        })
        .then(function(response){
            console.log("Delete Response", response)
        });
        setDebts(prev => prev.filter(event => event.id !== id));
        } 
        catch (err) {
            console.error('Failed to delete debt', err);
        }
    };

    //Update edit form values as user types.
    const handleEditFormChange = (event : any) => {
      const { name, value } = event.target; // Destructure name and value from the event target
      setEditForm((prevFormData : any) => ({
        ...prevFormData, // Spread the previous state to maintain other field values
        [name]: value,   // Update the specific field using its name as a dynamic key
      }));
    };

    const handleEditDropdown = (event : any) => {
      setEditForm(event.target.value);
    }

    //Initialzes and renders edit forms
    const handleEditForm = (debtObject : Debt) => {
        setEditPk(debtObject.id);
        //Set initial state of rendered forms.
        setEditForm({debt_name : debtObject.debt_name,
            debt_amount : debtObject.debt_amount,
            debt_payment: debtObject.debt_payment,
            debt_rate : debtObject.debt_rate,
            debt_interest: debtObject.debt_interest,
            debt_notes : debtObject.debt_notes,
        }
        )
        setShowEditForm(!showEditForm);
    }

    //Submits edit form updates to server and reloads page
    const handleEditRequest = async(event : any) => {
        event.preventDefault();
        const token = localStorage.getItem('access_token');
        try{
            console.log("Sending Put Request");
            await axios.put(`${updateUrl}/${editPk}`, {
                debt_name : editForm.debt_name,
                debt_amount: editForm.debt_amount,
                debt_payment: editForm.debt_payment,
                debt_rate: editForm.debt_rate,
                debt_interest: editForm.debt_interest,
                debt_notes: editForm.debt_notes,
            }, {
                headers: { Authorization: `Bearer ${token}` },
            })
            .then(function(response){
                console.log("Put Response", response);
                setShowEditForm(!showEditForm);
            })
            .then(function(response) {
                window.location.reload()
            })
        }
        catch(err){
            console.log("Error updating the table", err);
        }
    }

  return (
    <div>
      <div className="main-content" style={{padding:50}}> 
      <Navigation />
      <BudgetNavigation />
      {!showEditForm && <table className = "crud-table">
        <thead>
          <tr>
            {//Use slice to omit the "id" field from displaying on the table
            columns.slice(1).map(columnHead => (
              <th key={columnHead}>{columnHead}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {debts.map(debtObject => (
            <>
            <tr key={debtObject.id}>
              {//Use slice to omit the "id" field from displaying on the table
              columns.slice(1).map((item, index : number) => (
                <td key={index}>{debtObject[item]}</td>
              ))}

              <td>
                 <button onClick={() => handleEditForm(debtObject)}>
                    Edit
                </button>
              </td>
              <td>
                {!showEditForm && 
                <button onClick={() => handleDelete(debtObject.id)}>
                    Delete
                </button>
                }
              </td>
            </tr>
            </>
          ))}
        </tbody>
      </table>}
        {
        showEditForm && <form className = "crudForm" onSubmit = {handleEditRequest}>
            <label> debt_name
                <input
                    type = "text"
                    name = "debt_name"
                    value = {editForm.debt_name}
                    onChange = {handleEditFormChange}
                />
            </label>
            <label> debt_amount
                <input
                    type = "number"
                    name = "debt_amount"
                    value = {editForm.debt_amount}
                    onChange = {handleEditFormChange}
                />
            </label>
            <label>
              debt_payment
              <input
                type = "number"
                name = "debt_payment"
                value = {editForm.debt_payment}
                onChange = {handleEditFormChange}
              />
            </label>
            <label> debt_notes
                <input
                    type = "text"
                    name = "debt_notes"
                    value = {editForm.debt_notes}
                    onChange = {handleEditFormChange}
                />
            </label>
            <label> debt_rate
                <select name="debt_rate" value={editForm.debt_rate} onChange = {handleEditFormChange}>
                  <option value="Weekly"> Weekly </option>
                  <option value='Monthly'> Monthly </option>
                  <option value='Annually'> Annually </option>
                </select>
            </label>
            <label> debt_interest
              <input 
                type = "number"
                name = "debt_interest"
                value = {editForm.debt_interest}
                onChange = {handleEditFormChange}
              />
            </label>
            <button className = "crudFormSubmitButton" type="submit"> Submit </button>
            <button onClick = {() => setShowEditForm(!showEditForm)}> Cancel </button>
        </form>
        }
        </div>
    </div>
  );
};

export default DebtSummary;