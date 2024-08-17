import React from 'react';
import { Link } from 'react-router-dom';
import './homepagecss.css'; // Ensure this path is correct

const HomePage = () => {
  return (
    <div>
      <nav className="navbar">
        <div className="logo">
          <img src="/memelogo.png" alt="Memeify Logo" /> {/* Ensure this path is correct */}
          <span>Memeify.</span>
        </div>
        <div className="nav-links">
          <Link to="/"><a href="#home-content">Home</a></Link>
          <Link to="/guidePage"><a href="#guidepage-content">Guide</a></Link>
          <a href="#">Create Quizlet</a>
        </div>
        <div className="button-group">
          <Link to="/signUp">
            <button>Sign up
              <div className="arrow-wrapper">
                <div className="arrow"></div>
              </div>
            </button>
          </Link>
          <Link to="/signIn">
            <button>Login
              <div className="arrow-wrapper">
                <div className="arrow"></div>
              </div>
            </button>
          </Link>
        </div>
      </nav>

      <div className="content-frame" id="home-content">
        {/* Add content here if needed */}
      </div>
    </div>
  );
};

export default HomePage;
