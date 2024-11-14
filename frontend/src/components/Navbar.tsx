// src/components/Navbar.tsx
import React, {useEffect, useState} from 'react';
import {AppBar, Toolbar, Button, Typography, Box, CircularProgress} from '@mui/material';
import {Link} from 'react-router-dom';
import api from "../api/api.ts";


const Navbar: React.FC = () => {
    const [userInfo, setUserInfo] = useState<any>(null);
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        const fetchMe = async () => {
            try {
                const userResponse = await api.get('/users/me')
                setUserInfo(userResponse.data)
                setLoading(false)
            } catch (error) {
                console.error('Error fetching data:', error);
                setLoading(false)
            }
        };
        fetchMe();
    }, []);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress/>
            </Box>
        );
    }
    return (
        <AppBar position="sticky">
            <Toolbar>
                <Typography variant="h6" sx={{flexGrow: 1}}>
                    FileShare
                </Typography>
                <Box>
                    <Button
                        component={Link}
                        to="/files"
                        color="inherit"
                        sx={{textTransform: 'none', marginRight: 2}}
                    >
                        Files
                    </Button>
                </Box>
                {userInfo.role == 'admin' && (
                    <Box>
                        <Button
                            component={Link}
                            to={"/admin"}
                            color="inherit"
                            sx={{textTransform: 'none', marginRight: 2}}
                        >
                            Admin Panel
                        </Button>
                    </Box>
                )}
                {userInfo && (
                    <Box sx={{display: 'flex', alignItems: 'center', marginLeft: 3}}>
                        <Typography variant="body2" sx={{marginRight: 2}}>
                            {userInfo.username} ({userInfo.email})
                        </Typography>
                        <Box
                            sx={{
                                padding: '2px 8px',
                                backgroundColor: userInfo.role === 'admin' ? '#ff1500' : '#d512cf',
                                color: 'white',
                                borderRadius: '4px',
                                fontSize: '0.875rem',
                            }}
                        >
                            {userInfo.role}
                        </Box>
                    </Box>
                )}

            </Toolbar>
        </AppBar>
    );
};

export default Navbar;

