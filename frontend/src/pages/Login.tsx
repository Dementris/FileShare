// src/pages/Login.tsx
import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import api from '../api/api.ts';
import { useNavigate } from 'react-router-dom';
import {AxiosError} from "axios";

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await api.post('/auth/login', { email, password });
            const token = response.data.token;
            const user = response.data

            localStorage.setItem('accessToken', token.accessToken);
            localStorage.setItem('refreshToken', token.refreshToken);
            localStorage.setItem('role', user.role);

            navigate("/files")
        } catch (err) {
            // Cast the error to AxiosError type
            const error = err as AxiosError;

            // Check for 401 status and display an appropriate error message
            if (error.response && error.response.status === 401) {
                setError('Invalid email or password. Please try again.');
            } else {
                setError('An error occurred. Please try again later.');
            }
        }
    };

    return (
        <Container maxWidth="xs">
            <Box mt={8} display="flex" flexDirection="column" alignItems="center">
                <Typography component="h1" variant="h5">
                    Login
                </Typography>
                <Box component="form" onSubmit={handleSubmit} mt={2}>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        label="Email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        label="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <Button type="submit" fullWidth variant="contained" color="primary">
                        Login
                    </Button>
                </Box>
                {error && (
                    <Typography color="error" mt={2}>
                        {error}  {/* Display the error message */}
                    </Typography>
                )}
            </Box>
        </Container>
    );
};
export default Login;
