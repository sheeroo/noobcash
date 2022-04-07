import axios from 'axios';
import { store } from 'store';
import { LOGOUT } from 'store/actions';

const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: 'https://localhost:44376'
});

export default axiosInstance;
