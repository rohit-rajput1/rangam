// src/components/FileUpload.tsx
import React, { useState } from 'react';
import axios from '../axiosConfig';
import './FileUpload.css';

const FileUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [jobDescription, setJobDescription] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError("Please select a file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('/extract_job_description', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setJobDescription(response.data.job_description);
            setError(null);
        } catch (err) {
            setError("Failed to upload file and extract job description.");
        }
    };

    return (
        <div className="container">
            <h1>Upload Resume PDF</h1>
            <p>Extract the job description from your resume in PDF format.</p>
            <label className="label-file">
                Choose file
                <input type="file" onChange={handleFileChange} accept=".pdf" />
            </label>
            <br />
            <button onClick={handleUpload}>Extract</button>
            {error && <p className="error">{error}</p>}
            {jobDescription && (
                <div className="job-description">
                    <h2>Extracted Job Description:</h2>
                    <p>{jobDescription}</p>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
