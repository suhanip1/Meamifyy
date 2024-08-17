import React, { useState } from 'react';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [fileUrl, setFileUrl] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    console.log(selectedFile)
    console.log(selectedFile.type)
    if (selectedFile && selectedFile.type === 'audio/mp3' || 'audio/mpeg') {
      setFile(selectedFile);
    } else {
      alert('Please select a valid Audio file.');
    }
  };


  // Not Using this one
  const handleUpload1 = () => {
    if (file) {
      // Here you can add your upload logic
      console.log('Uploading file:', file);
      // For example, use fetch or axios to send the file to your server
      // Example:
      // const formData = new FormData();
      // formData.append('file', file);
      // axios.post('/upload', formData)
      //   .then(response => console.log(response))
      //   .catch(error => console.error(error));
    } else {
      alert('Please select a file to upload.');
    }
  };

  const handleUpload = () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      fetch('http://localhost:8080/upload', {  // Adjust the URL if needed
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.file_url) {
            setFileUrl(data.file_url);
          }
          console.log(data.message);
        })
        .catch(error => console.error('Error:', error));
    } else {
      alert('Please select a file to upload.');
    }
  };

  return (
    <div>
      <h1>Upload MP3 File</h1>
      <input 
        type="file" 
        accept=".mp3"
        onChange={handleFileChange} 
      />
      <button onClick={handleUpload}>Upload</button>
      {fileUrl && (
        <div>
          <h2>Uploaded File</h2>
          <audio controls>
            <source src={`http://localhost:8080${fileUrl}`} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
};

export default UploadPage;