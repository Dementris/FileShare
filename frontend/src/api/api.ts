import axios from 'axios';
import {useNavigate} from "react-router-dom";

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        const navigate = useNavigate();

        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refreshToken');

            if (refreshToken) {
                try {
                    const { data } = await axios.post('http://127.0.0.1:8000/api/v1/auth/refresh', null, {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`,
                        },
                    });

                    localStorage.setItem('accessToken', data.accessToken);
                    localStorage.setItem('refreshToken', data.refreshToken);
                    api.defaults.headers.common['Authorization'] = `Bearer ${data.accessToken}`;

                    originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    console.error('Refresh token failed', refreshError);
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    navigate("/login")
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;