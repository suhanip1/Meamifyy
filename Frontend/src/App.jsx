import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';

import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';

function App() {
  const [count, setCount] = useState(0);

  const fetchAPI = async () => {
    try {
      const response = await axios.get('http://localhost:8080/api/users');
      console.log(response.data);
    } catch (error) {
      console.error('There was an error fetching users!', error);
    }
  };

  useEffect(() => {
    fetchAPI();
  }, []);

  return (
    <Router>
      <Routes>
        
        <Route path="/signIn" element={<SignIn />} />
        <Route path="/signUp" element={<SignUp />} />
        
      </Routes>
    </Router>
  );
}

export default App;
