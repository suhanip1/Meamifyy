import React, { useState } from 'react';

const UploadPage = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'audio/mp3') {
      setFile(selectedFile);
    } else {
      alert('Please select a valid MP3 file.');
    }
  };

  const handleUpload = () => {
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

  return (
    <div>
      <h1>Upload MP3 File</h1>
      <input 
        type="file" 
        accept=".mp3"
        onChange={handleFileChange} 
      />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadPage;
