import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import '../Styles/Components/BudgetNavigation.css';

function BudgetNavigation() {


  return (
    <div className = 'budget-navigation-bar'>
      <Navbar className="container-fluid">
        <Container className="budget-navigation-container">
          <Nav className="budget-navigation">
            <NavDropdown title="Expenses">
              <NavDropdown.Item href='/expense'> Expenses Breakdown </NavDropdown.Item>
              <NavDropdown.Item href='/expense/create'> Add Expense</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Debts">
              <NavDropdown.Item href="/debt"> Debt Breakdown </NavDropdown.Item>
              <NavDropdown.Item href="/debt/create"> Add Debt</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown title="Income">
              <NavDropdown.Item href="/income"> Income Breakdown </NavDropdown.Item>
              <NavDropdown.Item href="/income/create"> Add Income </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Container>
      </Navbar>
    </div>
  );
}

export default BudgetNavigation;