import React from 'react';
import './GuidePage.css';

const GuidePage = () => {
  return (
    <div className="container">
      <div className="header">
        <div className="logo">Meamify</div>
        <div className="nav">
          <a href="#">Home</a>
          <a href="#">Guide</a>
          <a href="#">Create</a>
        </div>
      </div>

      <div className="step">
        <h2>Step 1: Upload Your PDF</h2>
        <div className="content">
          <p>Start by uploading your document to Memefy. Simply drag and drop your PDF into our platform, or click the upload button to select your file.</p>
          <img src="/path/to/upload-icon.png" alt="Upload Icon" />
        </div>
      </div>

      <div className="step">
        <h2>Step 2: Automated Analysis</h2>
        <div className="content step2-content">
          <div className="item">
            <img src="/path/to/analysis-icon.png" alt="Content Analysis" />
            <p>Content Analysis</p>
          </div>
          <div className="item">
            <img src="/path/to/theme-icon.png" alt="Theme/Topic Assembly" />
            <p>Theme/Topic Assembly</p>
          </div>
          <div className="item">
            <img src="/path/to/quiz-icon.png" alt="Question Preparation" />
            <p>Question Preparation</p>
          </div>
        </div>
      </div>

      <div className="step">
        <h2>Step 3: Meme Creation</h2>
        <div className="content step2-content">
          <div className="item">
            <img src="/path/to/magic-icon.png" alt="Transform Magic" />
            <p>Transform Magic</p>
          </div>
          <div className="item">
            <img src="/path/to/templates-icon.png" alt="Meme Templates" />
            <p>Meme Templates</p>
          </div>
          <div className="item">
            <img src="/path/to/interactive-icon.png" alt="Interactive Q&A" />
            <p>Interactive Q&A</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Memefy;
