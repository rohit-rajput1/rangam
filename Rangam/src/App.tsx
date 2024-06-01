// src/App.tsx
import React from 'react';
import FileUpload from './components/FileUpload';
import './App.css';

const App: React.FC = () => {
    return (
        <div className="App">
            <FileUpload />
            <footer>
                <p>&copy; 2024 Your Company. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default App;
