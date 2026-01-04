import React, { useContext, useState, useEffect } from 'react';
import BudgetNavigation from '../Components/BudgetNavigation';
import { APIContext } from '../Contexts/APIContext';
import axios from 'axios';
import Navigation from '../Components/Navigation';

import '../Styles/Components/CrudTableStyle.css';

interface Expense {
    id: number;
    expense_name?: string;
    user: string;
    expense_category?: string;
    expense_amount: number;
    expense_notes?: string;
    expense_rate: string;
    expense_date: string;
}

interface ExpenseEdit {
    expense_name?: string;
    expense_category?: string;
    expense_amount: number;
    expense_notes?: string;
    expense_rate: string;
}

// Only show these columns in our table
type ColumnKey = keyof Omit<Expense, 'user' | 'expense_date'>;

const columns: ColumnKey[] = [
    'id',
    'expense_name',
    'expense_category',
    'expense_amount',
    'expense_notes',
    'expense_rate',
];

const ExpenseSummary: React.FC = () => {
  // Pull baseUrl from the context
  const baseUrl  = useContext(APIContext);
  const fetchUrl = `${baseUrl}/expense/get`;
  const editUrl = `${baseUrl}/expense`;

  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [showEditForm, setShowEditForm] = useState<boolean>(false);
  const [editPk, setEditPk] = useState<number>();
  const [editForm, setEditForm] = useState<ExpenseEdit>({
    expense_name : '',
    expense_category : 'Essential',
    expense_amount : 0,
    expense_notes : '',
    expense_rate : "Weekly",}
  );

  // Fetch the list on mount (and whenever fetchUrl changes)
    const getAll = useEffect(() => {
        const loadExpenses = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const { data } = await axios.get<Expense[]>(fetchUrl, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setExpenses(data);
        } 
            catch (err) {
                console.error('Failed to load expenses', err);
            }
        };

        loadExpenses();
    }, [fetchUrl]);

  // Delete handler
    const handleDelete = async (id: number) => {
        if (!window.confirm('Delete this expense?')) return;

        try {
            const token = localStorage.getItem('access_token');
            await axios.delete(`${editUrl}/${id}`, {
                headers: { Authorization: `Bearer ${token}` },
        })
        .then(function(response){
            console.log("Delete Response", response)
        });
        setExpenses(prev => prev.filter(event => event.id !== id));
        } 
        catch (err) {
            console.error('Failed to delete expense', err);
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

    //Initialzes and renders edit forms
    const handleEditForm = (expenseObject : Expense) => {
        setEditPk(expenseObject.id);
        //Set initial state of rendered forms.
        setEditForm({expense_name : expenseObject.expense_name,
            expense_amount : expenseObject.expense_amount,
            expense_category : expenseObject.expense_category,
            expense_notes : expenseObject.expense_notes,
            expense_rate : expenseObject.expense_rate
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
            await axios.put(`${editUrl}/${editPk}`, {
                expense_name : editForm.expense_name,
                expense_amount: editForm.expense_amount,
                expense_category: editForm.expense_category,
                expense_notes: editForm.expense_notes,
                expense_rate: editForm.expense_rate,
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
      <Navigation />
      <div className="main-content"> 
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
          {expenses.map(expenseObject => (
            <>
            <tr key={expenseObject.id}>
              {//Use slice to omit the "id" field from displaying on the table
              columns.slice(1).map((item, index : number) => (
                <td key={index}>{expenseObject[item]}</td>
              ))}
              <td>
                <button onClick={() => handleEditForm(expenseObject)}>
                    Edit
                </button>
              </td>
              <td>
                <button onClick={() => handleDelete(expenseObject.id)}>
                    Delete
                </button>
                
              </td>
            </tr>
            </>
          ))}
        </tbody>
      </table>
        }
        {
        showEditForm && <form className = "crudForm" onSubmit = {handleEditRequest}>
            <label> expense_name
                <input
                    type = "text"
                    name = "expense_name"
                    value = {editForm.expense_name}
                    onChange = {handleEditFormChange}
                />
            </label>
            <label> expense_category
                <select
                    name = "expense_category"
                    value = {editForm.expense_category}
                    onChange = {handleEditFormChange}>
                  <option value="Essential"> Essential </option>
                  <option value="Discretionary"> Discretionary </option>
                </select>
            </label>
            <label> expense_amount
                <input
                    type = "number"
                    name = "expense_amount"
                    value = {editForm.expense_amount}
                    onChange = {handleEditFormChange}
                />
            </label>
            <label> expense_notes
                <input
                    type = "text"
                    name = "expense_notes"
                    value = {editForm.expense_notes}
                    onChange = {handleEditFormChange}
                />
            </label>
                <label>
                Rate
                <select name="expense_rate" value={editForm.expense_rate} onChange={handleEditFormChange}> 
                    <option value="Weekly"> Weekly </option>
                    <option value="Monthly"> Monthly</option>
                    <option value="Annually"> Annually </option>
                </select>
                </label>
            <button className = "crudFormSubmitButton" type="submit"> Submit </button>
            <button onClick = {() => setShowEditForm(!showEditForm)}> Cancel </button>
        </form>
        }
      </div>
    </div>
  );
};

export default ExpenseSummary;