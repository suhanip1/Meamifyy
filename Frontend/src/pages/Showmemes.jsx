import React, { useState } from 'react';

const MemeTemplates = () => {
    const [fileName, setFileName] = useState('');
    const [templates, setTemplates] = useState([]);
    const [error, setError] = useState('');

    const fetchTemplates = async () => {
        if (!fileName) {
            setError('Please enter a file name.');
            return;
        }

        try {
            //setFileName("https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3")

            const response = await fetch(`http://localhost:8080//api/memify?file_name=${fileName}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setTemplates(data);
            setError('');
        } catch (error) {
            console.error('Error fetching templates:', error);
            setError('Failed to fetch templates. Check console for details.');
        }
    };

    return (
        <div>
            <h1>Meme Templates</h1>
            <input 
                type="text" 
                value={fileName} 
                onChange={(e) => setFileName(e.target.value)} 
                placeholder="Enter file name"
            />
            <button onClick={fetchTemplates}>Fetch Templates</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div id="templatesContainer">
                {templates.map((template) => (
                    <div key={template.joke_id} className="template">
                        <h2>{template.name}</h2>
                        <p><strong>Question:</strong> {template.question}</p>
                        <p><strong>Joke:</strong> {template.joke}</p>
                        <p><strong>Joke Follow-Up:</strong> {template.joke_follow_up}</p>
                        <p><strong>Answer:</strong> {template.answer}</p>
                        <p><strong>Options:</strong></p>
                        <ul>
                            <li>1. {template.option_1}</li>
                            <li>2. {template.option_2}</li>
                            <li>3. {template.option_3}</li>
                            <li>4. {template.option_4}</li>
                        </ul>
                        <img src={template.url} alt={template.name} />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MemeTemplates;
