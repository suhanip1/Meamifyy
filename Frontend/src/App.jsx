import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'
import UploadPage from './pages/UploadPage'
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

function App() {
  const [count, setCount] = useState(0)

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8080/api/users")
    console.log(response.data.users);
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <>
    <Router>
      <Routes>
        <Route path="/uploadPage" element={<UploadPage />} />
      </Routes>
    </Router>
    
    </>
  )
}

export default App
