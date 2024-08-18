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
    <div>
      <h1>Upload Files</h1>
      
      <div>
        <h2>Upload Audio or Video File</h2>
        <input 
          type="file" 
          accept=".mp3, .wav, .ogg, .m4a, .mp4, .mov, .avi, .mkv, .flv"
          onChange={handleFileChange}
        />
        <button onClick={() => handleUpload('file')}>
          Upload Audio/Video
        </button>
        {uploadStatusAudioVideo === 'success' && <span style={{ color: 'yellow', marginLeft: '10px' }}>✔️</span>}
        {uploadStatusAudioVideo === 'error' && <span style={{ color: 'red', marginLeft: '10px' }}>❌</span>}

        {/* Display the audio player just below the upload section */}
        {fileUrl && (
          <div style={{ marginTop: '20px' }}>
            <audio controls>
              <source src={`http://localhost:8080${fileUrl}`} type="audio/mp3" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </div>
      
      <div style={{ marginTop: '30px' }}>
        <h2>Upload PDF File</h2>
        <input 
          type="file" 
          accept=".pdf"
          onChange={handleFileChange}
        />
        <button onClick={() => handleUpload('pdf')}>
          Upload PDF
        </button>
        {uploadStatusPDF === 'success' && <span style={{ color: 'green', marginLeft: '10px' }}>✔️</span>}
        {uploadStatusPDF === 'error' && <span style={{ color: 'red', marginLeft: '10px' }}>❌</span>}
      </div>
    </div>
  );
};

export default UploadPage;
