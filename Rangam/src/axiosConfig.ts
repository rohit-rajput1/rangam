// src/axiosConfig.ts
import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000', // Change this to your Django backend URL
});

export default instance;
