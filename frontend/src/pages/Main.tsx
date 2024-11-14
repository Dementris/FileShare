// src/pages/Main.tsx
import React from 'react';
import { Button, Container, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Main: React.FC = () => {
    const navigate = useNavigate();

    return (
        <Container maxWidth="sm">
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                height="100vh"
                textAlign="center"
            >
                <Typography variant="h3" gutterBottom>
                    Welcome to the App
                </Typography>
                <Typography variant="h6" color="textSecondary" gutterBottom>
                    Please log in or sign up to continue
                </Typography>
                <Box mt={4} display="flex" gap={2}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => navigate('/login')}
                    >
                        Login
                    </Button>
                    <Button
                        variant="outlined"
                        color="primary"
                        onClick={() => navigate('/signup')}
                    >
                        Signup
                    </Button>
                </Box>
            </Box>
        </Container>
    );
};

export default Main;
