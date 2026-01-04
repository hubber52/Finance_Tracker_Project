import { BrowserRouter, Route, Routes } from "react-router-dom";

import './App.css'
import './Styles/Base/Root.css'

//Import all pages
import LandingPage from './Pages/LandingPage';
import Register from './Pages/Register';
import Login from './Pages/Login';
import ExpenseSummary from './Pages/ExpenseSummaryPage';
import ExpensesCreate from './Pages/ExpenseCreatePage';
import DebtSummary from './Pages/DebtSummaryPage';
import DebtCreate from './Pages/DebtCreatePage';
import IncomeSummary from './Pages/IncomeSummaryPage';
import IncomeCreate from './Pages/IncomeCreatePage';
import OverviewPage from './Pages/OverviewPage';
import AboutPage from './Pages/AboutPage';
import ContactPage from './Pages/ContactPage';



function App() {

  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={ <LandingPage /> } />
          <Route path="/register" element = { <Register /> }  />
          <Route path="/login" element= { <Login /> } />
          <Route path='/expense' element= { <ExpenseSummary /> } />
          <Route path='/expense/create' element = { <ExpensesCreate /> }/>
          <Route path='/debt' element = { <DebtSummary /> }/>
          <Route path='/debt/create' element = { <DebtCreate /> } />
          <Route path='/income' element = { <IncomeSummary /> }  />
          <Route path='/income/create' element = { <IncomeCreate /> } />
          <Route path='/overview' element = { <OverviewPage /> } />
          <Route path='/about' element= { <AboutPage /> } />
          <Route path='/contact' element = { <ContactPage /> } />

      </Routes>
    </BrowserRouter>
  );
}

export default App
