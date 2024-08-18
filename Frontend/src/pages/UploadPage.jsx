import React, { useState } from 'react';
import './uploadPageCSS.css'

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [fileUrl, setFileUrl] = useState('');

  // Separate upload status for each type of file
  const [uploadStatusAudioVideo, setUploadStatusAudioVideo] = useState(null);
  const [uploadStatusPDF, setUploadStatusPDF] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const validAudioTypes = ['audio/mp3', 'audio/mpeg'];
      const validVideoTypes = ['video/mp4', 'video/mov', 'video/avi', 'video/mkv', 'video/flv'];
      const validPdfType = 'application/pdf';

      if (validAudioTypes.includes(selectedFile.type) || validVideoTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setUploadStatusAudioVideo(null); // Reset audio/video upload status
      } else if (selectedFile.type === validPdfType) {
        setPdfFile(selectedFile);
        setUploadStatusPDF(null); // Reset PDF upload status
      } else {
        alert('Please select a valid audio, video, or PDF file.');
      }
    }
  };

  const handleUpload = (type) => {
    let selectedFile = null;
    let endpoint = '';
    if (type === 'file') {
      selectedFile = file;
      endpoint = '/upload'; // Endpoint for audio/video
    } else if (type === 'pdf') {
      selectedFile = pdfFile;
      endpoint = '/upload_pdf'; // Endpoint for PDF
    }

    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);

      fetch(`http://localhost:8080${endpoint}`, {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (type === 'file') {
            if (data.file_url) {
              setFileUrl(data.file_url);
            }
            setUploadStatusAudioVideo('success'); // Mark audio/video as success
          } else if (type === 'pdf') {
            setUploadStatusPDF('success'); // Mark PDF as success
          }
        })
        .catch(error => {
          console.error('Error:', error);
          if (type === 'file') {
            setUploadStatusAudioVideo('error'); // Mark audio/video as error
          } else if (type === 'pdf') {
            setUploadStatusPDF('error'); // Mark PDF as error
          }
        });
    } else {
      alert('Please select a file to upload.');
    }
  };

  return (
    <div className="upload-page">
      <nav className="navbar">
        <div className="logo">
          <img src="memelogo.png" alt="Logo" />
          <span>Memeify.</span>
        </div>
        <div className="nav-links">
          <a href="#home-content">Home</a>
          <a href="#">Guide</a>
          <a href="#">Create Quizlet</a>
          <a href="#">About</a>
        </div>
        <div className="button-group">
          <button>Sign up
            <div className="arrow-wrapper">
              <div className="arrow"></div>
            </div>
          </button>
          <button>Login
            <div className="arrow-wrapper">
              <div className="arrow"></div>
            </div>
          </button>
        </div>
      </nav>

      <div className="upload-section">
        <h1>Upload Files</h1>
        
        <div className="upload-audio-video">
          <h2>Upload Audio or Video File</h2>
          <input 
            type="file" 
            accept=".mp3, .wav, .ogg, .m4a, .mp4, .mov, .avi, .mkv, .flv"
            onChange={handleFileChange}
          />
          <button onClick={() => handleUpload('file')}>
            Upload Audio/Video
          </button>
          {uploadStatusAudioVideo === 'success' && <span className="status success">✔️</span>}
          {uploadStatusAudioVideo === 'error' && <span className="status error">❌</span>}

          {/* Display the audio player just below the upload section */}
          {fileUrl && (
            <div className="audio-player">
              <audio controls>
                <source src={`http://localhost:8080${fileUrl}`} type="audio/mp3" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
        </div>
        
        <div className="upload-pdf" style={{ marginTop: '30px' }}>
          <h2>Upload PDF File</h2>
          <input 
            type="file" 
            accept=".pdf"
            onChange={handleFileChange}
          />
          <button onClick={() => handleUpload('pdf')}>
            Upload PDF
          </button>
          {uploadStatusPDF === 'success' && <span className="status success">✔️</span>}
          {uploadStatusPDF === 'error' && <span className="status error">❌</span>}
        </div>
      </div>
    </div>
  );
};

export default UploadPage;